import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.prompt import Prompt
from airport_manager.auth.routes import authenticate

console = Console()


def display_auth_menu(console: Console):
    header = Text("Auth Menu", justify="center", style="bold green")

    menu_options = [
        ("[1] Login", "1"),
        ("[2] Logout", "2"),
        ("[3] Back to Main Menu", "3")
    ]

    table = Table(box=box.SIMPLE, show_header=False, highlight=True)
    for option, _ in menu_options:
        table.add_row(option)

    console.print(Panel(table, title="Auth Options",
                  title_align="left", style="green"))


def handle_auth_menu(choice):
    console.clear()
    if choice == "1":
        username = Prompt.ask("Enter username")
        password = Prompt.ask("Enter password", password=True)
        token = authenticate(username, password)
        console.print(f'[green]Authenticated. Token: {token}[/green]')
        with open('.token', 'w') as f:
            f.write(token)
    elif choice == "2":
        try:
            os.remove('.token')
            console.print(f'[green]Logged out successfully.[/green]')
        except FileNotFoundError:
            console.print(f'[red]No active session found.[/red]')
    Prompt.ask("Press Enter to return to the auth menu...")
