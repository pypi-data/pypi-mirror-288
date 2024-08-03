from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.prompt import Prompt

console = Console()


def display_fr24_menu(console: Console):
    header = Text("FR24 Menu", justify="center", style="bold yellow")

    menu_options = [
        ("[1] FR24 Option 1", "1"),
        ("[2] FR24 Option 2", "2"),
        ("[3] Back to Main Menu", "3")
    ]

    table = Table(box=box.SIMPLE, show_header=False, highlight=True)
    for option, _ in menu_options:
        table.add_row(option)

    console.print(Panel(table, title="FR24 Options",
                  title_align="left", style="yellow"))


def handle_fr24_menu(choice):
    console.clear()
    if choice == "1":
        # Handle FR24 Option 1
        console.print("[yellow]FR24 Option 1 selected.[/yellow]")
    elif choice == "2":
        # Handle FR24 Option 2
        console.print("[yellow]FR24 Option 2 selected.[/yellow]")
    Prompt.ask("Press Enter to return to the FR24 menu...")
