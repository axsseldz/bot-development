from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def insert_data(
        user: str, 
        company: str, 
        creds: any, 
        sheet_id: any, 
        index_to_insert: int = 0, 
        column: str = 'A', 
        from_apply: bool = False) -> bool:
        """
        Helper function to insert data into the Google SpreadSheet
        """
        try:
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            range_to_check = 'A:I' 
            response = sheet.values().get(spreadsheetId=sheet_id, range=range_to_check).execute()
            rows = response.get('values', [])


            for index, row in enumerate(rows):

                if len(row) >= 2 and row[0] == user and row[1] == company:
                    for i in range(index_to_insert, len(row)):
    
                        if row[i] != '-':
                            return False
                        
                    if row[len(row) - 2] != '-':
                        return False
                        
                    else:
                        range_to_update = f"{column}{index + 1}"
                        body = {'values': [['✅']]}
                        sheet.values().update(
                            spreadsheetId=sheet_id,
                            range=range_to_update,
                            valueInputOption='RAW',
                            body=body).execute()
                        return True
                    
            if from_apply:
                values = [[user, company, '✅', '-', '-', '-', '-', '-', '-']]
                body = {'values': values}
                next_row = len(rows) + 1
                range_to_insert = f"A{next_row}:I{next_row}"

                sheet.values().append(
                    spreadsheetId=sheet_id,
                    range=range_to_insert,
                    valueInputOption='RAW',
                    body=body).execute()
            
                return True

            else:
                return False
            

        except HttpError as err:
            print(err)