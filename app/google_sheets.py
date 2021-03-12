import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Google_Sheets():
    def __init__(self, spreadsheet_id, sheet_range, current_sheet=0):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_range = sheet_range
        self.current_sheet = current_sheet 
        self.houses_build = {}
        try:
            self.connect_to_sheet()
            self.get_sheet_coordinates(self.spreadsheet_id, self.sheet_range)
            self.build_sheet()
        except ValueError as ve:
            print(f'{ve} incorrect or missing')


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

    def get_sheet_coordinates(self, spreadsheet_id, sheet_range):
        service = self.service

        if self.spreadsheet_id is None:
            raise ValueError

        result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=sheet_range).execute()

        self.build_houses_coordinates(result.get("values", [])[0])
    
    def build_houses_coordinates(self, houses):
        # 0 b4
        coord = 4
        blank = 0
        for house in houses:
            if blank >= 2:
                break
            
            if house == '':
                blank +=1
                coord += 1
                continue
            else:
                blank = 0

           # if '' then increment blank continue 
            self.houses_build[house] = f'B{coord}'
            coord += 1
        
    def build_sheet(self):
        # iterate over house_build and overwrite whats in House column
        ...

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

    def get_all_house_member_count(self):
        if len(self.current_houses_list) < 1:
            self.get_current_house_roles()

        service = self.service
        spreadsheet_id = self.spreadsheet_id
        num_of_houses = len(self.current_houses_list)
        sheet_range = f'I5:I{5 + num_of_houses}'

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=sheet_range).execute()
        houses = result.get("values", [])
        house_names = self.current_houses_list
        for i, house_count in enumerate(houses):
            self.current_houses[house_names[i]] = {'count': house_count[0]}

        return

    def find_user_house(self, roles):
        current_houses = self.houses_build

        for role in roles:
            if role in current_houses:
                return current_houses[role]

        return None
