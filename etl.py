from requests import get
from sqlalchemy import create_engine, select, update
from sqlalchemy.schema import Table, MetaData

engine = create_engine('postgresql://<USERNAME>:<PASSWORD>@localhost:5432/moar_data')
wordsTable = Table('words', MetaData(), autoload=True, autoload_with=engine)
db_connection = engine.connect()

def getWordFromWords(getWord):
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
        updatedRhymesList = list(set(existingRhymes[2]) | set(rhymeList))
        db_connection.execute(
            update(wordsTable)
                .where(wordsTable.c.word == thisWord)
                .values(
                    syllables = syllableCount if syllableCount else existingRhymes[1]
                    ,rhyming_words = updatedRhymesList
                    ,datamuse_searched = searched or existingRhymes[3]))               

def getRhymes(word):
    rhymes = get('https://api.datamuse.com/words?max=1000&rel_rhy=' + word).json()
    rhymeList = [rhyme['word'] for rhyme in rhymes]
    insertIntoWords(word, rhymeList=rhymeList, searched=True)
    for rhyme in rhymes:
        insertIntoWords(rhyme['word'], rhyme['numSyllables'], rhymeList)

def blastOff():
    wordsToGet = db_connection.execute(
        select([wordsTable]).where(
            wordsTable.columns.datamuse_searched == False)).fetchall()
    #wordsToGet = set(open('/Users/theo/Rhymes/LyricsMathViz/cleaned_data/dr_seuss.txt').read().split())
    for word in wordsToGet:
        getRhymes(word[0])

blastOff()

engine.dispose()
