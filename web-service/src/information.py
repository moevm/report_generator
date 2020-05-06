from app import ABS_PATH
OAUTH_FILE = ABS_PATH.format('oauth.txt')


def get_oauth():
    with open(OAUTH_FILE, 'r') as file:
        return file.read().strip()
