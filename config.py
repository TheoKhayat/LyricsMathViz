from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData
from boto3 import resource

DATA_PATH = 'data/'
CLEANED_DATA_PATH = 'cleaned_data/'
CONN_STRING = 'CONNECTION STRING HERE!!'

# engine = create_engine(CONN_STRING)
# artistsTable = Table('artists', MetaData(), autoload=True, autoload_with=engine)
# wordsTable = Table('words', MetaData(), autoload=True, autoload_with=engine)

wordsDB = resource('dynamodb').Table('words')
artistsDB = resource('dynamodb').Table('artists')