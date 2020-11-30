import os, config
from num2words import num2words
from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData
# import pymongo # or use sql^


engine = create_engine(config.CONN_STRING)
artistsTable = Table('artists', MetaData(), autoload=True, autoload_with=engine)
db_connection = engine.connect()


def cleanKaggleLyrics(lyricsStr):
	wordsList = lyricsStr.replace('\n', ' ').replace('-', ' ').lower().split()
	cleanLyrics = []
	for word in wordsList:
		cleanedWord = ''.join([c for c in word if c.isalnum()])
		try:
			cleanedWord = num2words(float(cleanedWord)).replace('-', ' ')
		except Exception as e:
			pass
		finally:
			cleanLyrics.append(cleanedWord)
	return ' '.join(cleanLyrics)

for fileName in os.listdir(config.DATA_PATH):
	artistName = fileName.rstrip('.txt').replace('-', '_')
	filePath = config.DATA_PATH + fileName
	print('reading:', filePath)
	with open(filePath) as lyrics:
		lyricsStr = lyrics.read()
		cleanedLyricsStr = cleanKaggleLyrics(lyricsStr)
		db_connection.execute(
            artistsTable.insert().values(
                artist_name = artistName
                ,kaggle_lyrics = lyricsStr
                ,kaggle_lyrics_cleaned = cleanedLyricsStr))
	print(artistName, 'inserted!')
	with open(config.CLEANED_DATA_PATH + artistName + '.txt', 'w') as cleanedLyrics:
		cleanedLyrics.write(cleanedLyricsStr)
	print(artistName, 'written to clean_data/')

engine.dispose()