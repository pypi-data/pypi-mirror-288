import sys
import ast
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.prompt import Prompt
from airport_manager.database.routes import get_airport_coords, find_area, find_areas_for_coordinates
from airport_manager.utils import print_data, handle_response, print_success_panel
from airport_manager.config import get_token
from airport_manager.utils import clear_console

console = Console()


def display_database_menu(console: Console):
    header = Text("Database Menu", justify="center", style="bold blue")

    menu_options = [
        ("[1] Get Airport Coordinates", "1"),
        ("[2] Find Area by Coordinates", "2"),
        ("[3] Find Areas for Coordinates", "3"),
        ("[4] Back to Main Menu", "4"),
        ("[5] Exit", "5")
    ]

    table = Table(box=box.SIMPLE, show_header=False, highlight=True)
    for option, _ in menu_options:
        table.add_row(option)

    console.print(Panel(table, title="Database Options",
                  title_align="left", style="blue"))


def handle_database_menu(choice, raw):
    clear_console()
    data = None
    token = get_token()  # Get the API token
    title = ""
    style = ""

    if choice == "1":
        console.print(Panel("Retrieve the coordinates for a specified airport code.", style="green"))
        while True:
            airport_code = Prompt.ask("Enter airport code", default="BOM")
            data = get_airport_coords(airport_code, token)
            if handle_response(data):
                title = "Airport Coordinates"
                style = "bold green"
                break
            else:
                console.print("[red]Invalid airport code. Please try again.[/red]")

    elif choice == "2":
        console.print(Panel("Find the area for given latitude and longitude coordinates.", style="cyan"))
        while True:
            lat = Prompt.ask("Enter latitude", default="19.0952415")
            lon = Prompt.ask("Enter longitude", default="72.8713955")
            try:
                lat = float(lat)
                lon = float(lon)
                data = find_area(lat, lon, token)
                if handle_response(data):
                    title = "Area Information"
                    style = "bold cyan"
                    break
                else:
                    console.print("[red]Invalid coordinates. Please try again.[/red]")
            except ValueError:
                console.print("[red]Invalid input. Please enter valid numbers for latitude and longitude.[/red]")

    elif choice == "3":
        console.print(Panel("Find areas for a list of coordinates.", style="magenta"))
        while True:
            try:
                coords_input = Prompt.ask("Enter coordinates as a list of dicts (e.g., [{'lat': 1.0, 'lon': 2.0}])", default="[{'lat': 19.0952415, 'lon': 72.8713955}]")
                coords = ast.literal_eval(coords_input)
                if isinstance(coords, list) and all(isinstance(item, dict) for item in coords):
                    data = find_areas_for_coordinates(coords, token)
                    if handle_response(data):
                        title = "Areas for Coordinates"
                        style = "bold magenta"
                        break
                    else:
                        console.print("[red]Invalid coordinates. Please try again.[/red]")
                else:
                    raise ValueError
            except (SyntaxError, ValueError):
                console.print("[red]Invalid input for coordinates. Please enter a valid list of dicts.[/red]")

    if data:
        print_data(data, title, style)
        print_success_panel(data.get("status"), data.get("timestamp"))

    if raw:
        console.print("\n[bold]Raw Response:[/bold]")
        console.print(data)

    Prompt.ask("Press Enter to return to the database menu...")


if __name__ == "__main__":
    while True:
        clear_console()
        display_database_menu(console)
        choice = Prompt.ask(
            "Select an option [1/2/3/4/5]", choices=["1", "2", "3", "4", "5"])
        if choice == "4":
            break
        elif choice == "5":
            console.print("[red]Exiting...[/red]")
            sys.exit()
        handle_database_menu(choice, raw=True)
