from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from gtts.tts import gTTSError
from googleapiclient.discovery import build
import file_handler
SCOPES = ['https://www.googleapis.com/auth/tasks']
# TODO: change to use main file https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6


def main_page_flow():
    from gui_main import run_main_page
    run_main_page()  # if error occurs remove mp3 doesn't happen
    file_handler.remove_mp3()


def main():
    file_handler.create_log()
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    #!EXPIRED TOKEN.JSON (not creds.valid) case does not work
    if not creds:
        from gui_welcome import run_welcome_page
        run_welcome_page(creds, SCOPES)
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        main_page_flow()

    elif (not creds.valid):
        print("hello")
        file_handler.remove_token()
    else:
        main_page_flow()


if __name__ == '__main__':
    main()
