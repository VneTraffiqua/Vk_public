import requests
import os
from dotenv import load_dotenv


def get_access_token(key):
    url = 'https://oauth.vk.com/authorize'
    params = {
        'client_id': key,
        'response_type': 'token',
        'scope': 'photos, groups, wall, offline'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text


if __name__ == '__main__':
    load_dotenv()
    secret_key = os.getenv('CLIENT_ID')
    print(get_access_token(secret_key))
