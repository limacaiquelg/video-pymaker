import json
import os
import shutil


def access_credentials(filename: str, key: str) -> str:
    CREDENTIALS_DIRECTORY = 'credentials'
    CREDENTIALS_FILENAME = filename if filename.endswith('.json') else f'{filename}.json'

    with open(os.path.join(CREDENTIALS_DIRECTORY, CREDENTIALS_FILENAME), 'r') as file:
        credentials_dict = json.load(file)

    credential = credentials_dict.get(key)
    return credential


def create_new_directory(dirname: str, robot: str) -> bool:
    try:
        os.mkdir(dirname)
        return True
    except FileExistsError:
        print(f'> [{robot.capitalize()} Robot] Directory \'{dirname}\' already exists.')
        return False


def remove_directory(dirname: str, robot: str) -> bool:
    try:
        shutil.rmtree(dirname, ignore_errors=True)
        return True
    except Exception as e:
        print(f'> [{robot.capitalize()} Robot] Error deleting content directory: {e}')
        return False
