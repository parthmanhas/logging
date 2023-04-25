from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

with open('google_sheets_creds.txt', 'r') as f:
    SPREADSHEET_ID = f.readline().split('=')[1].strip()
    RANGE_NAME = f.readline().split('=')[1].strip()

range_name = RANGE_NAME

def main(row_data):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    if len(row_data) == 0:
        raise Exception('Empty row data!')
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        request_body = {
            "range": range_name,
            "majorDimension": "ROWS",
            "values": [row_data]
        }

        
        request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                                         range=range_name,
                                                         valueInputOption='USER_ENTERED',
                                                         insertDataOption='INSERT_ROWS',
                                                         body=request_body)
        
        response = request.execute()

        print(response)

    except HttpError as err:
        print(err)
