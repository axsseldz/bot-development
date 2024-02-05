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

        # Return numbers will be explained in 'message_handler' function

        try:
            # Get all the information from the SpreadSheet
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            range_to_check = 'A:I' 
            response = sheet.values().get(spreadsheetId=sheet_id, range=range_to_check).execute()
            rows = response.get('values', [])

            # Iterate over all the rows
            # check if there's a process with this 'user' and 'company'
            for index, row in enumerate(rows):

                # If there's already a process with the 'user' and 'company'
                # We want to know if it's a valid process 
                if len(row) >= 2 and row[0] == user and row[1] == company:

                    # For loop to check it there's is an advanced process
                    # 'index_to_insert' is from where we want to insert our check
                    # We iterate just all the way before 'offer' and 'rejection' 
                    for i in range(index_to_insert, len(row) - 2):

                        # 'user' already applied to this 'company'
                        if row[i] != '-' and index_to_insert == 2:
                            return '0'
    
                        # There's an advanced process with this 'user' and 'company'
                        if row[i] != '-':
                            return '1'
                        
                    # A desition has ben made by the company (either rejection or offer)
                    if row[len(row) - 2] != '-' or row[len(row) - 1] != '-':
                        return '2'
                        
                    # If we already iterated over the row 
                    # And we didn't find any advanced process, we check the 'index_to_insert'
                    else:
                        range_to_update = f"{column}{index + 1}"
                        body = {'values': [['✅']]}
                        sheet.values().update(
                            spreadsheetId=sheet_id,
                            range=range_to_update,
                            valueInputOption='RAW',
                            body=body).execute()
                        return '3'
                    
            # Already checked all rows and there's no process with 'user' and 'company' 
            # A process starts with 'user' and 'company'
            # We mark all positions with a '-' for better error control
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
            

            # 'user' has not applied to 'company' yet
            else:
                return '5'
            

        except HttpError as err:
            print(err)

def insert_company(company: str,  creds: any, sheet_id: any) -> bool :
    """
    Helper funcition to insert data into companies Google spreadsheet
    """
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        response = sheet.values().get(spreadsheetId=sheet_id, range="Allowed Companies").execute()
        rows = response.get('values', [])

        if [company] in rows:
            return False

        new_data = [[company]]
        body = {'values': new_data}
        sheet.values().append(
            spreadsheetId=sheet_id,
            range="Allowed Companies",
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"'{company}' has been added to the spread sheet")
        return True
    except HttpError as err:
        print(err)
        return False

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

    # '0': 'user' already applied to a certain 'company'
    if insertion_response == '0':
        return Messages.already_applied_message(user, company)

    # '1': 'user' has an advanced process with 'company'
    if insertion_response == '1':
        return Messages.advanced_process_message(user, company, process_state)

    # '2': 'user' has already received a desicion from 'company'
    elif insertion_response == '2':
        return Messages.final_desicion_message(user, company)
    
    # '3': 'user' moved forwrad in the process with 'company'
    elif insertion_response == '3':
        return Messages.successful_insertion_message(user, company, from_offer, from_rejection,process_state)

    # '4': 'user' applied successfully to a certain 'company'
    elif insertion_response == '4':
        return Messages.apply_message(user, company)
    
    # '5': 'user' attempted to use a command before 'apply'
    elif insertion_response == '5':
        return Messages.proper_procedure_message(user, company)
    