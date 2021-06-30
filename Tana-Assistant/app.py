from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from gtts.tts import gTTSError
# from gui import run_welcome_page
from googleapiclient.discovery import build
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']
# TODO: change to use main file https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6


def main_page_flow():
    from gui_main import run_main_page
    run_main_page()
    from voice import remove_mp3
    remove_mp3()


def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # service = initializer.creds
    # # The file token.json stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        from gui_welcome import run_welcome_page

        run_welcome_page(creds, SCOPES)
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        main_page_flow()
    else:
        main_page_flow()


if __name__ == '__main__':
    main()
