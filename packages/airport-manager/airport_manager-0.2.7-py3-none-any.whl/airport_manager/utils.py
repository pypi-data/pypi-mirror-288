from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


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
