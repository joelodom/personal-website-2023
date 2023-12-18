#
# AWS Lambda function to receive an API request, pull the most recent
# sensor data from MongoDB, and return that.
#
# Endpoint: https://gl3eypcm00.execute-api.us-east-1.amazonaws.com/default/pull-sensor-data
#

import json
import http.client
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

MONGO_DB_API_KEY = "mongo-joel-api-key2"
MONGO_DB_API_KEY_REGION = "us-east-1"
KEY_NAME = "mongodb-api-key"

MONGO_DATASOURCE = "joelodom"
MONGO_DATABASE = "sensor-database"
MONGO_COLLECTION = "sensor-collection"

API_HOST = "us-east-2.aws.data.mongodb-api.com"
API_ENDPOINT = "/app/data-mjzzu/endpoint/data/v1/action/find"

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
    "api-key": mongo_api_key
}


def fetch_most_recent_document(): # from my MongoDB collection
    query = {
        "dataSource": MONGO_DATASOURCE,
        "database": MONGO_DATABASE,
        "collection": MONGO_COLLECTION,
        "sort": {"_id": -1},  # Sorting by _id in descending order
        "limit": 1
    }

    conn = http.client.HTTPSConnection(API_HOST)
    conn.request("POST", API_ENDPOINT, headers=HEADERS, body=json.dumps(query))

    response = conn.getresponse()
    data = response.read()
    conn.close()

    response_data = data.decode()
    if response.status == 200:
        print("Sucessfully fetched document.")
        document = json.loads(data)
        return document
    else:
        print("Failed to fetch document.")
        print("Status Code: " + str(response.status))
        print("Response: " + str(response_data))
    
    return None

def lambda_handler(event, context):
    data = fetch_most_recent_document()

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(data)
    }

    return response
