#
# Scratchpad to figure out how to make it work
#

import http.client
import json

MONGO_DATASOURCE = "joelodom"
MONGO_DATABASE = "sensor-database"
MONGO_COLLECTION = "sensor-collection"

API_HOST = "us-east-2.aws.data.mongodb-api.com"
API_ENDPOINT = "/app/data-mjzzu/endpoint/data/v1/action/find"
API_KEY = ""

HEADERS = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

def fetch_most_recent_document():
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

def main():
    latest_document = fetch_most_recent_document()
    if latest_document:
        print("Most Recent Document:", latest_document)
    else:
        print("No document found.")

if __name__ == "__main__":
    main()
