import click
from rich.console import Console
from rich.prompt import Prompt
from airport_manager.flight_tracker_v1.menu import display_flight_tracker_v1_menu, handle_flight_tracker_v1_menu
from airport_manager.utils import clear_console

console = Console()

@click.command()
@click.pass_context
def flight_tracker_v1_menu(ctx):
    while True:
        clear_console()
        display_flight_tracker_v1_menu(console)
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
        if choice == "8":
            break
        handle_flight_tracker_v1_menu(choice)
