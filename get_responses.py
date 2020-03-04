import pickle
import os.path

import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class DataRetriever:
    def __init__(self):
        self.__RESULTS = None
        self.__CREDS   = None
        self.__SCOPES = []
        self.__SPREADSHEET_ID = ""
        self.__RANGE_NAME = ""
        
    def setSpreadsheetID(self, ssid):
        self.__SPREADSHEET_ID = ssid
        
    def setScopes(self, scopes):
        self.__SCOPES = scopes
        
    def setRange(self, range_name):
        self.__RANGE_NAME = range_name
    
    def getSpreadsheetID(self):
        return self.__SPREADSHEET_ID
        
    def getScopes(self):
        return self.__SCOPES
        
    def getRange(self):
        return self.__RANGE_NAME
        
    def setResults(self, res):
        self.__RESULTS = res
        
    def getResults(self):
        return self.__RESULTS
        
    def setCreds(self, creds):
        self.__CREDS = creds
        
    def getCreds(self):
        return self.__CREDS
            
    def setClassVars(self):
        with open('config.json') as config_file:
            data = json.load(config_file)
        config_file.close()
        self.setSpreadsheetID(data['SHEETS']['SPREADSHEET_ID'])
        self.setScopes(data['SHEETS']['SCOPES'])
        self.setRange(data['SHEETS']['RANGE_NAME'])
        
    def fetchCreds(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.getScopes())
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                
        self.setCreds(creds)
    
    def fetchResults(self):
        service = build('sheets', 'v4', credentials=self.getCreds())

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.getSpreadsheetID(),
                                    range=self.getRange()).execute()
        values = result.get('values', [])
        
        self.setResults(values)
        