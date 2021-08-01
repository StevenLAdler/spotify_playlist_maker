from __future__ import print_function
import os.path
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class DataRetriever:
    def __init__(self):
        self.__RESULTS = None
        self.__CREDS   = None
        
    def setResults(self, res):
        self.__RESULTS = res

    def setCreds(self, creds):
        self.__CREDS = creds
        
    # @property
    def getResults(self):
        return self.__RESULTS
    
    # @property
    def getCreds(self):
        return self.__CREDS

    def fetchCreds(self, config):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', config.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', config.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                    
            self.setCreds(creds)
    
    def fetchResults(self, config):
        service = build('sheets', 'v4', credentials=self.getCreds())

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=config.ssid,
                                    range=config.range).execute()
        values = result.get('values', [])
        
        self.setResults(values)
        
class Config:
    def __init__(self, config_path):
        self.__CONFIG = {}
        self.__CONFIG_PATH = config_path
    
    def setConfig(self):
        with open(self.__CONFIG_PATH) as config_file:
            self.__CONFIG = json.load(config_file)
        config_file.close()

    @property
    def ssid(self):
        if self.__CONFIG:
            return self.__CONFIG['SHEETS']['SPREADSHEET_ID']

    @property
    def scopes(self):
        if self.__CONFIG:
            return self.__CONFIG['SHEETS']['SCOPES']

    @property
    def range(self):
        if self.__CONFIG:
            return self.__CONFIG['SHEETS']['RANGE_NAME']

    @property
    def client_id(self):
        if self.__CONFIG:
            return self.__CONFIG['SPOTIFY']['CLIENT_ID']

    @property
    def client_secret(self):
        if self.__CONFIG:
            return self.__CONFIG['SPOTIFY']['CLIENT_SECRET']

    @property
    def username(self):
        if self.__CONFIG:
            return self.__CONFIG['SPOTIFY']['USERNAME']

    @property
    def pl_format(self):
        if self.__CONFIG:
            return self.__CONFIG['SPOTIFY']['PL_FORMAT']

    @property
    def pl_desc(self):
        if self.__CONFIG:
            return self.__CONFIG['SPOTIFY']['PL_DESC']
