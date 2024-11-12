import json
import boto3
from decimal import Decimal

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProcessedData')

def decimal_default(obj):
    """Helper function to convert Decimal objects to string or float."""
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float for JSON serialization
    raise TypeError("Type not serializable")

def lambda_handler(event, context):
    # Query the DynamoDB table (you can customize this query as needed)
    try:
        # Example of scanning the table (you can use query for more optimized fetching)
        response = table.scan()


        # Extract the items (rows)
        items = response.get('Items', [])

        # Return the items, converting Decimal to float for JSON compatibility
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # CORS header for S3 to access
            },
            'body': json.dumps(items, default=decimal_default)
        }

    except Exception as e:
        # Handle errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
