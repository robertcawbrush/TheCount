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

        response_coord = result.get("values", [])
        self.build_houses_coordinates(response_coord[0])

    def build_houses_coordinates(self, houses):
        alphabets_in_capital = []
        for i in range(66, 91):
            alphabets_in_capital.append(chr(i))

        coord = 4
        blank = 0
        for i, house in enumerate(houses):
            if blank >= 2:
                break

            if house == '':
                blank += 1
                coord += 1
                continue
            else:
                blank = 0

           # if '' then increment blank continue
            self.houses_build[house] = (alphabets_in_capital[i], 4)
            coord += 1

    def add_to_sheet(self, username, house_role, points):
        service = self.service
        spreadsheet_id = self.spreadsheet_id

        make_range = f'{house_role[0]}{house_role[1]+1}:{house_role[0]}2000'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=make_range).execute()

        # iterate through col until found name then grab cell next to
        cols = result.get('values', [])
        start = house_role[1] + 1

        for col in cols:
            if col[0] == username:
                break
            start += 1

        next_range = f'{chr(ord(house_role[0]) + 1)}{start}'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=next_range).execute()
        
        if 'values' in result:
            user_points = result.get('values', [])[0][0]
        else:
            user_points = '0'

        user_points += ' + ' + str(points)
        if user_points[0] != '=':
            user_points = '=' + user_points

        values = [
            [
                user_points
            ],
        ]
        body = {
            'values': values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=next_range,
            valueInputOption='USER_ENTERED', body=body).execute()

        updated_cells = result.get('updatedCells')
        print('{0} cells updated.'.format(updated_cells))

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
            if role.name in current_houses:
                return current_houses[role.name]

        return None
