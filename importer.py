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

def 