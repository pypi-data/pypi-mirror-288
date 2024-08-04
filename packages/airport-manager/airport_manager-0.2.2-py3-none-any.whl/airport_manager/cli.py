import sys
import click
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich import box
from animations.welcome_animation import welcome_animation, typewriter
from animations.end_animation import end_animation
from airport_manager.auth.menu import display_auth_menu, handle_auth_menu
from airport_manager.database.menu import display_database_menu, handle_database_menu
from airport_manager.fr24.menu import display_fr24_menu, handle_fr24_menu
from airport_manager.fa24.menu import display_fa24_menu, handle_fa24_menu

console = Console()


def get_token():
    return 'fixed-token'


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


@click.group()
def cli():
    console.clear()
    welcome_animation()


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


@click.command()
@click.pass_context
def auth_menu(ctx):
    while True:
        console.clear()
        display_auth_menu(console)
        choice = Prompt.ask("Select an option", choices=["1", "2", "3"])

        if choice == "3":
            break

        handle_auth_menu(choice)


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


@click.command()
@click.pass_context
def fa24_menu(ctx):
    while True:
        console.clear()
        display_fa24_menu(console)
        choice = Prompt.ask("Select an option", choices=["1", "2", "3"])

        if choice == "3":
            break

        handle_fa24_menu(choice)


cli.add_command(main_menu)
cli.add_command(auth_menu)
cli.add_command(database_menu)
cli.add_command(fr24_menu)
cli.add_command(fa24_menu)

if __name__ == "__main__":
    cli()
