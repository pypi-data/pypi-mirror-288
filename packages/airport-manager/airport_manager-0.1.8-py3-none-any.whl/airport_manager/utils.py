from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def print_data(data):
    if data:
        status = data.get("status", "unsuccess")
        timestamp = data.get("timestamp", "")

        table = Table(title="Server Data")
        table.add_column("Key")
        table.add_column("Value")

        for key, value in data.items():
            if isinstance(value, dict):
                value = format_dict(value)
            elif isinstance(value, list):
                value = format_list(value)
            table.add_row(key, str(value))

        panel_style = "green" if status == "success" else "red"
        panel_title = f"Status: {status}"
        if timestamp:
            panel_title += f" | Timestamp: {timestamp}"
        console.print(Panel(table, title=panel_title, style=panel_style))
    else:
        console.print("[red]No data to display.[/red]")


def format_dict(d):
    table = Table(box=None)
    table.add_column("Key", style="bold")
    table.add_column("Value")

    for key, value in d.items():
        table.add_row(key, str(value))

    return table


def format_list(lst):
    table = Table(box=None)
    for i, item in enumerate(lst):
        if isinstance(item, dict):
            item = format_dict(item)
        table.add_row(str(i), str(item))
    return table
