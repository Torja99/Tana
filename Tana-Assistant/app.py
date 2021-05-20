from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']
# TODO: change to use main file https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6


def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # !INSERT call to main page

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # !INSERT call to welcome page
        # TODO: make a function in gui for below logic up writing token
        # above will accept creds as a parameter and
        # call that function on button click of google sign in
        # in below else condition make call to other gui
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


if __name__ == '__main__':
    main()
