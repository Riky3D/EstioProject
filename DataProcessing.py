import boto3
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
destination_table = dynamodb.Table('ProcessedData')

def lambda_handler(event, context):
    for record in event.get('Records', []):
        if record['eventName'] == 'INSERT':
            try:
                new_item = record['dynamodb']['NewImage']

                city = new_item['city']['S']
                timestamp = int(new_item['timestamp']['N'])
                temperature_f = Decimal(new_item['temperature']['N'])
                weather = new_item['weather']['S']
                humidity = Decimal(new_item['humidity']['N'])

                # Convert timestamp to a readable format and add both versions
                readable_timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                temperature_c = (temperature_f - Decimal(32)) * Decimal(5) / Decimal(9)

                item = {
                    'city': city,
                    'timestamp': timestamp,                # Numeric timestamp for primary key
                    'readable_timestamp': readable_timestamp,  # Readable timestamp as an additional attribute
                    'temperature_c': round(temperature_c, 2),
                    'weather': weather,
                    'humidity': humidity
                }

                destination_table.put_item(Item=item)

            except Exception as e:
                print(f"Error processing record: {e}")
                raise
