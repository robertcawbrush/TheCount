import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
 

class Google_Sheets():
    def __init__(self, creds, document_id, sheet_range):
        self.creds = creds
        self.document_id= document_id
        self.sheet_range = sheet_range
        self.connect_to_sheet()
    
    def connect_to_sheet(self):
        print('connecting to sheet')
        ...