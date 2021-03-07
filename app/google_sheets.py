import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json


class Google_Sheets():
    def __init__(self, spreadsheet_id, sheet_range, current_sheet=None):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_range = sheet_range
        self.current_sheet = current_sheet if current_sheet is not None else 0

        self.connect_to_sheet()
        self.current_houses = self.get_current_house_roles()

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def connect_to_sheet(self):
        print('connecting to sheet')
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)
        print('connected to google sheets')

    def add_to_sheet(self, username, user_roles, points):
        service = self.service
        spreadsheet_id = self.spreadsheet_id
        sheet_range = self.sheet_range
        print('adding to sheet')
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=sheet_range).execute()
        print(f'rows? {result.get("values", [])}')

    def subtract_from_sheet(self, username):
        ...

    def get_current_house_roles(self):
        service = self.service
        spreadsheet_id = self.spreadsheet_id
        sheet_range = 'H5:H'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=sheet_range).execute()
        houses = result.get("values", [])
        return tuple([house[0] for house in houses])

    def find_user_house(self, roles):
        current_houses = self.current_houses
        for role in roles:
            if role.name in current_houses:
                return role 

        return None 