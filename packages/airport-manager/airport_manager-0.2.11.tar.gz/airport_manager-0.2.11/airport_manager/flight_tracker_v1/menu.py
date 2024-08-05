import click
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box
from airport_manager.flight_tracker_v1.routes import get_data_from_api
from airport_manager.flight_tracker_v1.utils import print_flight_tracker_data, print_weather_data, print_flight_data
from airport_manager.utils import handle_response, print_success_panel, clear_console

console = Console()

def display_flight_tracker_v1_menu(console: Console):
    header = Text("Flight Tracker v1 Menu", justify="center", style="bold yellow")

    menu_options = [
        ("[1] Live Stats", "1"),
        ("[2] Weather Stats", "2"),
        ("[3] Departures", "3"),
        ("[4] Arrivals", "4"),
        ("[5] Ground Operations", "5"),
        ("[6] Flight by Tail Number", "6"),
        ("[7] Back to Main Menu", "7")
    ]

    table = Table(box=box.SIMPLE, show_header=False, highlight=True)
    for option, _ in menu_options:
        table.add_row(option)

    console.print(Panel(table, title="Flight Tracker v1 Options",
                  title_align="left", style="yellow"))

@click.command()
@click.pass_context
def flight_tracker_v1_menu(ctx):
    while True:
        clear_console()
        display_flight_tracker_v1_menu(console)
        choice = Prompt.ask("Select an option", choices=[
                            "1", "2", "3", "4", "5", "6", "7"], default="1")
        if choice == "7":
            return
        handle_flight_tracker_v1_menu(choice)

def handle_flight_tracker_v1_menu(choice):
    clear_console()
    if choice == "1":
        airport_code = Prompt.ask("Enter airport code for live stats", default="BOM")
        data = get_data_from_api(f"live/{airport_code}")
        if handle_response(data):
            print_flight_tracker_data(data)
            print_success_panel(data.get("status"), data.get("timestamp"))
    elif choice == "2":
        airport_code = Prompt.ask("Enter airport code for weather stats", default="BOM")
        data = get_data_from_api(f"weather/{airport_code}")
        if handle_response(data):
            print_weather_data(data)
            print_success_panel(data.get("status"), data.get("timestamp"))
    elif choice == "3":
        airport_code = Prompt.ask("Enter airport code for departures", default="BOM")
        data = get_data_from_api(f"departures/{airport_code}")
        if handle_response(data):
            print_flight_tracker_data(data)
            print_success_panel(data.get("status"), data.get("timestamp"))
    elif choice == "4":
        airport_code = Prompt.ask("Enter airport code for arrivals", default="BOM")
        data = get_data_from_api(f"arrivals/{airport_code}")
        if handle_response(data):
            print_flight_tracker_data(data)
            print_success_panel(data.get("status"), data.get("timestamp"))
    elif choice == "5":
        airport_code = Prompt.ask("Enter airport code for ground operations", default="BOM")
        data = get_data_from_api(f"ground/{airport_code}")
        if handle_response(data):
            print_flight_tracker_data(data)
            print_success_panel(data.get("status"), data.get("timestamp"))
    elif choice == "6":
        tail_number = Prompt.ask("Enter tail number for flight information", default="VT-IBH")
        data = get_data_from_api(f"flight/{tail_number}")
        if handle_response(data):
            print_flight_data(data)
            print_success_panel(data.get("status"), data.get("timestamp"))
    elif choice == "7":
        return
    Prompt.ask("Press Enter to return to the Flight Tracker v1 menu...")
