import os

from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

from otter_bot.sheet.validate import validate_credentials
from otter_bot.functions.helper_functions import insert_data

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
    

    def get_allowed_companies_info(self) -> list[list[str]]:
        """
        Get information from the 'Allowed Companies' sheet.
        Returns a list with the information in the sheet.
        """
        try:
            # Build the service and make the API request
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.sheet_id, range='Allowed Companies').execute()
            values = result.get('values', [])

            return values

        except HttpError as err:
            print(err)

        return []

    
    def insert_apply_data(self, user: str, company: str) -> str:
        """
        Insert application data into the Google SpreadSheet (Apply column).
        """
        response = insert_data(user, company, self.creds, self.sheet_id, from_apply=True)
        return response
    

    def insert_oa_data(self, user: str, company: str) -> bool:
        """
        Insert online assessment data into the Google SpreadSheet (Online Assessment column).
        """
        response = insert_data(user, company, self.creds, self.sheet_id, 3, 'D')
        return response


    def insert_phone_data(self, user: str, company: str) -> None:
        """
        Insert phone interview data into the Google SpreadSheet (Phone column).
        """
        response = insert_data(user, company, self.creds, self.sheet_id, 4, 'E')
        return response

        
    def insert_interview_data(self, user: str, company: str) -> None:
        """
        Insert interview data into the Google SpreadSheet (Interview column).
        """
        response = insert_data(user, company, self.creds, self.sheet_id, 5, 'F')
        return response
        

    def insert_finalround_data(self, user: str, company: str) -> None:
        """
        Insert final round Interview data into the Google SpreadSheet (Final Round column).
        """
        response = insert_data(user, company, self.creds, self.sheet_id, 6, 'G')
        return response                     


    def insert_offer_data(self, user: str, company: str) -> None:
        """
        Insert offer data into the Google SpreadSheet (Offer column).
        """
        response = insert_data(user, company, self.creds, self.sheet_id, 7, 'H')
        return response


    def insert_rejection_data(self, user: str, company: str) -> None:
        """
        Insert rejection data into the Google SpreadSheet (Rejection column).
        """
        response = insert_data(user, company, self.creds, self.sheet_id, 3, 'I')
        return response
    
