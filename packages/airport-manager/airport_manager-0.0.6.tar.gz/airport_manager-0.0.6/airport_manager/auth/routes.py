import requests
from airport_manager.config import BASE_URL
from airport_manager.config import ENV


def authenticate(username, password):
    if ENV == 'testing':
        return 'test-token'

    response = requests.post(f'{BASE_URL}/auth/login', json={
        'username': username,
        'password': password
    })
    response.raise_for_status()
    return response.json()['token']
