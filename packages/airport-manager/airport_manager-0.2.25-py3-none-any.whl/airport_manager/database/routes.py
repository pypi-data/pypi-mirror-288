import requests
from rich.console import Console
from rich.panel import Panel
from airport_manager.config import BASE_URL

console = Console()


def handle_response(response):
    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        console.print(Panel(f"HTTP error occurred: {
                      http_err}", style="bold red"))
    except Exception as err:
        console.print(Panel(f"Other error occurred: {err}", style="bold red"))
    return None


def get_airport_coords(airport_code, token):
    try:
        response = requests.get(
            f"{BASE_URL}database/airport-coords/{airport_code}", headers={"api-token": token})
    except requests.ConnectionError as conn_err:
        console.print(Panel(f"Connection error occurred: {
                      conn_err}", style="bold red"))
        response = None

    if response is not None:
        return handle_response(response)
    else:
        return None


def find_area(lat, lon, token):
    try:
        response = requests.get(
            f"{BASE_URL}database/find-area/{lat}/{lon}", headers={"api-token": token})
    except requests.ConnectionError as conn_err:
        console.print(Panel(f"Connection error occurred: {
                      conn_err}", style="bold red"))
        response = None

    if response is not None:
        return handle_response(response)
    else:
        return None


def find_areas_for_coordinates(coords, token):
    try:
        response = requests.post(f"{BASE_URL}database/find-areas-for-coordinates", json={
                                 "coords": coords}, headers={"api-token": token})
    except requests.ConnectionError as conn_err:
        console.print(Panel(f"Connection error occurred: {
                      conn_err}", style="bold red"))
        response = None

    if response is not None:
        return handle_response(response)
    else:
        return None


def check_token_validity(token):
    try:
        response = requests.get(
            f"{BASE_URL}public/check-token-validity/{token}")
    except requests.ConnectionError as conn_err:
        console.print(Panel(f"Connection error occurred: {
                      conn_err}", style="bold red"))
        response = None

    if response is not None:
        return handle_response(response)
    else:
        return None
