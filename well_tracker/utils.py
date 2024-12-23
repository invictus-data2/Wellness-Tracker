import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

def get_google_sheet():
    """Authorize and return the Google Sheets client."""
    scope = [  'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']

    # Service account credentials
#     credentials_json = {
#  "type": "service_account",
#   "project_id": "double-venture-441113-m0",
#   "private_key_id": "980b561ca90cd408e34549d0c26b6a863a1b46c0",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDwvLvGKQYu5Ei\njYOUtYzkwm7c0rrkTNrVWkZkEQrE5nmKMzTy4R6c+b+2uIXI/t+dljD23u0OeAw4\nEDCxjSQKBc9prto7sKbse9IbfLIhmD+wZ2mJHwwpuSfqBWnStdnQpRkJhQPwIlqh\n6gZGuBekao/HUpidZ9FIc4OAFWZzoOjpzOg0iY6i5EY14lr9/UK6BePA9jIBlAzN\nhIKBCYTiYDCCM/7yypSOVg72dG/4arOi/dz0oWcrV164gG76JffzGafqmqKayIBe\niPLDtw/j+Z3WVADWfk3jncoQI3ge4D8eQVvinNj7LNmRdFVoo0rKmFXPa91dA6lL\nnEkKNQ4tAgMBAAECggEALR2P7s4DPYb2vRuXlE1d/feYZLB1LXnP4iU2vUeXL4c9\nQf4oqQP8UemWBxaSEJ86ql8LhE2enPvKNx52FmlEgcHSihTnyyNcaPplUvvjMq5b\nmTxP/G/JFhGLsxmRyKOr4fO2qDS9UlmcgR3F2gUBv9zmK2Xr8bTULOogR4PHE4T9\n1sUepGPffd22sbViLAhF6MntizsTxHOXeafN5hV05R0ClStL89pZh5Ii/TVCewuz\nz/QhKyZ8k+3dSD/m0PVMQ2oGa2cZpExKu09UQpD0v9q5fyI8DKJoBggFOVr/EuTS\n5EB0H29pOXCjcsWiAAka1TlNA0bghByziWDDlrwFAQKBgQDvQU5PsaaUTOMsn9n+\nOFlrfmOoTL2XVknH5pqhQlyN4v+u9MkvvPt/DZqC0da1nl/wMQnRhlbVv3pa7WDV\n5lYp0Bl3uhxnJbgfMEfnj6PB9KT9jrXOlEcW2UNPGTywBvvgLcQFy7567WYh5gSw\nyKS/lq4wtKbkBwxRbPwsI38RLQKBgQDRdmAwoMbV2Sa7HHp+UP60ExSqOWz7cP/J\nPkQn5oLp5PvswBOu2v0dzQtrrdSNSmydbMa3LuOo8cCLbwAJeLFdUVTT+0NYTX4P\nE245vFHcBEfPhBgGlzWZD2DRv2asvSJC2C2iOmK1yV7jGqcVk89khdmkAgVY4UQB\n2qmjmBoRAQKBgAGf4uU9opDtOLmr2DIWtdy5/fk9lCf76QJXeYNQzQoVmYDZnqgZ\nU2fYcs0imZ+gFKyv2I44qExJQY5ugDLTnpAoHpQmilzU77wees6Ctizx+VDTcD6X\n2Se5j/Bwjm3vjjRGe0dCy+dPx1rBkhSVODEo18Py5hM0TQwcflXaY9l9AoGBAL3v\n/eGaqTMZqolZlaodgBmCg+aoFC8dlJTEJcGYwXWe8uMIedDBO21eldCa3HcS2dMW\n5EsP9dko/1Rw3zO3gf4A1k8zNSpJetno4LbyEbjVGNkQC0lOrIeS7lTEnzJcf0jm\nBtto3kHBzI1bic+DLTkWNvkF7Btgie60fcefEWQBAoGBAOHUsbkjPRdQKIB4KFTW\nERm9yx70BNp9C0YmsXS+5/SvhWG7jaM+TAAYXnQMAhh23QPXeao2iImOZXve8bt1\n1BhHNMArn3ZBSNV7ahBBe+wHYPxpzU0Gm871mtxVHubDWP+lifB387ce1uUdf1ZS\nd5rp9tzo6DmKoKzXlX8emly8\n-----END PRIVATE KEY-----\n",
#   "client_email": "xyz-534@double-venture-441113-m0.iam.gserviceaccount.com",
#   "client_id": "108959544896634970463",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/xyz-534%40double-venture-441113-m0.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
#     }
    # Retrieve the path of the credentials file from the environment variable
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_XYZ")

    if credentials_path:
        with open(credentials_path, 'r') as file:
            credentials_json = json.load(file)
        
        # Ensure the credentials_json is not None
        if credentials_json:
            scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']  # Adjust the scope if needed
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
            print("Credentials loaded successfully.")
        else:
            print("Error: Unable to load credentials from the file.")
    else:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")


        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
        return gspread.authorize(credentials)


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
