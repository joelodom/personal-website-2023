#
# This is just a sample to tweak what I need to do before I move it
# into the lambda function.
#

import requests
import json

#API_URL = "https://us-east-2.aws.data.mongodb-api.com/app/data-mjzzu/endpoint/data/v1"
API_URL = "https://us-east-2.aws.data.mongodb-api.com/app/data-mjzzu/endpoint/data/v1/action/insertOne"

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Request-Headers": "*",
    "api-key": "PULL FROM SECRET MGR"
}

def insert_key_value(key, value):
    payload = {
        "dataSource": "joelodom",
        "database": "sensor-database",
        "collection": "sensor-collection",
        "document": {
            "key": key,
            "value": value,
        }
    }

    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))

    if response.status_code == 201:
        pass
        #print("Document inserted successfully.")
        #print("Response:", response.json())
    else:
        pass
        #print("Failed to insert document.")
        #print("Status Code:", response.status_code)
        #print("Response:", response.text)

insert_key_value("key123", "value123")
