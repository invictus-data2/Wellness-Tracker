import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

def get_google_sheet():
    """Authorize and return the Google Sheets client."""
    # Define the scope required to access Google Sheets and Drive
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    # Retrieve the path of the credentials file from the environment variable
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_XYZ")

    if credentials_path:
        try:
            # Open the credentials file and load it as a JSON
            with open(credentials_path, 'r') as file:
                credentials_json = json.load(file)

            # Ensure the credentials_json is not None
            if credentials_json:
                # Create credentials using the loaded JSON
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
                print("Credentials loaded successfully.")
                
                # Authorize the Google Sheets client
                client = gspread.authorize(credentials)
                return client
            else:
                print("Error: Credentials file is empty or invalid.")
                return None
        except FileNotFoundError:
            print(f"Error: The file at path {credentials_path} was not found.")
            return None
        except json.JSONDecodeError:
            print("Error: Failed to decode the credentials file. It may not be in valid JSON format.")
            return None
    else:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
        return None
    
def get_client_names():
    """Fetch client names from Google Sheets."""
    try:
        google_sheet = get_google_sheet()
        client_sheet = google_sheet.open("Wellness").worksheet("client_Directory")
        client_names = client_sheet.col_values(1)[1:]  # Skip header
        return client_names
    except Exception as e:
        print(f"Error fetching client names: {e}")
        return []


def get_coach_names():
    """Fetch coach names from Google Sheets."""
    try:
        google_sheet = get_google_sheet()
        coach_sheet = google_sheet.open("Wellness").worksheet("coach_Directory")
        coach_names = coach_sheet.col_values(1)[1:]  # Skip header
        return coach_names
    except Exception as e:
        print(f"Error fetching coach names: {e}")
        return []
