from __future__ import print_function
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def auth_flow(creds, SCOPES):

    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
