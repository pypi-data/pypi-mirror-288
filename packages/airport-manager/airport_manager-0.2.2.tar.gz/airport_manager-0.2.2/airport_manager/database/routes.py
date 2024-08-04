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


def handle_response(response):
    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        timestamp = extract_timestamp(response)
        return {"status": "unsuccess", "message": str(http_err), "timestamp": timestamp}
    except Exception as err:
        return {"status": "unsuccess", "message": str(err), "timestamp": ""}


def get_airport_coords(airport_code):
    try:
        response = requests.get(
            f'{BASE_URL}/database/airport-coords/{airport_code}')
        console.print(f"[green]Coordinates fetched successfully for airport code: {
                      airport_code}[/green]")
        return handle_response(response)
    except Exception as err:
        console.print(f"[red]Failed to fetch coordinates for airport code: {
                      airport_code}[/red]")
        return handle_response(response)


def find_area(lat, lon):
    try:
        response = requests.get(f'{BASE_URL}/database/find-area/{lat}/{lon}')
        console.print(
            f"[green]Area found successfully for coordinates: ({lat}, {lon})[/green]")
        return handle_response(response)
    except Exception as err:
        console.print(
            f"[red]Failed to find area for coordinates: ({lat}, {lon})[/red]")
        return handle_response(response)


def find_areas_for_coordinates(coordinates):
    try:
        response = requests.post(
            f'{BASE_URL}/database/find-areas-for-coordinates', json={'coords': coordinates})
        console.print(
            f"[green]Areas found successfully for provided coordinates[/green]")
        return handle_response(response)
    except Exception as err:
        console.print(
            f"[red]Failed to find areas for provided coordinates[/red]")
        return handle_response(response)
