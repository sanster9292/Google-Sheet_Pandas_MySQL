# Start by importing the files

from __future__ import print_function
import pickle
import os.path
import pandas as pd
import re
#Google libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# SQL libraries
from pandas.io import sql
import MySQLdb
from sqlalchemy import create_engine


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = '1mIYWBp9ExxlSaKnv22rio9nUzyJvrozYbWCrQdsOVRI'
RANGE_NAME  = 'Books'   #name of the worksheet in the google sheet.

# This function will import all the data from the google sheet in question
# and get rid of the empty cells. We will then store this data in the sheet variable

def get_sheet(SCOPES, SPREADSHEET_ID, RANGE_NAME):

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
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8910)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()
    values = result.get('values', [])

    return values

#Store the data from the google sheet in this variable.
sheet = get_sheet(SCOPES, SPREADSHEET_ID, RANGE_NAME)

# Transform the sheet into a pandas dataframe and do some house keeping before going ahead.
#Since this is different for every sheet, I will not create a function for this.

data_df = pd.DataFrame(sheet).dropna()
data_df.reset_index()
data_df.columns = data_df.iloc[0]
data_df = data_df.iloc[1:]
data_df = data_df.drop([''], axis = 1)
data_df.columns = ['start_date', 'date', 'book_title', 'author', 'genre',
       'comments']
data_df = data_df.drop('start_date', axis = 1)

# The genre section of this dataframe has two different delimiters '/' and ','.
# I am going to unify them and store them in a new column called genre_sep and drop the old genre column.

data_df['genre_sep'] = data_df['genre'].str.replace(re.escape('/'), ',')
data_df = data_df.drop('genre', axis = 1)


# I am going to reorganize the column order to match the schema of the database I created.
dat_org = data_df[['book_title', 'author', 'genre_sep', 'comments', 'date' ]]


# Let's set up the connection to the database now. I will create a dummy database just to
# make sure that it is working fine.

# I wil use MYSQL and SQLAlchemy to achieve this.

engine = create_engine("mysql+mysqldb://root:"+'PASSWORD'+"@localhost/NAME-OF-DATABASE")
dat_org.to_sql(name = 'TABLE-NAME',con=engine, if_exists='replace', index=False)
