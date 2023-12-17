import json
import boto3
import logging
import base64
from botocore.exceptions import ClientError

#
# TODO: Don't use the same bucket as the website content
#       (For demo only)
#

BUCKET = 'joelodom'
FOLDER = 'received-data'
MONGO_DB_API_KEY = 'mongo-joel-api-key2'
MONGO_DB_API_KEY_REGION = 'us-east-1'
KEY_NAME = 'mongodb-api-key'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(
    service_name = 'secretsmanager',
    region_name = MONGO_DB_API_KEY_REGION
)

mongo_api_key = None

try:
    mongo_api_key = client.get_secret_value(
        SecretId = MONGO_DB_API_KEY
    )
    mongo_api_key = mongo_api_key['SecretString'] # kind of a hack
    mongo_api_key = json.loads(mongo_api_key) # even worse
    mongo_api_key = mongo_api_key[KEY_NAME] # inexcusable
except ClientError as e:
    # For a list of exceptions thrown, see
    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    raise e

def encode_to_base64(input_string):
    byte_data = input_string.encode('utf-8')
    base64_encoded = base64.b64encode(byte_data)
    return base64_encoded.decode('utf-8')

def lambda_handler(event, context):
    logger.info("Event: " + json.dumps(event))
    
    bucket_name = BUCKET
    key = event['queryStringParameters']['key']
    value = event['queryStringParameters']['value']

    # base64 sanitizes the input
    key = FOLDER + '/' + encode_to_base64(key)
        
    try:
        # Check if the file already exists
        s3.head_object(Bucket=bucket_name, Key=key)
        # If the file exists, return an error
        return {
            'statusCode': 409,
            'body': json.dumps('File already exists.')
        }
    except:
        pass # expected if the file doesn't exist

    s3.put_object(Bucket=bucket_name, Key=key, Body=value)
    return {
        'statusCode': 200,
        'body': json.dumps('File created successfully.')
    }
