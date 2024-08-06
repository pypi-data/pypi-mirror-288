import time
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from animations.banner import display_banner
from airport_manager.utils import show_progress

console = Console()

def welcome_animation():
    messages = [
        "Initializing...",
        "Loading modules...",
        "Starting services...",
        "Ready to manage your airport data!"
    ]

    console.clear()
    display_banner()  # Display banner first

    progress_gen = show_progress("Welcome to Airport Manager:", messages)
    with Live(console=console, screen=False, auto_refresh=False) as live:
        for _ in progress_gen:
            console.clear()  # Clear console on each iteration
            display_banner()  # Display banner again
            live.update(Text(f"Welcome to Airport Manager: {_}", style="bold blue"))
            time.sleep(1)  # Adjust the timing as needed

