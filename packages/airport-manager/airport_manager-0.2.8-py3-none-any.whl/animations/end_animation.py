import time
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
import sys
from rich.panel import Panel
from rich.layout import Layout

console = Console()


def typewriter(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def end_animation():
    farewell_title = """
 ███████╗██╗███████╗████████╗    ██╗      █████╗ ██████╗ ██╗   ██╗██╗   ██╗
 ██╔════╝██║██╔════╝╚══██╔══╝    ██║     ██╔══██╗██╔══██╗██║   ██║╚██╗ ██╔╝
 ███████╗██║█████╗     ██║       ██║     ███████║██████╔╝██║   ██║ ╚████╔╝ 
 ╚════██║██║██╔══╝     ██║       ██║     ██╔══██║██╔══██╗██║   ██║  ╚██╔╝  
 ███████║██║██║        ██║       ███████╗██║  ██║██████╔╝╚██████╔╝   ██║   
 ╚══════╝╚═╝╚═╝        ╚═╝       ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   
                                                                          
    """
    creator = "Thank you for using Airport Manager CLI"

    console.clear()
    panel = Panel(Text(farewell_title, style="bold green", justify="center"),
                  border_style="green", subtitle=creator, subtitle_align="right")
    layout = Layout()
    layout.split(
        Layout(panel, name="top", size=12),
        Layout(name="middle")
    )

    with Live(console=console, refresh_per_second=10) as live:
        for i, message in enumerate([
            "\nSaving your data...",
            "\nClosing services...",
            "\nGoodbye!",
        ]):
            panel = Panel(Text(farewell_title, style="bold green", justify="center"), border_style="green", subtitle=creator, subtitle_align="right")
            layout = Layout()
            layout.split(
                Layout(panel, name="top", size=12),
                Layout(Text(message, style="bold blue"), name="middle")
            )
            live.update(layout)
            time.sleep(2)  # Adjust the timing as needed
    
    console.clear()