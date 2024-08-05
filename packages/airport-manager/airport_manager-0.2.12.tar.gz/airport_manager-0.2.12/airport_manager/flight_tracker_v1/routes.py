import requests
from rich.panel import Panel
from rich.console import Console
from airport_manager.utils import show_progress, clear_console
from airport_manager.config import BASE_URL, get_token

console = Console()

API_BASE_URL = f'{BASE_URL}flight-tracker/v1'

def get_data_from_api(endpoint):
    url = f"{API_BASE_URL}/{endpoint}"
    token = get_token()
    headers = {'api-token': token}
    
    response = None
    for _ in show_progress("Fetching data..."):
        response = requests.get(url, headers=headers)
        if response.status_code == 200 or response.status_code != 200:
            break
    
    clear_console()
    
    if response.status_code == 200:
        return response.json()
    else:
        console.print(Panel(f"Request failed: {response.json().get('message', 'Unknown error')}", style="bold red"))
        return None

