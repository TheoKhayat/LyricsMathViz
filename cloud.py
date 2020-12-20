from requests import get
from boto3 import resource

wordsDB = resource('dynamodb').Table('words')
artistsDB = resource('dynamodb').Table('artists')


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
    print('doin', thisWord)
    existingRhymes = getWordFromDynamoWords(thisWord)
    if not existingRhymes:
        wordsDB.put_item(
            Item = {
                'word': thisWord,
                'syllables': syllableCount,
                'rhyming_words': rhymeList,
                'datamuse_searched': searched})
    else:
        wordsDB.update_item(
            Key = {'word': thisWord},
            UpdateExpression = 'SET syllables=:s, rhyming_words=:r, datamuse_searched=:d',
            ExpressionAttributeValues = {
                ':s': syllableCount if syllableCount else existingRhymes['syllables'],
                ':r': list( set(existingRhymes['rhyming_words']) | set(rhymeList) ),
                ':d': searched or existingRhymes['datamuse_searched']})

def getRhymes(word): # GET request to datamuse API -> insert/update Dynamo
    rhymes = get('https://api.datamuse.com/words?max=1000&rel_rhy=' + word).json()
    rhymeList = [rhyme['word'] for rhyme in rhymes]
    insertIntoDynamoWords(word, rhymeList=rhymeList, searched=True)
    for rhyme in rhymes:
        insertIntoDynamoWords(rhyme['word'], rhyme['numSyllables'], rhymeList)

def getWords():
    response = wordsDB.scan()
    for word in response['Items']:
        if not word['datamuse_searched']:
            getRhymes(word['word'])
    while 'LastEvaluatedKey' in response:
        response = wordsDB.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        for word in response['Items']:
            if not word['datamuse_searched']:
                getRhymes(word['word'])

try:
    getWords()
except Exception as e:
    print('Something broke...', e)
finally:
    print('done :)')
    # engine.dispose()