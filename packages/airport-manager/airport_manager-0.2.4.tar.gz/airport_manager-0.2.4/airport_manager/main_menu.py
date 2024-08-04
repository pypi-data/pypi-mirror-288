import click
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box
from airport_manager.auth.main_menu import auth_menu
from airport_manager.database.main_menu import database_menu
from airport_manager.fr24.main_menu import fr24_menu
from airport_manager.fa24.main_menu import fa24_menu
from animations.end_animation import end_animation

console = Console()


def display_main_menu(console: Console):
    header = Text("Main Menu", justify="center", style="bold blue")
    menu_options = [
        ("[A] Auth Menu", "A"),
        ("[D] Database Menu", "D"),
        ("[R] FR24 Menu", "R"),
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
        console.clear()
        display_main_menu(console)
        choice = Prompt.ask("Select an option", choices=[
                            "A", "D", "R", "F", "5"], default="A")
        if choice == "5":
            console.clear()
            end_animation()
            break
        if choice == "A":
            ctx.invoke(auth_menu)
        elif choice == "D":
            ctx.invoke(database_menu)
        elif choice == "F":
            ctx.invoke(fa24_menu)
        elif choice == "R":
            ctx.invoke(fr24_menu)
