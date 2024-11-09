import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProcessedData')

def lambda_handler(event, context):
    # Retrieve all items (you may adjust query/filter parameters as needed)
    response = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items']),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # To allow web browser access
        }
    }
