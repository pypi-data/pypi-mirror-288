import click
from rich.console import Console
from rich.prompt import Prompt
from airport_manager.utils import clear_console
from airport_manager.auth.menu import display_auth_menu, handle_auth_menu

console = Console()


@click.command()
@click.pass_context
def auth_menu(ctx):
    while True:
        clear_console()
        display_auth_menu(console)
        choice = Prompt.ask("Select an option", choices=["1", "2", "3"])
        if choice == "3":
            break
        handle_auth_menu(choice)
