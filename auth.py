
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/calendar',
    'https://mail.google.com/'
]

TOKEN_FILE = "token.pkl"
CREDENTIALS_FILE = "client_GCP.json"  


def authenticate():
    """
    Handles Google OAuth authentication.
    If successful, returns True.
    If fails, returns False.
    """
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)


    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print("❌ Token refresh failed:", e)
                creds = None
        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print("❌ Authentication failed:", e)
                return False

        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)


    try:
        drive_service = build('drive', 'v3', credentials=creds)
        results = drive_service.files().list(pageSize=3).execute()
        files = results.get('files', [])
        if files:
            print("✅ Authentication successful. Example files:")
            for f in files:
                print("  -", f['name'])
        else:
            print("✅ Authentication successful, but no files found.")
        return True
    except Exception as e:
        print("❌ API test failed:", e)
        return False


if __name__ == "__main__":
    if authenticate():
        print(">>> SUCCESS")
    else:
        print(">>> FAIL")
