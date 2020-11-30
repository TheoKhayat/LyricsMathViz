from flask import Flask
#from datetime import datetime
from config import engine#, artistsTable

db_connection = engine.connect()
app = Flask('myApp')

@app.route('/')
def rootUrl():
    return 'hii'

@app.route('/get/<artist>')
def getHandler(artist):
    return 'Hiii ' + artist
    '''
    	viz_freq: {word_i: words.count(word_i)}
		viz_time: {punctuations: {',;'".?!$#@&}}
		viz_rapper: f(math...)
    '''

@app.route('/post/<artist_upload>')
def postHandler(artist_upload):
	return 'Handling upload: ' + artist_upload


try:
	if __name__ == '__main__':
		app.run()
except Exception as e:
	print('Something broke...', e)
finally:
	engine.dispose()