import click
from rich.console import Console
from rich.prompt import Prompt
from airport_manager.fa24.menu import display_fa24_menu, handle_fa24_menu
from airport_manager.utils import clear_console

console = Console()


@click.command()
@click.pass_context
def fa24_menu(ctx):
    while True:
        clear_console()
        display_fa24_menu(console)
        choice = Prompt.ask("Select an option", choices=["1", "2", "3"])
        if choice == "3":
            break
        handle_fa24_menu(choice)
