import sys
import click
from rich.panel import Panel
from rich.console import Console
from animations.welcome_animation import welcome_animation
from animations.end_animation import end_animation
from airport_manager.config import set_token, get_token
from airport_manager.database.routes import check_token_validity
from airport_manager.main_menu import main_menu
from airport_manager.auth.main_menu import auth_menu
from airport_manager.database.main_menu import database_menu
from airport_manager.fr24.main_menu import fr24_menu
from airport_manager.fa24.main_menu import fa24_menu

console = Console()


def validate_token():
    while True:
        token = console.input("Please enter your API token: ")
        response = check_token_validity(token)
        if response and response.get("status") == "success":
            set_token(token)
            console.print(
                Panel("Token validated successfully!", style="bold green"))
            break
        else:
            console.print(Panel(f"Token validation failed: {response.get('message', 'Unknown error')}", style="bold red"))


@click.group()
def cli():
    console.clear()
    welcome_animation()
    validate_token()


cli.add_command(main_menu)
cli.add_command(auth_menu)
cli.add_command(database_menu)
cli.add_command(fr24_menu)
cli.add_command(fa24_menu)

if __name__ == "__main__":
    cli()
