import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('ENV', 'production')
BASE_URL = os.getenv("BASE_URL")
