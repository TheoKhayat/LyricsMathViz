from requests import get
from config import wordsDB, artistsDB
from boto3.dynamodb.conditions import Attr

def wordCount(lyrics):
    splitLyrics = lyrics.split()
    return {word: splitLyrics.count(word) for word in splitLyrics}

def artistsToDynamo():
    for row in connection.execute('SELECT * FROM artists').fetchall():
        (artistName, dirtyData, cleanedData) = row
        artistsDB.put_item(
            Item = {
                'artist_name': artistName,
                #'kaggle_lyrics': dirtyData,
                'cleaned_lyrics': cleanedData,
                'word_count': wordCount(cleanedData)})

def wordsToDynamo():
    for row in connection.execute('SELECT * FROM words').fetchall():
        (word, syllables, rhyming_words, datamuse_searched) = row
        wordsDB.put_item(
            Item = {
                'word': word,
                'syllables': syllables,
                'rhyming_words': rhyming_words,
                'datamuse_searched': datamuse_searched})

def getWordFromDynamoWords(getWord): # if word exists in Dynamo then return record row else None
    wordInDB = wordsDB.get_item(Key={'word': getWord})
    return wordInDB['Item'] if 'Item' in wordInDB else None

def insertIntoDynamoWords(thisWord, syllableCount=None, rhymeList=[], searched=False):
    existingRhymes = getWordFromDynamoWords(thisWord)
    if not existingRhymes:
        print('inserting:', thisWord)
        wordsDB.put_item(
            Item = {
                'word': thisWord,
                'syllables': syllableCount,
                'rhyming_words': rhymeList,
                'datamuse_searched': searched})
    else:
        updateFields = []
        expressionAttributeValues = {}

        if not existingRhymes['syllables'] and syllableCount:
            updateFields.append('syllables=:s')
            expressionAttributeValues[':s'] = syllableCount

        if not existingRhymes['datamuse_searched'] and searched:
            updateFields.append('datamuse_searched=:d')
            expressionAttributeValues[':d'] = True

        allRhymes = set(existingRhymes['rhyming_words']) | set(rhymeList)
        if len(allRhymes) > len(existingRhymes['rhyming_words']):
            updateFields.append('rhyming_words=:r')
            expressionAttributeValues[':r'] = list(allRhymes)

        if updateFields:
            print('updating:', thisWord, updateFields)
            wordsDB.update_item(
                Key = {'word': thisWord},
                UpdateExpression = 'SET ' + ','.join(updateFields),
                ExpressionAttributeValues = expressionAttributeValues)

def getRhymes(responseItems): # GET request to datamuse API -> insert/update Dynamo
    for rhymeRecord in responseItems:
        word = rhymeRecord['word']
        rhymes = get('https://api.datamuse.com/words?max=1000&rel_rhy=' + word).json()
        rhymeList = [rhyme['word'] for rhyme in rhymes]
        insertIntoDynamoWords(word, rhymeList=rhymeList, searched=True)
        for rhyme in rhymes:
            insertIntoDynamoWords(rhyme['word'], rhyme['numSyllables'], rhymeList)

def getWords():
    response = wordsDB.scan(FilterExpression=Attr('datamuse_searched').eq(False))
    getRhymes(response['Items'])
    while 'LastEvaluatedKey' in response:
        response = wordsDB.scan(FilterExpression=Attr('datamuse_searched').eq(False), ExclusiveStartKey=response['LastEvaluatedKey'])
        getRhymes(response['Items'])

try:
    getWords()
except Exception as e:
    print('Something broke...', e)
finally:
    print('done :)')