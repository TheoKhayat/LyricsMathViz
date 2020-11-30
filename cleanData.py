import os
from num2words import num2words
from config import DATA_PATH, CLEANED_DATA_PATH, engine, artistsTable

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

try:
	if __name__ == '__main__':

		for fileName in os.listdir(DATA_PATH):
			artistName = fileName.rstrip('.txt').replace('-', '_')
			filePath = DATA_PATH + fileName
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
			with open(CLEANED_DATA_PATH + artistName + '.txt', 'w') as cleanedLyrics:
				cleanedLyrics.write(cleanedLyricsStr)
			print(artistName, 'written to clean_data/')

except Exception as e:
	print('Something broke cleaning...', e)
finally:
	engine.dispose()