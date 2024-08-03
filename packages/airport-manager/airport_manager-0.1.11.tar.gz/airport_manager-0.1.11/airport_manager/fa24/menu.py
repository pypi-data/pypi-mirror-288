from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.prompt import Prompt

console = Console()


def display_fa24_menu(console: Console):
    header = Text("FA24 Menu", justify="center", style="bold cyan")

    menu_options = [
        ("[1] FA24 Option 1", "1"),
        ("[2] FA24 Option 2", "2"),
        ("[3] Back to Main Menu", "3")
    ]

    table = Table(box=box.SIMPLE, show_header=False, highlight=True)
    for option, _ in menu_options:
        table.add_row(option)

    console.print(Panel(table, title="FA24 Options",
                  title_align="left", style="cyan"))


def handle_fa24_menu(choice):
    console.clear()
    if choice == "1":
        # Handle FA24 Option 1
        console.print("[cyan]FA24 Option 1 selected.[/cyan]")
    elif choice == "2":
        # Handle FA24 Option 2
        console.print("[cyan]FA24 Option 2 selected.[/cyan]")
    Prompt.ask("Press Enter to return to the FA24 menu...")
