import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('ENV', 'production')
BASE_URL = "http://127.0.0.1:8000"
