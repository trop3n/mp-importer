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
    
