import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from . import build_sheet


class Google_Sheets():
    def __init__(self, spreadsheet_id, range_start, range_end):
        self.spreadsheet_id = spreadsheet_id
        self.range_start = range_start
        self.range_end = range_end
        self.sheet_range = range_start + ':' + range_end
        self.houses_info = {}

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

        response_coord = result.get("values", ())
        return response_coord

    def build_houses_coordinates(self, houses):
        alphabets_in_capital = []
        for i in range(65, 91):
            alphabets_in_capital.append(chr(i))

        for i in range(65, 91):
            alphabets_in_capital.append(chr(65) + chr(i))

        coord = 14
        offest = 3
        for i, house in enumerate(houses):
            self.houses_info[house[0]] = {
                "users_col": alphabets_in_capital[i],
                "points_col": alphabets_in_capital[i+1],
                "starting_row": coord
            }
            alphabets_in_capital = alphabets_in_capital[offest - 1::]

    def add_to_sheet(self, username, house_coordinates, points) -> int:
        if house_coordinates is None:
            raise ValueError

        service = self.service
        spreadsheet_id = self.spreadsheet_id

        house_range = f"{house_coordinates['house_coord']['users_col']}{house_coordinates['house_coord']['starting_row'] + 1}:{house_coordinates['house_coord']['points_col']}2000"
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=house_range, majorDimension="ROWS").execute()

        users = result.get('values', [])
        point_sum = 0
        found = False
        for user in users:
            if user[0] == username:
                found = True
                point_sum = int(user[1]) + points
                user[1] = point_sum

                break

        if not found:
            raise ValueError

        users = sorted(users, reverse=True, key=lambda x: int(x[1]))

        build_sheet.build_house(self.service, users,
                                self.spreadsheet_id, house_range)
        return point_sum

    def find_user_house(self, roles):
        current_houses = self.houses_info

        for role in roles:
            if role.name in current_houses:
                return {"house_name": role.name, "house_coord": current_houses[role.name]}

        return None
