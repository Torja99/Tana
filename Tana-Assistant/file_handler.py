import os
import glob
import custom_logger


def remove_mp3():
    dir_path = f"{os.path.dirname(os.path.realpath(__file__))}\\temp-audio"
    for fl in glob.glob(f"{dir_path}\\*.mp3"):
        custom_logger.log.info(f"removed: {fl}")
        os.remove(fl)


def create_log():
    dir_path = f"{os.path.dirname(os.path.realpath(__file__))}"
    with open(f"{dir_path}/log_files/tana.log", 'w') as fp:
        pass


def remove_token():
    file_path = f"{os.path.dirname(os.path.realpath(__file__))}\\token.json"
    custom_logger.log.info(f"removed: {file_path}")
    os.remove(file_path)
