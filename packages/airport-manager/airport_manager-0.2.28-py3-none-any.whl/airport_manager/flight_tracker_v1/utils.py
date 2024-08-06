from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from datetime import datetime
from rich.prompt import Prompt
from airport_manager.utils import clear_console


console = Console()


def format_percentage(value):
    return f"{value * 100:.0f}%"


def print_weather_data(data):
    status = data.get("status", "unsuccess")
    timestamp = data.get("timestamp", "")
    weather = data.get("weather", {})

    def create_weather_table(weather):
        general_table = Table(box=box.MINIMAL)
        general_table.add_column("Metric", style="bold magenta")
        general_table.add_column("Value", style="bold cyan")

        general_metrics = [
            ("METAR", "metar"),
            ("QNH (hPa)", "qnh"),
            ("Humidity (%)", "humidity"),
            ("Pressure (hg)", "pressure.hg"),
            ("Pressure (hPa)", "pressure.hpa"),
            ("Flight Category", "flight.category"),
            ("Sky Condition", "sky.condition.text")
        ]

        for display_name, metric in general_metrics:
            keys = metric.split('.')
            value = weather
            for key in keys:
                value = value.get(key, "N/A")
                if value == "N/A":
                    break
            general_table.add_row(display_name, str(value))

        visibility_table = Table(box=box.MINIMAL)
        visibility_table.add_column("Metric", style="bold magenta")
        visibility_table.add_column("Value", style="bold cyan")

        visibility_metrics = [
            ("Visibility (km)", "sky.visibility.km"),
            ("Visibility (mi)", "sky.visibility.mi"),
            ("Visibility (nmi)", "sky.visibility.nmi"),
        ]

        for display_name, metric in visibility_metrics:
            keys = metric.split('.')
            value = weather
            for key in keys:
                value = value.get(key, "N/A")
                if value == "N/A":
                    break
            visibility_table.add_row(display_name, str(value))

        wind_table = Table(box=box.MINIMAL)
        wind_table.add_column("Metric", style="bold magenta")
        wind_table.add_column("Value", style="bold cyan")

        wind_metrics = [
            ("Wind Direction", "wind.direction.text"),
            ("Wind Speed (kmh)", "wind.speed.kmh"),
            ("Wind Speed (kts)", "wind.speed.kts"),
            ("Wind Speed (mph)", "wind.speed.mph")
        ]

        for display_name, metric in wind_metrics:
            keys = metric.split('.')
            value = weather
            for key in keys:
                value = value.get(key, "N/A")
                if value == "N/A":
                    break
            wind_table.add_row(display_name, str(value))

        temp_elevation_table = Table(box=box.MINIMAL)
        temp_elevation_table.add_column("Metric", style="bold magenta")
        temp_elevation_table.add_column("Value", style="bold cyan")

        temp_elevation_metrics = [
            ("Temperature (°C)", "temp.celsius"),
            ("Temperature (°F)", "temp.fahrenheit"),
            ("Dew Point (°C)", "dewpoint.celsius"),
            ("Dew Point (°F)", "dewpoint.fahrenheit"),
            ("Elevation (m)", "elevation.m"),
            ("Elevation (ft)", "elevation.ft"),
        ]

        for display_name, metric in temp_elevation_metrics:
            keys = metric.split('.')
            value = weather
            for key in keys:
                value = value.get(key, "N/A")
                if value == "N/A":
                    break
            temp_elevation_table.add_row(display_name, str(value))

        console.print(Panel(general_table, title="General Weather Data", title_align="left", style="bold blue"))
        console.print(Panel(visibility_table, title="Visibility Data", title_align="left", style="bold green"))
        console.print(Panel(wind_table, title="Wind Data", title_align="left", style="bold yellow"))
        console.print(Panel(temp_elevation_table, title="Temperature and Elevation Data", title_align="left", style="bold magenta"))

    if weather:
        create_weather_table(weather)


