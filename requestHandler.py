from flask import Flask
from config import engine

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

try:
	if __name__ == '__main__':
		app.run()
except Exception as e:
	print('Something broke...', e)
finally:
	engine.dispose()