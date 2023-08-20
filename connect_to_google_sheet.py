import gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client

def connect_to_google_sheet_and_get_sheet(spreadsheet_id, sheet_name, credentials_file):
    # Connect to Google Sheets using service account credentials
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file)
    client = gspread.authorize(credentials)

    # Open the specific sheet within the spreadsheet
    try:
        spreadsheet = client.open_by_key(spreadsheet_id)
    except gspread.exceptions.APIError as e:
        print("Error: {}".format(e))
        print("Make sure the spreadsheet ID is correct.")
        return

    try:
        sheet = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.APIError as e:
        print("Error: {}".format(e))
        print("Make sure the sheet name is correct.")
        return
    
    return sheet
