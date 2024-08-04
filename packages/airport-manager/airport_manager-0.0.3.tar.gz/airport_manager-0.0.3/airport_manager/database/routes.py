import requests
from rich.console import Console
from airport_manager.config import BASE_URL

console = Console()


def extract_timestamp(response):
    try:
        error_data = response.json()
        return error_data.get('timestamp', '')
    except ValueError:
        return ''


def get_api_token(airport_code):
    try:
        response = requests.get(f'{BASE_URL}/database/api-token/{airport_code}', )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        timestamp = extract_timestamp(response)
        return {"status": "unsuccess", "message": str(http_err), "timestamp": timestamp}
    except Exception as err:
        return {"status": "unsuccess", "message": str(err), "timestamp": ""}


def get_airport_coords(airport_code):
    try:
        response = requests.get(f'{BASE_URL}/database/airport-coords/{airport_code}', )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        timestamp = extract_timestamp(response)
        return {"status": "unsuccess", "message": str(http_err), "timestamp": timestamp}
    except Exception as err:
        return {"status": "unsuccess", "message": str(err), "timestamp": ""}


def find_area(lat, lon):
    try:
        response = requests.get(f'{BASE_URL}/database/find-area/{lat}/{lon}')
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        timestamp = extract_timestamp(response)
        return {"status": "unsuccess", "message": str(http_err), "timestamp": timestamp}
    except Exception as err:
        return {"status": "unsuccess", "message": str(err), "timestamp": ""}


def find_areas_for_coordinates(coordinates):
    try:
        response = requests.post(f'{BASE_URL}/database/find-areas-for-coordinates', json={
            'coords': coordinates
        }, )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        timestamp = extract_timestamp(response)
        return {"status": "unsuccess", "message": str(http_err), "timestamp": timestamp}
    except Exception as err:
        return {"status": "unsuccess", "message": str(err), "timestamp": ""}
