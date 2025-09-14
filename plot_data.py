import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import os
import shutil

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    """Load the CSV data files"""
    try:
        events_df = pd.read_csv('data/events.csv')
        sensors_df = pd.read_csv('data/sensors.csv')
        
        # Convert time columns to datetime
        events_df['Time'] = pd.to_datetime(events_df['Time'])
        sensors_df['Time'] = pd.to_datetime(sensors_df['Time'])
        
        return events_df, sensors_df
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return None, None

def plot_sensor_timeseries(sensors_df):
    """Plot sensor data as time series"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Temperature plot
    ax1.plot(sensors_df['Time'], sensors_df['HeatExchanger01.S001'], 
             marker='o', linewidth=2, markersize=4, label='HeatExchanger01.S001')
    ax1.set_title('Temperature Sensor Data Over Time', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Temperature (°C)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Pressure plot
    ax2.plot(sensors_df['Time'], sensors_df['PumpStation01.S002'], 
             marker='s', linewidth=2, markersize=4, color='orange', label='PumpStation01.S002')
    ax2.set_title('Pressure Sensor Data Over Time', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Pressure (bar)', fontsize=12)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.xticks(rotation=45)
    return fig

def plot_events_by_type(events_df):
    """Plot events data grouped by event type"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    event_types = events_df['Event Type'].unique()
    
    for i, event_type in enumerate(event_types):
        if i < len(axes):
            event_data = events_df[events_df['Event Type'] == event_type]
            
            axes[i].plot(event_data['Time'], event_data['Value'], 
                        marker='o', linewidth=2, markersize=5)
            axes[i].set_title(f'{event_type}', fontsize=12, fontweight='bold')
            
            # Get units for y-label
            units = event_data['Units'].iloc[0] if len(event_data) > 0 else ''
            axes[i].set_ylabel(f'Value ({units})', fontsize=10)
            axes[i].grid(True, alpha=0.3)
            axes[i].tick_params(axis='x', rotation=45)
    
    # Hide unused subplots
    for i in range(len(event_types), len(axes)):
        axes[i].set_visible(False)
    
    plt.suptitle('Events Data by Type Over Time', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

def plot_events_distribution(events_df):
    """Plot distribution of event types and statuses"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Event type distribution
    event_counts = events_df['Event Type'].value_counts()
    ax1.pie(event_counts.values, labels=event_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Distribution of Event Types', fontsize=14, fontweight='bold')
    
    # Status distribution
    status_counts = events_df['Status'].value_counts()
    colors = sns.color_palette("Set2", len(status_counts))
    ax2.bar(status_counts.index, status_counts.values, color=colors)
    ax2.set_title('Event Status Distribution', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Count', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def plot_correlation_heatmap(events_df):
    """Plot correlation heatmap for numerical event data"""
    # Create pivot table for numerical analysis
    pivot_data = events_df.pivot_table(
        values='Value', 
        index='Time', 
        columns='Event Type', 
        aggfunc='mean'
    )
    
    # Calculate correlation matrix
    corr_matrix = pivot_data.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, ax=ax, cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Matrix of Event Types', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_culprit_signals_plot(events_df, sensors_df):
    """Create a plot similar to the culprit_signals example image"""
    # Set up the figure with multiple subplots
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))
    fig.suptitle('Culprit Signals Analysis - Industrial Process Monitoring', fontsize=16, fontweight='bold')
    
    # Color palette for consistency
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Plot 1: Temperature sensor data
    ax1 = axes[0, 0]
    ax1.plot(sensors_df['Time'], sensors_df['HeatExchanger01.S001'], 
             color=colors[0], linewidth=2, marker='o', markersize=3)
    ax1.set_title('Temperature - HeatExchanger01.S001', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Temperature (°C)', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45, labelsize=8)
    
    # Plot 2: Pressure sensor data
    ax2 = axes[0, 1]
    ax2.plot(sensors_df['Time'], sensors_df['PumpStation01.S002'], 
             color=colors[1], linewidth=2, marker='s', markersize=3)
    ax2.set_title('Pressure - PumpStation01.S002', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Pressure (bar)', fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45, labelsize=8)
    
    # Plot 3: Temperature events
    temp_events = events_df[events_df['Event Type'] == 'Temperature']
    ax3 = axes[1, 0]
    if not temp_events.empty:
        ax3.plot(temp_events['Time'], temp_events['Value'], 
                 color=colors[2], linewidth=2, marker='d', markersize=4)
    ax3.set_title('Temperature Events', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Temperature (°C)', fontsize=10)
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=45, labelsize=8)
    
    # Plot 4: Efficiency events
    eff_events = events_df[events_df['Event Type'] == 'Efficiency']
    ax4 = axes[1, 1]
    if not eff_events.empty:
        ax4.plot(eff_events['Time'], eff_events['Value'], 
                 color=colors[3], linewidth=2, marker='^', markersize=4)
    ax4.set_title('Heat Recovery Efficiency', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Efficiency (%)', fontsize=10)
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(axis='x', rotation=45, labelsize=8)
    
    # Plot 5: Energy Reclaim events
    energy_events = events_df[events_df['Event Type'] == 'Energy Reclaim']
    ax5 = axes[2, 0]
    if not energy_events.empty:
        ax5.plot(energy_events['Time'], energy_events['Value'], 
                 color=colors[4], linewidth=2, marker='v', markersize=4)
    ax5.set_title('Energy Reclaim', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Energy (kWh)', fontsize=10)
    ax5.grid(True, alpha=0.3)
    ax5.tick_params(axis='x', rotation=45, labelsize=8)
    ax5.set_xlabel('Time', fontsize=10)
    
    # Plot 6: CO₂ Reduction events
    co2_events = events_df[events_df['Event Type'] == 'CO₂ Reduction']
    ax6 = axes[2, 1]
    if not co2_events.empty:
        ax6.plot(co2_events['Time'], co2_events['Value'], 
                 color=colors[5], linewidth=2, marker='*', markersize=5)
    ax6.set_title('CO₂ Reduction', fontsize=12, fontweight='bold')
    ax6.set_ylabel('CO₂ Reduction (kg)', fontsize=10)
    ax6.grid(True, alpha=0.3)
    ax6.tick_params(axis='x', rotation=45, labelsize=8)
    ax6.set_xlabel('Time', fontsize=10)
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    
    return fig

def archive_existing_plot():
    """Archive existing plot file with timestamp"""
    images_dir = "images"
    archive_dir = "images/archive"
    
    # Ensure archive directory exists
    os.makedirs(archive_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Archive existing plot if it exists
    filename = "culprit_signals_analysis.png"
    filepath = os.path.join(images_dir, filename)
    if os.path.exists(filepath):
        # Create archived filename with timestamp
        name, ext = os.path.splitext(filename)
        archived_filename = f"{name}_{timestamp}{ext}"
        archived_filepath = os.path.join(archive_dir, archived_filename)
        
        # Move file to archive
        shutil.move(filepath, archived_filepath)
        print(f"Archived {filename} to {archived_filename}")

def create_dashboard():
    """Create only the culprit signals analysis plot"""
    events_df, sensors_df = load_data()
    
    if events_df is None or sensors_df is None:
        print("Could not load data files. Make sure events.csv and sensors.csv exist in the data folder.")
        return
    
    print(f"Loaded {len(events_df)} events and {len(sensors_df)} sensor readings")
    
    # Archive existing plot first
    archive_existing_plot()
    
    # Create the culprit signals plot (similar to example image)
    print("Creating culprit signals plot...")
    fig_culprit = create_culprit_signals_plot(events_df, sensors_df)
    fig_culprit.savefig('images/culprit_signals_analysis.png', dpi=300, bbox_inches='tight')
    
    # Close the figure to free memory and prevent showing
    plt.close(fig_culprit)
    
    print(f"New plot saved: images/culprit_signals_analysis.png at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    create_dashboard()