import json
import boto3
import os
import logging
import base64

#
# TODO: Don't use the same bucket as the website content
#       (For demo only)
#

BUCKET = 'joelodom'
FOLDER = 'received-data'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

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