def print_flight_tracker_data(data):
    arrivals = data.get("arrivals", {})
    departures = data.get("departures", {})

    def create_live_table(arrivals_live, departures_live):
        table = Table(box=box.MINIMAL)
        table.add_column("Metric", style="bold magenta")
        table.add_column("Arrivals", style="bold cyan")
        table.add_column("Departures", style="bold cyan")

        metrics = [
            ("Index", "index"),
            ("Average Delay (min)", "averageDelayMin"),
            ("On-time Flights", "ontime"),
            ("Delayed Flights", "delayed"),
            ("Delayed %", "delayedPercentage"),
            ("Cancelled Flights", "cancelled"),
            ("Cancelled %", "cancelledPercentage"),
            ("Trend", "trend")
        ]
        
        for display_name, metric in metrics:
            arrivals_value = arrivals_live.get(metric, "N/A")
            departures_value = departures_live.get(metric, "N/A")
            if metric == "trend":
                arrivals_value = Text(arrivals_value, style="green" if arrivals_value == "up" else "red" if arrivals_value == "down" else "yellow")
                departures_value = Text(departures_value, style="green" if departures_value == "up" else "red" if departures_value == "down" else "yellow")
            elif metric.endswith("Percentage"):
                arrivals_value = format_percentage(arrivals_value)
                departures_value = format_percentage(departures_value)
            table.add_row(display_name, str(arrivals_value), str(departures_value))

        return Panel(table, title="Live Data", title_align="left", style="bold green")

    def create_metrics_table(arrivals_metrics, departures_metrics):
        table = Table(box=box.MINIMAL)
        table.add_column("Metric", style="bold magenta")
        table.add_column("Arrivals - Yesterday", style="bold cyan")
        table.add_column("Arrivals - Today", style="bold cyan")
        table.add_column("Arrivals - Tomorrow", style="bold cyan")
        table.add_column("Departures - Yesterday", style="bold cyan")
        table.add_column("Departures - Today", style="bold cyan")
        table.add_column("Departures - Tomorrow", style="bold cyan")

        metrics = [
            ("Total Flights", "total"),
            ("Delayed Flights", "delayed"),
            ("Delayed %", "delayedPercentage"),
            ("Cancelled Flights", "cancelled"),
            ("Cancelled %", "cancelledPercentage")
        ]
        
        for display_name, metric in metrics:
            row = [display_name]
            for period in ["yesterday", "today", "tomorrow"]:
                value = arrivals_metrics.get(period, {}).get(metric, "N/A")
                if metric.endswith("Percentage") and value != "N/A":
                    value = format_percentage(value)
                row.append(str(value))
            for period in ["yesterday", "today", "tomorrow"]:
                value = departures_metrics.get(period, {}).get(metric, "N/A")
                if metric.endswith("Percentage") and value != "N/A":
                    value = format_percentage(value)
                row.append(str(value))
            table.add_row(*row)

        return Panel(table, title="Arrivals and Departures Data", title_align="left", style="bold blue")

    if arrivals and departures:
        arrivals_live = arrivals.get("live", {})
        departures_live = departures.get("live", {})
        
        arrivals_metrics = {
            "yesterday": arrivals.get("yesterday", {}),
            "today": arrivals.get("today", {}),
            "tomorrow": arrivals.get("tomorrow", {})
        }

        departures_metrics = {
            "yesterday": departures.get("yesterday", {}),
            "today": departures.get("today", {}),
            "tomorrow": departures.get("tomorrow", {})
        }

        console.print(create_live_table(arrivals_live, departures_live))
        console.print(create_metrics_table(arrivals_metrics, departures_metrics))


def format_status(status):
    if "Landed" in status:
        return Text(status, style="bold green")
    elif "Estimated departure" in status or "departure" in status:
        return Text(status, style="bold yellow")
    else:
        return Text(status, style="bold red")


def print_flight_info(data):
    flights = data.get("flights", [])
    
    if not flights:
        console.print(Panel("No flight data available.", style="bold red"))
        return
    
    def create_flight_info_table(flights_batch, start_index):
        table = Table(box=box.MINIMAL)
        table.add_column("Date", style="bold magenta")
        table.add_column("From", style="bold cyan")
        table.add_column("To", style="bold cyan")
        table.add_column("Flight Number", style="bold green")
        table.add_column("Flight ID", style="orange_red1")
        table.add_column("Duration", style="bold yellow")
        table.add_column("STD", style="bold blue")
        table.add_column("ATD", style="bold blue")
        table.add_column("STA", style="bold blue")
        table.add_column("Status", style="bold red")
        
        for i, flight in enumerate(flights_batch, start=start_index):
            table.add_row(
                flight.get("date", "N/A"),
                flight.get("from", "N/A"),
                flight.get("to", "N/A"),
                flight.get("flight_number", "N/A"),
                flight.get("data_flight", "N/A"),
                flight.get("duration", "N/A"),
                flight.get("std", "N/A"),
                flight.get("atd", "N/A"),
                flight.get("sta", "N/A"),
                format_status(flight.get("status", "N/A"))
            )
        
        return table

    batch_size = 10
    start_index = 0
    while start_index < len(flights):
        batch = flights[start_index:start_index + batch_size]
        table = create_flight_info_table(batch, start_index + 1)
        console.print(Panel(table, title=f"Flight Data (Showing {start_index + 1}-{min(start_index + batch_size, len(flights))} of {len(flights)})", title_align="left", style="bold green"))
        start_index += batch_size
        if start_index < len(flights):
            choice = Prompt.ask("Press Enter to continue or type 'q' to quit", default="")
            clear_console()
            if choice.lower() == 'q':
                break


