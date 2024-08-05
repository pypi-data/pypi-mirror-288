import click
import sys
from rich.console import Console
from rich.prompt import Prompt
from airport_manager.database.menu import display_database_menu, handle_database_menu
from animations.end_animation import end_animation

console = Console()


@click.command()
@click.option('-r', '--raw', is_flag=True, help="Show raw response")
@click.pass_context
def database_menu(ctx, raw):
    while True:
        console.clear()
        display_database_menu(console)
        choice = Prompt.ask("Select an option", choices=[
                            "1", "2", "3", "4", "5"])
        if choice == "4":
            break
        elif choice == "5":
            console.clear()
            end_animation()
            sys.exit()
        handle_database_menu(choice, raw)
