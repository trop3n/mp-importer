Ministry Platform Bulk Importer

This Python script provides a simple way to bulk-import data into a Ministry Platform table from a CSV file. It uses a .env file to securely manage your API credentials.
Prerequisites

    Python 3.6+: Make sure you have Python installed on your system.

    Ministry Platform API Credentials: You will need a Client ID and Client Secret with appropriate permissions to create records. Contact your Ministry Platform administrator to obtain these.

    Table and Field Names: You must know the exact name of the table (e.g., Contacts) and the field names (e.g., First_Name, Email_Address) you are importing into.

Setup

    Download Files:
    Save all the files (mp_bulk_importer.py, data_to_import.csv, etc.) to a folder on your computer.

    Install Required Libraries:
    This script uses requests, pandas, and python-dotenv. You can install them using pip. Open your terminal or command prompt and run:

    pip install requests pandas python-dotenv

    Create and Configure .env file:

        In the same folder as the script, create a file named .env.

        Open the .env file and add your configuration information like so:

    # Ministry Platform API Credentials
    # Replace the placeholder values with your actual credentials.
    MP_DOMAIN="my.ministryplatform.com"
    CLIENT_ID="YOUR_CLIENT_ID"
    CLIENT_SECRET="YOUR_CLIENT_SECRET"

        Important: This file contains sensitive information. Make sure to add .env to your .gitignore file if you are using version control.

    Configure Script Settings (Optional):

        Open mp_bulk_importer.py.

        You can change the TARGET_TABLE and CSV_FILE_PATH variables if needed.

Usage

    Prepare Your Data:

        Open the data_to_import.csv file (or create your own).

        Crucially, the column headers in the CSV file must exactly match the field names in your Ministry Platform table. For example, if Ministry Platform expects First_Name, your CSV column header must be First_Name, not First Name or firstName.

        Fill the CSV with the data you want to import. Each row will become a new record in Ministry Platform.

    Run the Importer:

        Open your terminal or command prompt.

        Navigate to the folder where you saved the files.

        Run the script using the following command:

    python mp_bulk_importer.py

    Check the Output:

        The script will print its progress to the terminal, including authentication status and the final API response.

        If the import is successful, you will see a "Bulk import successful!" message along with the data returned by the server.

        If there are errors, the script will print the error message from the server, which can help you troubleshoot issues with your data or configuration.

Important Notes

    Test First: Always test this script on a development or staging instance of Ministry Platform before running it on your live production data.

    Data Validation: This script no longer performs any data validation. Ensure the data in your CSV file is clean and in the correct format for the corresponding fields in Ministry Platform.

    Error Handling: The script includes basic error handling, but an error from the API usually means there's an issue with the data you're sending. Carefully check the API response in the terminal for clues.