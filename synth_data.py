import pandas as pd
import numpy as np
import random
import os
import shutil
import time
from datetime import datetime, timedelta

# Helper function to select random event types and their details
def random_event_type():
    types = [
        ("Temperature", "°C", "Waste heat capture at furnace outlet", "Active", "Furnace in operation"),
        ("Pressure", "bar", "Pressure buildup in recovery system", "Warning", "Increased throughput demand"),
        ("Efficiency", "%", "Heat recovery efficiency drop", "Alert", "Heat exchanger fouling"),
        ("Energy Reclaim", "kWh", "Energy transferred to process stream", "Completed", "Scheduled daily cycle"),
        ("CO₂ Reduction", "kg", "Greenhouse gas reduction logged", "Logged", "Automated monitoring")
    ]
    return random.choice(types)

# Define sensor sources and IDs
sources = [
    ("HeatExchanger01", "S001"),
    ("PumpStation01", "S002"),
    ("ControlUnit01", "S003"),
    ("RecoveryUnit02", "S004"),
    ("MonitorSystem01", "S005")
]

# Configuration
start_time = datetime(2025, 9, 13, 8, 0, 0)
interval = timedelta(minutes=5)
n_rows = 20

# Generate Events Dataset
events = []
for i in range(n_rows):
    t = start_time + interval * i
    e_type, units, description, status, reason = random_event_type()
    source, sensor_id = random.choice(sources)
    # Generate plausible values based on event type
    if e_type == "Temperature":
        value = np.random.normal(425, 10)
    elif e_type == "Pressure":
        value = np.random.normal(3.2, 0.2)
    elif e_type == "Efficiency":
        value = np.random.normal(80, 5)
    elif e_type == "Energy Reclaim":
        value = np.random.normal(250, 20)
    elif e_type == "CO₂ Reduction":
        value = np.random.normal(56, 10)
    number = 100 + i
    events.append([
        t.strftime("%Y-%m-%d %H:%M:%S"),
        e_type,
        round(value, 2),
        units,
        description,
        status,
        reason,
        sensor_id,
        number,
        source
    ])

events_df = pd.DataFrame(events, columns=[
    "Time",
    "Event Type",
    "Value",
    "Units",
    "Event Description",
    "Status",
    "Reason",
    "Sensor Id",
    "Number",
    "Source"
])

# Generate Sensors Dataset (using just 2 sensors for this example)
sensor_names = [f"{src}.{s_id}" for src, s_id in sources[:2]]  # Adjust to include more sensors
sensors = []
for i in range(n_rows):
    t = start_time + interval * i
    temp = np.random.normal(425, 6)  # HeatExchanger01.S001
    pressure = np.random.normal(3.2, 0.15)  # PumpStation01.S002
    sensors.append([
        t.strftime("%Y-%m-%d %H:%M:%S"),
        round(temp, 2),
        round(pressure, 3)
    ])

sensors_df = pd.DataFrame(sensors, columns=["Time"] + sensor_names)

def archive_existing_files():
    """Archive existing CSV files with timestamp"""
    data_dir = "data"
    archive_dir = "data/archive"
    
    # Ensure archive directory exists
    os.makedirs(archive_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Archive existing files if they exist
    for filename in ["events.csv", "sensors.csv"]:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            # Create archived filename with timestamp
            name, ext = os.path.splitext(filename)
            archived_filename = f"{name}_{timestamp}{ext}"
            archived_filepath = os.path.join(archive_dir, archived_filename)
            
            # Move file to archive
            shutil.move(filepath, archived_filepath)
            print(f"Archived {filename} to {archived_filename}")

def generate_and_save_data():
    """Generate new data and save to CSV files"""
    # Archive existing files first
    archive_existing_files()
    
    # Generate new data (using existing logic)
    events = []
    for i in range(n_rows):
        t = start_time + interval * i
        e_type, units, description, status, reason = random_event_type()
        source, sensor_id = random.choice(sources)
        # Generate plausible values based on event type
        if e_type == "Temperature":
            value = np.random.normal(425, 10)
        elif e_type == "Pressure":
            value = np.random.normal(3.2, 0.2)
        elif e_type == "Efficiency":
            value = np.random.normal(80, 5)
        elif e_type == "Energy Reclaim":
            value = np.random.normal(250, 20)
        elif e_type == "CO₂ Reduction":
            value = np.random.normal(56, 10)
        number = 100 + i
        events.append([
            t.strftime("%Y-%m-%d %H:%M:%S"),
            e_type,
            round(value, 2),
            units,
            description,
            status,
            reason,
            sensor_id,
            number,
            source
        ])

    events_df = pd.DataFrame(events, columns=[
        "Time",
        "Event Type",
        "Value",
        "Units",
        "Event Description",
        "Status",
        "Reason",
        "Sensor Id",
        "Number",
        "Source"
    ])

    # Generate Sensors Dataset
    sensor_names = [f"{src}.{s_id}" for src, s_id in sources[:2]]
    sensors = []
    for i in range(n_rows):
        t = start_time + interval * i
        temp = np.random.normal(425, 6)  # HeatExchanger01.S001
        pressure = np.random.normal(3.2, 0.15)  # PumpStation01.S002
        sensors.append([
            t.strftime("%Y-%m-%d %H:%M:%S"),
            round(temp, 2),
            round(pressure, 3)
        ])

    sensors_df = pd.DataFrame(sensors, columns=["Time"] + sensor_names)

    # Save to CSV in data folder
    events_df.to_csv("data/events.csv", index=False)
    sensors_df.to_csv("data/sensors.csv", index=False)

    print(f"Generated new events.csv and sensors.csv at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def run_continuous_generation():
    """Run the data generation continuously every 30 seconds"""
    print("Starting continuous data generation (every 30 seconds)")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Update start_time to current time for realistic timestamps
            global start_time
            start_time = datetime.now()
            
            generate_and_save_data()
            
            # Wait 30 seconds
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nStopping data generation...")

if __name__ == "__main__":
    # Run continuous generation
    run_continuous_generation()
