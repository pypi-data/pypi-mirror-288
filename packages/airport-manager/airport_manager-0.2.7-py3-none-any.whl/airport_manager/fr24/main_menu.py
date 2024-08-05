import click
from rich.console import Console
from rich.prompt import Prompt
from airport_manager.fr24.menu import display_fr24_menu, handle_fr24_menu

console = Console()


@click.command()
@click.pass_context
def fr24_menu(ctx):
    while True:
        console.clear()
        display_fr24_menu(console)
        choice = Prompt.ask("Select an option", choices=["1", "2", "3"])
        if choice == "3":
            break
        handle_fr24_menu(choice)
