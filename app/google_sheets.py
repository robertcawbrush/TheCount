import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Google_Sheets():
    def __init__(self, document_id, sheet_range, current_sheet=None):
        self.document_id = document_id
        self.sheet_range = sheet_range
        self.current_sheet = current_sheet if current_sheet is not None else 0
        self.connect_to_sheet()

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def connect_to_sheet(self):
        print('connecting to sheet')
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def add_to_sheet(self, username, points):
        print('adding to sheet')
        self.service

    def subtract_from_sheet(self, username):
        ...
