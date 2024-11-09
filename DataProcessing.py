import boto3
import json
from datetime import datetime

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Define the destination table name
destination_table = dynamodb.Table('ProcessedData')

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_item = record['dynamodb']['NewImage']

            # Extract and convert data from DynamoDB format
            city = new_item['city']['S']
            timestamp = int(new_item['timestamp']['N'])
            temperature_f = float(new_item['temperature']['N'])
            weather = new_item['weather']['S']
            humidity = int(new_item['humidity']['N'])

            # Transform timestamp to a readable format and convert temperature to Celsius
            readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            temperature_c = (temperature_f - 32) * 5.0 / 9.0

            # Prepare the transformed item for the destination table
            transformed_item = {
                'city': city,
                'timestamp': readable_time,
                'temperature': round(temperature_c, 2),
                'weather': weather,
                'humidity': humidity
            }

            # Insert the transformed item into the ProcessedData table
            try:
                destination_table.put_item(Item=transformed_item)
                print(f"Inserted transformed item: {json.dumps(transformed_item)}")
            except Exception as e:
                print(f"Error inserting item: {e}")

    return {"statusCode": 200, "body": json.dumps("Processed event with transformation successfully")}
