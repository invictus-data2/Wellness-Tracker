import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet():
    """Authorize and return the Google Sheets client."""
    scope = [  'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']

    # Service account credentials
    credentials_json = {
    "type": "service_account",
    "project_id": "automation-422503",
    "private_key_id": "5dc333faf9c1b06fe534dd748fb1d87567f7cfa3",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCd1aYmqrNNJvqs\nsjtf6vmPXM8312sq+fGCdq2p90exXhkOMg+83exW0diz8UZ7IPOqw4mWpmYXPytB\naMSBzScRO9UaSy+KdzxiVtSsKupXulWstKQRrkfARCAPOA1a1s8h5PM/PpkvQZeY\n9RT7+un5N8q8s2s13kF+EP6wfE0VJHI7gGvOeRBZGas9cCgHKbIE0nUwhZnI14V7\nqtI4oujtdbPA/jtDqs7N/xephFCCuV5gBEsfw1Ju2XdP0btr1vquLhELrfUK6gWD\na4xKkMV8YO9GhoMfgwl2WExFhOufQSpv5xokzHSb7J/mlejecujAhO1MuERHCdXM\nn9N3aHxrAgMBAAECggEARJLR9MO+Ufto9sYbANHsqkpG53qK36mnMakRS6KZfeil\nlyLN7p82swPKFGfz2MQYyazZ5t+VxGzYBLuZgNGasySdMibPWWfzjsAt9z1QAlx9\nI6N6Ewp2twSCL0qJltl0NcQsoOI4GK11SWnVu6Koq/P++9wx7L4LE1Qb656duNyl\nZDZ6W1e67lZ4Y9Ef4vA/sKJaoU554UzuhmdVj8CAJGa7ZPT/XtzVkSYnqFuoLNBk\nRwwo+DAutsfcBbCq9R4ymD23LO1KJMTDEQMzJKXJ9czbRtxTrNUZRBDL5SJAZ4Nk\nu+6HLxf9xIaqlyE0zFsZfyGUKwSssS76xzfgUMBT/QKBgQDVDlo236mLk/MnAB00\n9NFqsXmMbLysfH/nomGxZe4ciCv+OcvpTA/jFDNInmsXrhM8uGReCRaQCWWU6fF6\nm+dXYHg+cK2KB20NsVa9mfaHHP4I2w23iAHBicRwEWeucSaWpWwSNnWxDF7ootfY\nt8sDf/C4lduepw/+bEB530N3HQKBgQC9peEMfUF+JK3Da4AvWZrWIwH+HdTY2ugl\nQaXXgbZAWwfRNrB0Mk3qQ9EPpre9IFQbgEk0frg907lwaE5pbPoupfTxhgtazqHK\nmnULLnKUZoI6VpASen06zhf537dSwE0BK5ewK6noYMQWN+0Dhv9zDIDhyDqk4UQF\nOAZYV+wDJwKBgEoXhqoEmAqRNgL/GCkdZmJrO7Do86gsV7KvFrhBkU/czyfG47HL\nIM9AbCE57lY61DfOjCDjmjQXAHuL681OwGHzi31zY/ZXZMZZQKgJDeGo5HMh8qA7\nrRioF2c9tkfE072Z435l8AHVIoBWeSfFqtUZvhYDD3AZ+wbokHeRe/3FAoGAWUlq\nrh2eowwTvyiynhhavKyYuJJE7qAJodjJgq/wJVZ2VLqh0uMIKd4p5GuCoAlDb/sy\n/AMZLQqsiM6i9CG5nBLIQpnwaJ1WMPQNXOlOSq4EbADrLbf7k58KTLtWLSCaYI2s\nieXUxbIhP7Cu5vU8+WaOmz5Q1eW0x5w76IXkeQsCgYEAtWv74A5+9w6nTptmltDg\n+t2BTChHPbNbIvfmcr34bhjt95JWuos40Xg/Tjqla6+1/JVC60uJpnnmlPKVIX4O\nfRaDEfX4VmcrlvDMH4FDTGMFUO18eas2CmymRtdHSXVFEycB8S+kV1mZrmWXh4fR\nfXhC5gEYwKpAauDjHdRYm/0=\n-----END PRIVATE KEY-----\n",
    "client_email": "dataadmin@automation-422503.iam.gserviceaccount.com",
    "client_id": "116524974662221993471",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dataadmin%40automation-422503.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }

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
