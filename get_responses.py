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

    @property
    def results(self):
        return self.__RESULTS
    
    @property
    def creds(self):
        return self.__CREDS   

    @results.setter
    def results(self, results):
        self.__RESULTS = results

    @creds.setter
    def creds(self, creds):
        self.__CREDS = creds

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
                    
        self.creds = creds
    
    def fetchResults(self, config):
        service = build('sheets', 'v4', credentials=self.creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=config.ssid,
                                    range=config.range).execute()
        values = result.get('values', [])
        
        self.results = values
        
        
class Config:
    def __init__(self, config_path):
        self.config = config_path

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config_path):
        with open(config_path) as config_file:
            self._config = json.load(config_file)
        config_file.close()

    @property
    def ssid(self):
        if self.config:
            return self.config['SHEETS']['SPREADSHEET_ID']

    @property
    def scopes(self):
        if self.config:
            return self.config['SHEETS']['SCOPES']

    @property
    def range(self):
        if self.config:
            return self.config['SHEETS']['RANGE_NAME']

    @property
    def client_id(self):
        if self.config:
            return self.config['SPOTIFY']['CLIENT_ID']

    @property
    def client_secret(self):
        if self.config:
            return self.config['SPOTIFY']['CLIENT_SECRET']

    @property
    def username(self):
        if self.config:
            return self.config['SPOTIFY']['USERNAME']

    @property
    def pl_format(self):
        if self.config:
            return self.config['SPOTIFY']['PL_FORMAT']

    @property
    def pl_desc(self):
        if self.config:
            return self.config['SPOTIFY']['PL_DESC']
