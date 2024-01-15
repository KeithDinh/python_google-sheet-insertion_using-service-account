from google.oauth2 import service_account
from googleapiclient.discovery import build

spreadsheet_id = 'your google sheet ID' # get from the url of the google sheet
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def auth():
  credentials = service_account.Credentials.from_service_account_file("private_key.json", scopes=SCOPES)
  service = build("sheets", "v4", credentials=credentials)
  return service

def get_sheet_name():
  # A single google sheet has many spreadsheets (tabs)
  ss = auth().spreadsheets()
  
  request = ss.get(spreadsheetId=spreadsheet_id, ranges=[], includeGridData=False)
  sheet_props = request.execute()
  print(sheet_props)


def append_values(range_name, _values):
  '''
  ValueInputOption
  RAW	not parsed and inserted as a string. "=1+2" places the string, not the formula
  USER_ENTERED	parsed exactly as entered into the Sheets UI."Mar 1 2016" becomes a date, and "=1+2" becomes a formula. Formats can also be inferred, so "$100.15" becomes a number with currency formatting.
  '''
  ss = auth().spreadsheets()

  body = {"values": _values}
  result = (
      ss.values()
      .append(
          spreadsheetId=spreadsheet_id,
          range=range_name,
          valueInputOption='RAW',
          # insertDataOption='INSERT_ROWS', # this line renders new line with BOLD
          body=body)
      .execute()
  )
  
  print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
  return result

append_values( "A2:F2", [["1", "2", "3", "4", "5", "6"]], )

# get_sheet_name()