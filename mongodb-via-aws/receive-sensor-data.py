#
# AWS Lambda function to receive an API request and insert the data into MongoDB.
# Going through AWS API Gateway and AWS Lambda incur cost, but you get the nice
# benefits that come with AWS, including security, etc.
#

import json
import boto3
import logging
import base64
from botocore.exceptions import ClientError
import http.client

logger = logging.getLogger()
logger.setLevel(logging.INFO)

MONGO_DB_API_KEY = "mongo-joel-api-key2"
MONGO_DB_API_KEY_REGION = "us-east-1"
KEY_NAME = "mongodb-api-key"

MONGO_DATASOURCE = "joelodom"
MONGO_DATABASE = "sensor-database"
MONGO_COLLECTION = "sensor-collection"

API_HOST = "us-east-2.aws.data.mongodb-api.com"
API_ENDPOINT = "/app/data-mjzzu/endpoint/data/v1/action/insertOne"

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

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Request-Headers": "*",
    "api-key": mongo_api_key
}

conn = http.client.HTTPSConnection(API_HOST)


def insert_key_value(key, val): # into MongoDB
    payload = {
        "dataSource": MONGO_DATASOURCE,
        "database": MONGO_DATABASE,
        "collection": MONGO_COLLECTION,
        "document": {
            "key": key,
            "value": val,
        }
    }

    conn.request("POST", API_ENDPOINT, body=json.dumps(payload), headers=HEADERS)
    response = conn.getresponse()

    response_data = response.read().decode()
    if response.status == 201:
        logger.info("Document inserted successfully.")
        logger.debug("Response: " + str(response_data))
    else:
        logger.error("Failed to insert document.")
        logger.info("Status Code: " + str(response.status))
        logger.info("Response: " + str(response_data))


def encode_to_base64(input_string): # returns a string
    byte_data = input_string.encode('utf-8')
    base64_encoded = base64.b64encode(byte_data)
    return base64_encoded.decode('utf-8')


def lambda_handler(event, context): # entry point for the lambda
    logger.info("Event: " + json.dumps(event))
    
    #bucket_name = BUCKET
    key = event['queryStringParameters']['key']
    val = event['queryStringParameters']['value']

    # base64 sanitizes the input, kind of
    key = encode_to_base64(key)
    val = encode_to_base64(val)

    insert_key_value(key, val)

    return {
        'statusCode': 200,
        'body': json.dumps('File created successfully.')
    }


#conn.close() # TODO: Is there a place for Lambda teardown so we can be nice?
