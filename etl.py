from requests import get
from sqlalchemy import create_engine, select, update
from sqlalchemy.schema import Table, MetaData
from config import engine, wordsTable

db_connection = engine.connect()


def getWordFromWords(getWord): # if word exists in Postgres then return record row else None
    result = db_connection.execute(
        select([wordsTable]).where(
            wordsTable.columns.word == getWord)).fetchone()
    return result if result else None

def insertIntoWords(thisWord, syllableCount=None, rhymeList=[], searched=False):
    existingRhymes = getWordFromWords(thisWord)
    if not existingRhymes:
        db_connection.execute(
            wordsTable.insert().values(
                word = thisWord
                ,syllables = syllableCount
                ,rhyming_words = rhymeList
                ,datamuse_searched = searched))
    else:
        (word, syllables, existingRhymingWords, datamuseSearched) = existingRhymes
        updatedRhymesList = list( set(existingRhymingWords) | set(rhymeList) )
        db_connection.execute(
            update(wordsTable)
                .where(wordsTable.c.word == thisWord)
                .values(
                    syllables = syllableCount if syllableCount else syllables
                    ,rhyming_words = updatedRhymesList
                    ,datamuse_searched = searched or datamuseSearched))               

def getRhymes(word): # GET request to datamuse API -> insert/update Postgres
    rhymes = get('https://api.datamuse.com/words?max=1000&rel_rhy=' + word).json()
    rhymeList = [rhyme['word'] for rhyme in rhymes]
    insertIntoWords(word, rhymeList=rhymeList, searched=True)
    for rhyme in rhymes:
        insertIntoWords(rhyme['word'], rhyme['numSyllables'], rhymeList)

def blastOff(artistName=None): # main entrypoint
    if artistName:
        localFilePath = f'/Users/theo/Rhymes/LyricsMathViz/cleaned_data/{artistName}.txt'
        wordsToGet = set(open(localFilePath).read().split())
    else:
        wordsToGet = [word[0] for word in db_connection.execute(
            select([wordsTable]).where(
                wordsTable.columns.datamuse_searched == False)).fetchall()]
    for word in wordsToGet:
        getRhymes(word)


try:
    blastOff() #blastOff('dr_seuss')
except Exception as e:
    print('Something broke...', e)
finally:
    engine.dispose()