import json
import boto3
import os
import logging

#
# TODO: Don't use the same bucket as the website content
#       (For demo only)
#

BUCKET = 'joelodom'
FOLDER = 'received-data'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    logger.info("Event: " + json.dumps(event))
    
    bucket_name = BUCKET
    key = event['queryStringParameters']['key']
    value = event['queryStringParameters']['value']

    key = FOLDER + '/' + key
        
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
