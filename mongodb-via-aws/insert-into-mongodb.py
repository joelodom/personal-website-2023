#
# This is just a sample to tweak what I need to do before I move it
# into the lambda function.
#

import http.client
import json

API_HOST = "us-east-2.aws.data.mongodb-api.com"
API_ENDPOINT = "/app/data-mjzzu/endpoint/data/v1/action/insertOne"

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Request-Headers": "*",
    "api-key": ""
}

conn = http.client.HTTPSConnection(API_HOST)

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

    conn.request("POST", API_ENDPOINT, body=json.dumps(payload), headers=HEADERS)
    response = conn.getresponse()

    response_data = response.read().decode()
    if response.status == 201:
        print("Document inserted successfully.")
        print("Response:", response_data)
    else:
        print("Failed to insert document.")
        print("Status Code:", response.status)
        print("Response:", response_data)

insert_key_value("joel", "31415")

#conn.close()
