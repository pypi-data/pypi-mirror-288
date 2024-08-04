from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.prompt import Prompt
from airport_manager.database.routes import get_api_token, get_airport_coords, find_area, find_areas_for_coordinates
from airport_manager.utils import print_data

console = Console()

def display_database_menu(console: Console):
    header = Text("Database Menu", justify="center", style="bold blue")

    menu_options = [
        ("[1] Get API Token", "1"),
        ("[2] Get Airport Coordinates", "2"),
        ("[3] Find Area by Coordinates", "3"),
        ("[4] Find Areas for Coordinates", "4"),
        ("[5] Back to Main Menu", "5")
    ]

    table = Table(box=box.SIMPLE, show_header=False, highlight=True)
    for option, _ in menu_options:
        table.add_row(option)

    console.print(Panel(table, title="Database Options", title_align="left", style="blue"))

def handle_database_menu(choice, raw):
    console.clear()
    data = None
    if choice == "1":
        airport_code = Prompt.ask("Enter airport code")
        data = get_api_token(airport_code)
    elif choice == "2":
        airport_code = Prompt.ask("Enter airport code")
        data = get_airport_coords(airport_code)
    elif choice == "3":
        lat = None
        lon = None
        while lat is None:
            try:
                lat = float(Prompt.ask("Enter latitude"))
            except ValueError:
                console.print("[red]Invalid input for latitude. Please enter a valid number.[/red]")
        while lon is None:
            try:
                lon = float(Prompt.ask("Enter longitude"))
            except ValueError:
                console.print("[red]Invalid input for longitude. Please enter a valid number.[/red]")
        data = find_area(lat, lon)
    elif choice == "4":
        coords = None
        while coords is None:
            try:
                coords_input = Prompt.ask("Enter coordinates as a list of dicts (e.g., [{'lat': 1.0, 'lon': 2.0}])")
                coords = eval(coords_input)
                if not isinstance(coords, list) or not all(isinstance(item, dict) for item in coords):
                    raise ValueError
            except (SyntaxError, ValueError):
                console.print("[red]Invalid input for coordinates. Please enter a valid list of dicts.[/red]")
                coords = None
        data = find_areas_for_coordinates(coords)

    console.clear()
    print_data(data)

    if raw:
        console.print("\n[bold]Raw Response:[/bold]")
        console.print(data)

    Prompt.ask("Press Enter to return to the database menu...")
