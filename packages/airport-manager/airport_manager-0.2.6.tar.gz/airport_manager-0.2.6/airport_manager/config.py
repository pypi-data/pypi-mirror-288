import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('ENV', 'production')
BASE_URL = "http://127.0.0.1:8000/"

# config.py
api_token = None


def set_token(token):
    global api_token
    api_token = token


def get_token():
    return api_token
