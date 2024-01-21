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
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()

            range_to_check = 'A:C'  
            response = sheet.values().get(spreadsheetId=self.sheet_id, range=range_to_check).execute()
            rows = response.get('values', [])

            #Check if user and company already exist
            for row in rows:
                if len(row) >= 2 and row[0] == user and row[1] == company:
                    return '1'


            # Data to be inserted
            values = [[user, company, '✅']]
            body = {'values': values}

            # Find the next available row
            next_row = len(rows) + 1
            range_to_insert = f"A{next_row}:C{next_row}"

            sheet.values().append(
                spreadsheetId=self.sheet_id,
                range=range_to_insert,
                valueInputOption='RAW',
                body=body).execute()
            return '2'
        
        except HttpError as err:
            print(err)
    
    def insert_oa_data(self, user: str, company: str) -> str:
        """
        Insert Online Assessment data into the Google SpreadSheet (Online Assessment column).
        """
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()

            range_to_check = 'A:D' 
            response = sheet.values().get(spreadsheetId=self.sheet_id, range=range_to_check).execute()
            rows = response.get('values', [])

            # Check if user and company already exist, if so just mark required column
            for index, row in enumerate(rows):
                if len(row) >= 2 and row[0] == user and row[1] == company:

                    arreglo = row

                    for i in range(4, len(row)):
                        if row[i] == "✅":
                            return
                        
                    

                    
                    if len(row) > 3 and row[3] == "✅":  
                        return '1'  
                    
                    
                    
                    elif len(row) > 3:
                        return '2'
                    
                    else:
                        range_to_update = f"D{index + 1}"
                        body = {'values': [['✅']]}
                        sheet.values().update(
                            spreadsheetId=self.sheet_id,
                            range=range_to_update,
                            valueInputOption='RAW',
                            body=body).execute()
                        return '3'
                    
                
            values = [[user, company, '-', '✅']]  
            body = {'values': values}
            next_row = len(rows) + 1
            range_to_insert = f"A{next_row}:D{next_row}"

            # Append a new row
            sheet.values().append(
            spreadsheetId=self.sheet_id,
            range=range_to_insert,
            valueInputOption='RAW',
            body=body).execute()
                    
            return '4'

        except HttpError as err:
            print(err)


    def insert_phone_data(self, user: str, company: str) -> None:
        """
        Insert data into the spreadsheet.
        """
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()

            # Check if user and company already exist
            range_to_check = 'A:E'
            response = sheet.values().get(spreadsheetId=self.sheet_id, range=range_to_check).execute()
            rows = response.get('values', [])
            for index, row in enumerate(rows):
                if len(row) >= 2 and row[0] == user and row[1] == company:

          
                    if len(row) > 4 and row[4] == '✅':  
                        return '1'  
                    
                    elif len(row) > 4:
                        return '2'
                    
                    else:
                        # Update only the Phone column
                        range_to_update = f"E{index + 1}"
                        body = {'values': [['✅']]}
                        sheet.values().update(
                            spreadsheetId=self.sheet_id,
                            range=range_to_update,
                            valueInputOption='RAW',
                            body=body).execute()
                        return '3'
                    
    
            values = [[user, company, '-', '-', '✅']]  
            body = {'values': values}
            next_row = len(rows) + 1
            range_to_insert = f"A{next_row}:E{next_row}"

            # Append a new row
            sheet.values().append(
                spreadsheetId=self.sheet_id,
                range=range_to_insert,
                valueInputOption='RAW',
                body=body).execute()
            
            return '4'

        except HttpError as err:
            print(err)
        
    def insert_interview_data(self, user: str, company: str) -> None:
        """
        Insert data into the spreadsheet.
        """
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()

            range_to_check = 'A:G'
            response = sheet.values().get(spreadsheetId=self.sheet_id, range=range_to_check).execute()
            rows = response.get('values', [])
            for index, row in enumerate(rows):
                if len(row) >= 2 and row[0] == user and row[1] == company:
              
                    if len(row) > 5 and row[5] == '✅':  
                        return '1' 
                    
                    elif len(row) > 5:
                        return '2'
                    
                    else:
                
                        range_to_update = f"F{index + 1}"
                        body = {'values': [['✅']]}
                        sheet.values().update(
                            spreadsheetId=self.sheet_id,
                            range=range_to_update,
                            valueInputOption='RAW',
                            body=body).execute()
                        return '3'
         
            values = [[user, company, '-', '-', '-','✅']]  
            body = {'values': values}
            next_row = len(rows) + 1
            range_to_insert = f"A{next_row}:F{next_row}"

            # Append a new row
            sheet.values().append(
                spreadsheetId=self.sheet_id,
                range=range_to_insert,
                valueInputOption='RAW',
                body=body).execute()
            
            return '4'

        except HttpError as err:
            print(err)
        

    def insert_finalround_data(self, user: str, company: str) -> None:
        """
        Insert data into the spreadsheet.
        """
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()

            # Check if user and company already exist
            range_to_check = 'A:G'
            response = sheet.values().get(spreadsheetId=self.sheet_id, range=range_to_check).execute()
            rows = response.get('values', [])
            for index, row in enumerate(rows):
                if len(row) >= 2 and row[0] == user and row[1] == company:
                    # Check if the command was already executed for this user and company
                    if (len(row) > 6 and row[7] == '🎉') or (len(row) > 5 and row[8] == '😭'):
                        return False  # Command already executed for this user and company
                    else:
                        # Update only the Interviews column
                        range_to_update = f"G{index + 1}"
                        body = {'values': [['✅']]}
                        sheet.values().update(
                            spreadsheetId=self.sheet_id,
                            range=range_to_update,
                            valueInputOption='RAW',
                            body=body).execute()
                        return True
                    
            for row in rows:
                if len(row) >= 2 and row[0] == user and row[1] == company and row[7] == "🎉":
                    return False
                
                else:
                    # Data to be inserted for new user and company
                    values = [[user, company, '-', '-', '-','-', '✅']]  # Empty string for the Online Assessment column
                    body = {'values': values}
                    next_row = len(rows) + 1
                    range_to_insert = f"A{next_row}:G{next_row}"

                    # Append a new row
                    sheet.values().append(
                        spreadsheetId=self.sheet_id,
                        range=range_to_insert,
                        valueInputOption='RAW',
                        body=body).execute()
                    
                    return True

        except HttpError as err:
            print(err)
                     


    def insert_offer_data(self, user: str, company: str) -> None:
        """
        Insert data into the spreadsheet.
        """
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()

            # Check if user and company already exist
            range_to_check = 'A:G'
            response = sheet.values().get(spreadsheetId=self.sheet_id, range=range_to_check).execute()
            rows = response.get('values', [])
            for index, row in enumerate(rows):
                if len(row) >= 2 and row[0] == user and row[1] == company:
                    # Check if the command was already executed for this user and company
                    if (len(row) > 6 and row[6] == '😭') or (len(row) > 5 and row[5] == '🎉'):
                        return False  # Command already executed for this user and company
                    else:
                        # Update only the Interviews column
                        range_to_update = f"F{index + 1}"
                        body = {'values': [['🎉']]}
                        sheet.values().update(
                            spreadsheetId=self.sheet_id,
                            range=range_to_update,
                            valueInputOption='RAW',
                            body=body).execute()
                        return True
                    
            for row in rows:
                if len(row) >= 2 and row[0] == user and row[1] == company and row[5] == "🎉":
                    return False
                
                else:
                    # Data to be inserted for new user and company
                    values = [[user, company, '', '', '','🎉']]  # Empty string for the Online Assessment column
                    body = {'values': values}
                    next_row = len(rows) + 1
                    range_to_insert = f"A{next_row}:F{next_row}"

                    # Append a new row
                    sheet.values().append(
                        spreadsheetId=self.sheet_id,
                        range=range_to_insert,
                        valueInputOption='RAW',
                        body=body).execute()
                    
                    return True

        except HttpError as err:
            print(err)


    def insert_rejection_data(self, user: str, company: str) -> None:
        """
        Insert data into the spreadsheet.
        """
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()

            # Check if user and company already exist
            range_to_check = 'A:G'
            response = sheet.values().get(spreadsheetId=self.sheet_id, range=range_to_check).execute()
            rows = response.get('values', [])
            for index, row in enumerate(rows):
                if len(row) >= 2 and row[0] == user and row[1] == company:
                    # Check if the command was already executed for this user and company
                    if (len(row) > 6 and row[6] == '😭') or (len(row) > 5 and row[5] == '🎉'):  
                        return False  # Command already executed for this user and company
                    else:
                        # Update only the Interviews column
                        range_to_update = f"G{index + 1}"
                        body = {'values': [['😭']]}
                        sheet.values().update(
                            spreadsheetId=self.sheet_id,
                            range=range_to_update,
                            valueInputOption='RAW',
                            body=body).execute()
                        return True
                    
            for row in rows:
                if len(row) >= 2 and row[0] == user and row[1] == company and row[6] == "😭":
                    return False
                
                else:
                    # Data to be inserted for new user and company
                    values = [[user, company, '', '', '','', '😭']]  # Empty string for the Online Assessment column
                    body = {'values': values}
                    next_row = len(rows) + 1
                    range_to_insert = f"A{next_row}:G{next_row}"

                    # Append a new row
                    sheet.values().append(
                        spreadsheetId=self.sheet_id,
                        range=range_to_insert,
                        valueInputOption='RAW',
                        body=body).execute()
                    
                    return True

        except HttpError as err:
            print(err)