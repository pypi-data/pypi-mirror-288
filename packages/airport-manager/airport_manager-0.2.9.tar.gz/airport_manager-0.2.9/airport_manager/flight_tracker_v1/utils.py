from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

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


def print_flight_data(data):
    status = data.get("status", "unsuccess")
    timestamp = data.get("timestamp", "")
    
    if status != 'success':
        error_message = f"Status: {status} | Message: {data.get('message', '')} | Timestamp: {timestamp}"
        console.print(Panel(Text(error_message, justify="center"), style="red"))
        return
    
    flights = data.get("flights", [])
    
    table = Table(box=box.MINIMAL)
    table.add_column("Date", style="bold magenta")
    table.add_column("From", style="bold cyan")
    table.add_column("To", style="bold cyan")
    table.add_column("Flight Number", style="bold green")
    # table.add_column("Flight ID", style="orange_red1")
    table.add_column("Duration", style="bold yellow")
    table.add_column("STD", style="bold blue")
    table.add_column("ATD", style="bold blue")
    table.add_column("STA", style="bold blue")
    table.add_column("Status", style="bold red")
    
    for flight in flights:
        table.add_row(
            flight.get("date", "N/A"),
            flight.get("from", "N/A"),
            flight.get("to", "N/A"),
            flight.get("flight_number", "N/A"),
            # flight.get("data_flight", "N/A"),
            flight.get("duration", "N/A"),
            flight.get("std", "N/A"),
            flight.get("atd", "N/A"),
            flight.get("sta", "N/A"),
            format_status(flight.get("status", "N/A"))

        )
    
    console.print(Panel(table, title="Flight Data", title_align="left", style="bold green"))

