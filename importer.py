import requests
import json
import pandas as pd
import sys
import os
from dotenv import load_dotenv

# --- Configuration ---
# load environment variables from dotenv file
load_dotenv()

# Important: Create an .env file in the same directory as this script
# and add your configuration values there.
# Example .env file:
# MP_DOMAIN="my.ministryplatform.com"
# CLIENT_ID="YOUR_CLIENT_ID"
# CLIENT_SECRET="YOUR_CLIENT_SECRET"

MP_DOMAIN = os.getenv("MP_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# The name of the table you want to import data into (e.g., "Contacts", "Participants")
TARGET_TABLE = "Contacts"

# Path to .csv file
CSV_FILE_PATH = "sample-data.csv"
# --- End of Config ---


def get_auth_token():
    """
    Authenticates with the Ministry Platform API to get an OAuth access token.
    """
    print("Attempting to get authentication token...")
    auth_url = f"https://{MP_DOMAIN}/api/oauth/connect/token"
    payload = {
        "grant_type": "client_credentials",
        "scope": "http://www.thinkministry.com/dataplatform/scopes/all",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.port(auth_url, data=payload, headers=headers)
        response.raise_for_status() # raises an HTTPError for bad responses (4xx or 5xx)

        token_data = response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            print("Error: 'access_token' not found in the response.")
            sys.exit(1)

        print("Successfully obtained authentication token.")
        return access_token

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred during authentication: {http_err}")
        print(f"Response content: {response.content.decode()}")
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred during authentication: {req_err}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response from token endpoint.")
        print(f"Response was: {response.text}")

    sys.exit(1)

def bulk_create_records(token, records):
    """
    Sends a list of records to the Ministry Platform API for creation.

    Args:
        token(str): The OAuth access token.
        records(list): A list of dictionaries, where each dictionary represents a record to create.
    """
    if not records:
        print("No records to import.")
        return

    print(f"Preparing to import {len(records)} records into the '{TARGET_TABLE}' table...")
    api_url = f"https://{MP_DOMAIN}/api/tables/{TARGET_TABLE}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        # The API expects a JSON array of objects
        response = requests.post(api_url, data=json.dumps(records), headers=headers)
        response.raise_for_status()

        print("Bulk import successful!")
        print("API Response:")
        # Pretty print the JSON response
        print(json.dumps(response.json(), indent=2))

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred during bulk import: {http_err}")
        print("The server responded with an error. THis could be due to:")
        print("- Invalid data in your CSV (e.g., wrong data types, missing required fields).")
        print("- Incorrect table or field names in your configuration or CSV headers.")
        print(f"REsponse content: {response.content.decode()}")
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred during bulk import: {req_err}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response from bulk create endpoint.")
        print(f"Response was: {response.text}")

def main():
    """
    Main function to run the importer.
    """
    print("--- Ministry Platform Bulk Importer ---")

    # Basic validation
    if not all([MP_DOMAIN, CLIENT_ID, CLIENT_SECRET]):
        print("Error: One or more required environment variables (MP_DOMAIN, CLIENT_ID, CLIENT_SECRET) are missing.")
        print("Please create a .env file and add these variables.")
        return

    # 1. Read data from CSV
    try:
        print(f"Reading data from '{CSV_FILE_PATH}'...")
        df = pd.read_csv(CSV_FILE_PATH)
        # convert the DataFrame to a list of dictionaries, which matches the JSON format needed by the API
        records_to_import = df.to_dict('records')
    except FileNotFoundError:
        print(f"Error: the file '{CSV_FILE_PATH}' was not found.")
        print("Please make sure the CSV file is in the same directory as the script, or provide the full path.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

    # 2. Get authentication token
    auth_token = get_auth_token()

    # 3. Perform the bulk insert
    if auth_token:
        bulk_create_recrods(auth_token, records_to_import)

    print("--- Process Complete ---")

if __name__ == "__main__":
    main()