from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import file_handler
import custom_logger
SCOPES = ['https://www.googleapis.com/auth/tasks']


def main_page_flow():
    from gui_main import run_main_page
    run_main_page()  # if error occurs remove mp3 doesn't happen
    file_handler.remove_mp3()


def main():
    file_handler.create_log()
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:  # expired token case
            creds.refresh(Request())
        else:
            try:
                # token invalid or not there
                from gui_welcome import run_welcome_page
                run_welcome_page(creds, SCOPES)
                creds = Credentials.from_authorized_user_file(
                    'token.json', SCOPES)
            except FileNotFoundError:
                custom_logger.log.info("Early Exit Error")

    main_page_flow()


if __name__ == '__main__':
    main()
