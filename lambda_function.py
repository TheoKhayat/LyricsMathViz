from boto3 import resource
from json import dumps

wordsTable = resource('dynamodb').Table('words')

def getWordsHandler(event, context):
    httpMethod = event['httpMethod']
    if httpMethod != 'GET':
        if httpMethod == 'OPTIONS':
            return builtResponse(300)
        else:
            return builtResponse(400, 'ERROR: route only accepts GET requests!')
    else:
        params = event['queryStringParameters']
        if not params or 'w' not in params:
            return builtResponse(500, 'ERROR: "w" parameter required!')
        else:
            results = {}
            wordsToRhyme = params['w'].split(',')
            for word in wordsToRhyme:
                wordRecord = wordsTable.get_item(Key={'word': word})
                if 'Item' not in wordRecord:
                    results[word] = None
                else:
                    thisRecord = wordRecord['Item']
                    if 'include_n_grams' in params and params['include_n_grams'] == 'yes':
                        thisRecordRhymes = thisRecord['rhyming_words']
                    else:
                        thisRecordRhymes = [word for word in thisRecord['rhyming_words'] if ' ' not in word]
                    results[word] = {
                        'syllables': int(thisRecord['syllables']) if thisRecord['syllables'] else None,
                        'rhymes': sorted(thisRecordRhymes)
                    }
            return builtResponse(200, dumps(results))

def builtResponse(statusCode, responseBody=None):
    response = {
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'statusCode': statusCode
    }
    if responseBody:
        response['body'] = responseBody
    return response
