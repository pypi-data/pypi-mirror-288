import time
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

FACTS = [
    "Did you know? Airport Manager supports real-time flight tracking.",
    "Tip: You can view weather stats by entering the airport code.",
    "Fun fact: The Airport Manager was built with FastAPI and Rich!",
    "Pro tip: Use the API token for authenticated requests.",
    "Did you know? You can track flights by their tail number."
]

def clear_console():
    console.print("\033c", end="")

def handle_response(response):
    status = response.get("status", "unsuccess")
    timestamp = response.get("timestamp", "")
    message = response.get("message", "Unknown error")

    if status != 'success':
        error_message = f"Status: {status} | Message: {message} | Timestamp: {timestamp}"
        console.print(Panel(Text(error_message, justify="center"), style="red"))
        return False

    return True

def print_success_panel(status, timestamp):
    panel_title = f"Status: {status} | Timestamp: {timestamp}"
    panel_style = "green" if status == "success" else "red"
    console.print(Panel(Text(panel_title, justify="center"), style=panel_style))

def print_data(data):
    if data:
        status = data.get("status", "unsuccess")
        timestamp = data.get("timestamp", "")

        table = Table(title="Server Data")
        table.add_column("Key")
        table.add_column("Value")

        for key, value in data.items():
            if key == "area" and isinstance(value, dict):
                for area_key, area_value in value.items():
                    table.add_row(area_key, str(area_value))
            elif key == "coordinates" and isinstance(value, list):
                for idx, coord in enumerate(value):
                    coord_table = Table(box=None)
                    coord_table.add_column("Key", style="bold")
                    coord_table.add_column("Value")
                    for coord_key, coord_value in coord.items():
                        if isinstance(coord_value, dict):
                            for nested_key, nested_value in coord_value.items():
                                coord_table.add_row(
                                    nested_key, str(nested_value))
                        else:
                            coord_table.add_row(coord_key, str(coord_value))
                    table.add_row(f"Coordinate {idx+1}", coord_table)
            else:
                table.add_row(key, str(value))

        panel_style = "green" if status == "success" else "red"
        panel_title = f"Status: {status}"
        if timestamp:
            panel_title += f" | Timestamp: {timestamp}"
        console.print(Panel(table, title=panel_title, style=panel_style))
    else:
        console.print("[red]No data to display.[/red]")

def show_progress(task_description: str):
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task(task_description, total=None)
        for fact in FACTS:
            progress.update(task, description=f"{task_description} {fact}")
            time.sleep(1)  # Simulate loading time
            yield
        progress.stop()
