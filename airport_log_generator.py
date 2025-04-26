#!/usr/bin/env python3
import json
import logging
import os
import random
import time
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
LOGS_DIR = "/app/logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Airport codes and names
AIRPORTS = {
    "JFK": "New York JFK",
    "LAX": "Los Angeles",
    "ORD": "Chicago O'Hare",
    "LHR": "London Heathrow",
    "CDG": "Paris Charles de Gaulle",
    "DXB": "Dubai International",
    "HND": "Tokyo Haneda",
    "SIN": "Singapore Changi"
}

# Airlines (two-letter codes)
AIRLINES = ["AA", "DL", "UA", "BA", "LH", "EK", "JL", "SQ", "AF", "KL", "QF", "CX", "TK", "AI", "LX", "OS", "IB", "AZ"]

# Flight statuses
FLIGHT_STATUSES = ["On Time", "Boarding", "Delayed", "Departed", "Arrived", "Cancelled", "Diverted"]

# Weather conditions
WEATHER_CONDITIONS = ["Clear", "Cloudy", "Rain", "Snow", "Fog", "Thunderstorm", "Windy", "Hail"]

# Log levels with weighted probabilities
LOG_LEVELS = ["INFO", "INFO", "INFO", "INFO", "WARN", "WARN", "ERROR", "DEBUG", "DEBUG"]

def generate_flight_number():
    """Generate a random flight number"""
    airline = random.choice(AIRLINES)
    number = random.randint(1000, 9999)
    return f"{airline}{number}"

def generate_timestamp():
    """Generate current timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()

def generate_flight_update():
    """Generate a flight update log entry"""
    airport = random.choice(list(AIRPORTS.keys()))
    flight = generate_flight_number()
    status = random.choice(FLIGHT_STATUSES)
    destination = random.choice([a for a in AIRPORTS.keys() if a != airport])

    level = "INFO"
    if status == "Delayed":
        level = "WARN"
        delay = random.randint(15, 180)
        message = f"Flight {flight} to {destination} is {status} by {delay} minutes"
    elif status == "Cancelled":
        level = "ERROR"
        message = f"Flight {flight} to {destination} is {status} due to operational issues"
    elif status == "Diverted":
        level = "WARN"
        message = f"Flight {flight} to {destination} is {status} to {random.choice([a for a in AIRPORTS.keys() if a != airport and a != destination])}"
    else:
        message = f"Flight {flight} to {destination} is {status}"

    return {
        "timestamp": generate_timestamp(),
        "level": level,
        "message": message,
        "airport": airport,
        "flight": flight,
        "event": "flight_update"
    }

def generate_passenger_activity():
    """Generate a passenger activity log entry"""
    airport = random.choice(list(AIRPORTS.keys()))
    flight = generate_flight_number()
    passenger_count = random.randint(1, 200)

    activities = ["checked in", "boarding", "deplaned", "connecting"]
    activity = random.choice(activities)

    message = f"{passenger_count} passengers {activity} for flight {flight}"

    return {
        "timestamp": generate_timestamp(),
        "level": "INFO",
        "message": message,
        "airport": airport,
        "flight": flight,
        "event": "passenger_activity"
    }

def generate_security_event():
    """Generate a security-related log entry"""
    airport = random.choice(list(AIRPORTS.keys()))
    terminal = random.randint(1, 5)

    events = [
        ("INFO", "Security Checkpoint Opened"),
        ("INFO", "Security Checkpoint Closed"),
        ("INFO", "Security Drill"),
        ("INFO", "Baggage Inspection"),
        ("WARN", "Prohibited Item Found"),
        ("WARN", "Unattended Baggage"),
        ("ERROR", "Security Alert")
    ]

    level, event_type = random.choice(events)
    message = f"Security: {event_type} at {airport} terminal {terminal}"

    return {
        "timestamp": generate_timestamp(),
        "level": level,
        "message": message,
        "airport": airport,
        "event": "security"
    }

def generate_baggage_event():
    """Generate a baggage-related log entry"""
    airport = random.choice(list(AIRPORTS.keys()))
    flight = generate_flight_number()

    events = [
        ("INFO", "Baggage Loaded"),
        ("INFO", "Baggage Unloaded"),
        ("INFO", "Baggage Transferred"),
        ("WARN", "Baggage Delayed"),
        ("ERROR", "Baggage Lost")
    ]

    level, event_type = random.choice(events)
    message = f"Baggage: {event_type} for flight {flight}"

    return {
        "timestamp": generate_timestamp(),
        "level": level,
        "message": message,
        "airport": airport,
        "flight": flight,
        "event": "baggage"
    }

def generate_weather_event():
    """Generate a weather-related log entry"""
    airport = random.choice(list(AIRPORTS.keys()))
    condition = random.choice(WEATHER_CONDITIONS)
    visibility = random.randint(1, 10)

    level = "INFO"
    if condition in ["Snow", "Fog", "Thunderstorm", "Hail"]:
        level = "WARN"
        message = f"Weather at {airport}: {condition}, visibility {visibility} km, flights may be delayed"
    else:
        message = f"Weather at {airport}: {condition}, visibility {visibility} km"

    return {
        "timestamp": generate_timestamp(),
        "level": level,
        "message": message,
        "airport": airport,
        "event": "weather"
    }

def generate_log_entry():
    """Generate a random log entry"""
    generators = [
        generate_flight_update,
        generate_passenger_activity,
        generate_security_event,
        generate_baggage_event,
        generate_weather_event
    ]

    # Weighted selection to make flight updates more common
    weights = [0.4, 0.2, 0.1, 0.2, 0.1]
    generator = random.choices(generators, weights=weights, k=1)[0]

    return generator()

def write_log_entry(log_entry):
    """Write a log entry to the appropriate log file"""
    log_file = os.path.join(LOGS_DIR, "airport.log")

    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    logger.info(f"Generated log: {log_entry['message']}")

def main():
    """Main function to generate logs continuously"""
    logger.info("Starting airport log generator")

    try:
        while True:
            # Generate between 1-3 log entries
            for _ in range(random.randint(1, 3)):
                log_entry = generate_log_entry()
                write_log_entry(log_entry)

            # Sleep for a random interval between 1-5 seconds
            time.sleep(random.uniform(1, 5))
    except KeyboardInterrupt:
        logger.info("Stopping airport log generator")

if __name__ == "__main__":
    main()
