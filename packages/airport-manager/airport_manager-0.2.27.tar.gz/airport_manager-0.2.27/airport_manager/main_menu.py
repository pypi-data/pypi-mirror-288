import click
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box
from airport_manager.database.main_menu import database_menu
from airport_manager.flight_tracker_v1.main_menu import flight_tracker_v1_menu
from airport_manager.fa24.main_menu import fa24_menu
from animations.end_animation import end_animation
from airport_manager.utils import clear_console

console = Console()

def display_main_menu(console: Console):
    header = Text("Main Menu", justify="center", style="bold blue")
    menu_options = [
        ("[D] Database Menu", "D"),
        ("[R] Flight Tracker v1 Menu", "R"),
        ("[F] FA24 Menu", "F"),
        ("[5] Exit", "5")
    ]
    table = Table(box=box.SIMPLE, show_header=False, highlight=True)
    for option, _ in menu_options:
        table.add_row(option)
    console.print(Panel(table, title="Options",
                  title_align="left", style="blue"))

@click.command()
@click.pass_context
def main_menu(ctx):
    while True:
        clear_console()
        display_main_menu(console)
        choice = Prompt.ask("Select an option", choices=[
                            "D", "R", "F", "5"], default="D")
        if choice == "5":
            clear_console()
            end_animation()
            break
        elif choice == "D":
            ctx.invoke(database_menu)
        elif choice == "F":
            ctx.invoke(fa24_menu)
        elif choice == "R":
            ctx.invoke(flight_tracker_v1_menu)
