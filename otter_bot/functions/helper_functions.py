from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from otter_bot.common.bot_messages import Messages

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
                    for i in range(index_to_insert, len(row) - 2):
    
                        if row[i] != '-':
                            return '1'
                        
                    if row[len(row) - 2] != '-' or row[len(row) - 1] != '-':
                        return '2'
                        
                    else:
                        range_to_update = f"{column}{index + 1}"
                        body = {'values': [['✅']]}
                        sheet.values().update(
                            spreadsheetId=sheet_id,
                            range=range_to_update,
                            valueInputOption='RAW',
                            body=body).execute()
                        return '3'
                    
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
            
                return '4'

            else:
                return '5'
            

        except HttpError as err:
            print(err)



def message_handler(
        user: str, 
        company: str, 
        insertion_response: str,
        process_state: str = '',
        from_rejection = False,
        from_offer = False, ) -> str:
    """
    Helper function to hadle Bot messages
    """

    if insertion_response == '1':
        return Messages.advanced_process_message(user, company, process_state)

    elif insertion_response == '2':
        return Messages.final_desicion_message(user, company)
    
    elif insertion_response == '3':
        return Messages.successful_insertion_message(user, company, from_offer, from_rejection,process_state)

    elif insertion_response == '4':
        return Messages.apply_message(user, company)

    elif insertion_response == '5':
        return Messages.proper_procedure_message(user, company)
    