def print_flight_data(data, data_type: str):
    flights = data.get(data_type, [])
    total = data.get("total", 0)

    if not flights:
        console.print(Panel("No flight data available.", style="bold red"))
        return

    def create_flight_table(flights_batch, start_index):
        table = Table(box=box.MINIMAL)
        table.add_column("Flight Number", style="bold green")
        table.add_column("Flight ID", style="bold bright_yellow")

        if data_type == "departures":
            table.add_column("To", style="bold cyan")
        elif data_type == "arrivals":
            table.add_column("From", style="bold cyan")

        table.add_column("Scheduled Departure", style="bold blue")
        table.add_column("Scheduled Arrival", style="bold blue")
        if data_type != "ground":
            table.add_column("Status", style="bold red")
        table.add_column("Aircraft Model", style="bold yellow")
        table.add_column("Registration", style="bold magenta")
        
        for i, flight_info in enumerate(flights_batch, start=start_index):
            flight = flight_info.get("flight", {})
            ident = flight.get("identification", {})
            status = flight.get("status", {})
            aircraft = flight.get("aircraft", {})
            origin_info = flight.get("airport", {}).get("origin", {}).get("code", {})
            destination_info = flight.get("airport", {}).get("destination", {}).get("code", {})

            row_data = [
                ident.get("number", {}).get("default", "N/A"),
                str(ident.get("id", "N/A")),
            ]

            if data_type == "departures":
                row_data.append(f'{destination_info.get("iata", "N/A")}')
            elif data_type == "arrivals":
                row_data.append(f'{origin_info.get("iata", "N/A")}')

            row_data.extend([
                datetime.utcfromtimestamp(flight.get("time", {}).get("scheduled", {}).get("departure", 0)).strftime('%Y-%m-%d %H:%M:%S'),
                datetime.utcfromtimestamp(flight.get("time", {}).get("scheduled", {}).get("arrival", 0)).strftime('%Y-%m-%d %H:%M:%S'),
            ])

            if data_type != "ground":
                row_data.append(format_status(status.get("text", "N/A")))

            row_data.extend([
                aircraft.get("model", {}).get("text", "N/A"),
                aircraft.get("registration", "N/A"),
            ])
            
            table.add_row(*row_data)

        return table

    batch_size = 10
    start_index = 0
    while start_index < len(flights):
        batch = flights[start_index:start_index + batch_size]
        table = create_flight_table(batch, start_index + 1)
        console.print(Panel(table, title=f"{data_type.capitalize()} Data (Showing {start_index + 1}-{min(start_index + batch_size, len(flights))} of {total})", title_align="left", style="bold green"))
        start_index += batch_size
        if start_index < len(flights):
            choice = Prompt.ask("Press Enter to continue or type 'q' to quit", default="")
            clear_console()
            if choice.lower() == 'q':
                break


def format_datetime(timestamp):
    if timestamp:
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def print_flight_playback(data):
    flight = data.get("flight", {})
    
    if not flight:
        console.print(Panel("No flight data available.", style="bold red"))
        return

    identification = flight.get("identification", {})
    model = flight.get("model", {})
    status = flight.get("status", {})
    airline = flight.get("airline", {})
    airport = flight.get("airport", {})
    track = flight.get("track", [])

    flight_info_table = Table(box=box.MINIMAL)
    flight_info_table.add_column("Field", style="bold magenta")
    flight_info_table.add_column("Value", style="bold cyan")

    flight_info_table.add_row("Flight ID", identification.get("id", "N/A"))
    flight_info_table.add_row("Callsign", identification.get("callsign", "N/A"))
    flight_info_table.add_row("Aircraft Model", model.get("text", "N/A"))
    flight_info_table.add_row("Status", status.get("text", "N/A"))
    flight_info_table.add_row("Live", str(status.get("live", "N/A")))
    flight_info_table.add_row("Airline", airline.get("name", "N/A"))

    origin = airport.get("origin", {})
    destination = airport.get("destination", {})
    flight_info_table.add_row("Origin Airport", origin.get("name", "N/A"))
    flight_info_table.add_row("Origin IATA", origin.get("code", {}).get("iata", "N/A"))
    flight_info_table.add_row("Destination Airport", destination.get("name", "N/A"))
    flight_info_table.add_row("Destination IATA", destination.get("code", {}).get("iata", "N/A"))

    batch_size = 10
    start_index = 0
    total_tracks = len(track)

    while start_index < total_tracks:
        track_table = Table(box=box.MINIMAL)
        track_table.add_column("Timestamp", style="bold blue")
        track_table.add_column("Latitude", style="bold cyan")
        track_table.add_column("Longitude", style="bold cyan")
        track_table.add_column("Altitude (ft)", style="bold magenta")
        track_table.add_column("Speed (kmh)", style="bold yellow")
        track_table.add_column("Heading", style="bold red")

        end_index = start_index + batch_size
        for entry in track[start_index:end_index]:
            track_table.add_row(
                format_datetime(entry.get("timestamp")),
                str(entry.get("latitude", "N/A")),
                str(entry.get("longitude", "N/A")),
                str(entry.get("altitude", {}).get("feet", "N/A")),
                str(entry.get("speed", {}).get("kmh", "N/A")),
                str(entry.get("heading", "N/A"))
            )

        clear_console()
        console.print(Panel(flight_info_table, title="Flight Information", title_align="left", style="bold green"))
        console.print(Panel(track_table, title=f"Flight Track Data (Showing {start_index + 1}-{min(end_index, total_tracks)} of {total_tracks})", title_align="left", style="bold green"))
        
        start_index += batch_size
        if start_index < total_tracks:
            choice = input("Press Enter to continue or type 'q' to quit: ")
            if choice.lower() == 'q':
                break


