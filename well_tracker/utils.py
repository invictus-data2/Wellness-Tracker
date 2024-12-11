import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet():
    """Authorize and return the Google Sheets client."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Service account credentials
    credentials_json = {
        "type": "service_account",
        "project_id": "driven-terra-422205-u3",
        "private_key_id": "0d9e401e37 85c20b354033e5f6bbaf4b8b36353e",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDIXGHiGxfwMCFZ\n5QG9HnEbA+SgXn7tDj9aQYNMjIfedo+8BP4JuaEPJTxm9IvQchzgVfMtceyMGjeW\nQm8N0a2Sze+z/CDBW7q6iaNhobp8Gtp4kFsN4bVUgsIUdL7Xplc58Uzpjbt/TQ5H\nYeYE60wEsz9uC/MugZvTs5mDaQDTP3bDCVfU7U/e+zX1kgffwbVSNwQglODRsHCp\nOLgr9FupN7qckEjDcvhHOIDMRzPPHWEX+y8//3M+d7Jn1xpH6Nx7IhvjhMySK3lI\n5N+g+buVFCgfYmiAbk/UO1BFJcZhTrHg/X3k8ild4GZd1hq0f2z6/5sDynHTG14t\nyFSrRApRAgMBAAECggEAAfj7T/ICV1MjwrJBDD1GJyFhdaCDNPJ9hIRL72g4kHIF\nRAaB4/30M2yG+yeeT2+cnkd2yxtpsY752jyHNAn1p9kgv8wbVR3JFBFLDtORklYc\ndL6/Fr8e6APC4Z6tEeDl7A7k5J9PmZcjZhKDcuS6Jhd5ryvJ1iBgwux6S2/pUvIy\n3r5eLzdsaM2IARmcQLTI/K36RCeZGd0OGcbB3aT2kIXdc3+9TCjjGuSbYqfuwnxC\neppRXS7jjalAfeGzCLOr9w5LaSFAeGFiIfFJPoS3JmM1mD1yFzgYQXyw33S2C8yC\ncWUp7kOGHCIHej4ZGOVogt4Ell9kCcKsuU7xpgcoPQKBgQDzwfRqoMku4+Oy1SlM\nrhnKSRA4BVp8rhXkQ2iYLc+0FzAffb6u4UpdgeeL7ShRnLSb6sU7KbJGTy9kPJGU\nYZO0UkxrHn6IqmKhN523t0gYlQg3oUJciB1Sl1zlzxM/HW8IbDssgQoId4ujal6k\n1/2crMPgIedckzNSaq+Sp2S4zwKBgQDSbHdDmSmcjHZ1hLj1LArKI/gWxwk5MZrT\nv+PtwM0QQVEEbTbEpDwHcE2KK50cC+pkus2phHUAGkxYNiD3WM4gEV3nT3PBCBGO\nfji1z5ybjZemphgRhoES1DBQkb8Nm/+/crX6Jz39U8hJK1uvN8hGm5zM7zWUMp5d\nU1drWw+S3wKBgFzAG2mLPqIJ8rU0aN+Vi5iuDm7SkqjIcOoHQEBPhi3neNcyuKDA\ndtR3vow+tE3Bi/Ob9GpbpkscjFLevSIxsss1WYCU/N6xvo/LosaqBdPcuWC5io+8\n9zNbBu0myxMD9yDEVgvMGe441rhanCKrUQQRtQKOxAM0u52LnLz31tp/AoGAD0Eb\nuEPPN3EbWVOg0O07bwIChywwp/vHnJgpnt++PfJuPCLquICrdWKXzG9y+UiH2nuM\nU0Ct9q7xX+e0phnC/6Iiq5Uf8Bt0ol7WH6AIW2J9XvBliEe27bWCNyUJs6Pee3OG\na7cSkF3VhDBneiFSHIRFbrncqXyt7FgRW1ADpgMCgYEApzjwXJ2Luph0eL2LTF4j\nqjC4GpyV9nxA8ULtxIC5HblUrzt46SHp7jex781seY9uSS+1qvcMD/rUG6CGLKQb\nwC2x/9qX6qaxV+cRdYO0RfkxYei/rcEzWcoHdXYlYpQkVuwguvyjOU6rSGcbZSCc\n1DzILAUGtiDefe61ngmCloY=\n-----END PRIVATE KEY-----\n",
        "client_email": "chatterjee-20@driven-terra-422205-u3.iam.gserviceaccount.com",
        "client_id": "105464373381649806312",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/chatterjee-20%40driven-terra-422205-u3.iam.gserviceaccount.com",
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
