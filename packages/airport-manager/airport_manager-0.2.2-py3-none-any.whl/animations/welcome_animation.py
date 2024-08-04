import time
import sys
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout

console = Console()

def typewriter(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def welcome_animation():
    title = """
 █████╗ ██╗██████╗ ██████╗  ██████╗ ██████╗ ████████╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
██╔══██╗██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
███████║██║██████╔╝██████╔╝██║   ██║██████╔╝   ██║       ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
██╔══██║██║██╔══██╗██╔═══╝ ██║   ██║██╔══██╗   ██║       ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
██║  ██║██║██║  ██║██║     ╚██████╔╝██║  ██║   ██║       ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                                       
    """
    creator = "Created by Shubh Thorat"

    console.clear()
    with Live(console=console, refresh_per_second=10) as live:
        for i, message in enumerate([
            "\nInitializing...",
            "\nLoading modules...",
            "\nStarting services...",
            "\nReady to manage your airport data!",
        ]):
            panel = Panel(Text(title, style="bold green", justify="center"), border_style="green", subtitle=creator, subtitle_align="right")
            layout = Layout()
            layout.split(
                Layout(panel, name="top", size=12),
                Layout(Text(message, style="bold blue"), name="middle")
            )
            live.update(layout)
            time.sleep(2)  # Adjust the timing as needed

if __name__ == "__main__":
    welcome_animation()
