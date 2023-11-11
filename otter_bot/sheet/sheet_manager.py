import os

from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

from otter_bot.sheet.validate import validate_credentials

load_dotenv()

class SheetManager():
    def __init__(self, sheet_id : str = os.environ['SHEET_ID']) -> None :
        self.sheet_id : str = sheet_id
        self.creds : Credentials = validate_credentials()
    
    def query(self, query_range : str) -> list[list[str]]:
        """
        Make a request to the spreadsheet API.
        Returns a list with the information inside of the query_range argument.
        """
        try:
            service = build('sheets', 'v4', credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.sheet_id,
                                        range=query_range).execute()
            values = result.get('values', [])
            return values    
            
        except HttpError as err:
            print(err)
        return []
