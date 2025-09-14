#!/usr/bin/env python3
"""
Streamlit Web UI for Industrial Process Monitoring Pipeline
Beautiful version with enhanced AI Analysis section - All warnings fixed
"""

import streamlit as st
import time
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import glob
import re

# Import our pipeline modules
from synth_data import generate_and_save_data
from plot_data import create_dashboard
from pipeline import run_plot_analysis, save_analysis_report

# Configure Streamlit page
st.set_page_config(
    page_title="Industrial Process Monitor",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hide deprecation warnings */
    .stDeprecationWarning {
        display: none;
    }
    
    /* AI Analysis Section Styling */
    .ai-analysis-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px 10px 0 0;
        margin-bottom: 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .ai-analysis-container {
        background: white;
        border-radius: 0 0 10px 10px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #667eea;
        margin-top: -5px;
    }
    
    .analysis-highlight {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .anomaly-card {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .anomaly-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .critical-badge {
        background: linear-gradient(135deg, #f93b1d 0%, #ea1e63 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .warning-badge {
        background: linear-gradient(135deg, #f7b731 0%, #ea8d1e 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .info-badge {
        background: linear-gradient(135deg, #5ca0f2 0%, #4c84ff 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    .analysis-section {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .section-title {
        color: #667eea;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.25rem;
    }
    
    /* Animation for new analysis */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .new-analysis-alert {
        animation: pulse 2s infinite;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    /* Scrollbar styling for analysis text */
    .stTextArea textarea {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 13px;
        line-height: 1.5;
        background: #f8f9fa;
        border: 1px solid #667eea30;
    }
    
    .stTextArea textarea::-webkit-scrollbar {
        width: 8px;
    }
    
    .stTextArea textarea::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .stTextArea textarea::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'cycle_count' not in st.session_state:
    st.session_state.cycle_count = 0
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = ""
if 'status_messages' not in st.session_state:
    st.session_state.status_messages = []
if 'last_cycle_time' not in st.session_state:
    st.session_state.last_cycle_time = None
if 'next_cycle_time' not in st.session_state:
    st.session_state.next_cycle_time = None
if 'cycle_in_progress' not in st.session_state:
    st.session_state.cycle_in_progress = False
if 'new_analysis_flag' not in st.session_state:
    st.session_state.new_analysis_flag = False

def add_status_message(message, msg_type="info"):
    """Add a status message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.status_messages.append({
        "time": timestamp,
        "message": message,
        "type": msg_type
    })
    if len(st.session_state.status_messages) > 10:
        st.session_state.status_messages.pop(0)

def force_load_analysis():
    """Force load analysis from file system"""
    analysis_text = ""
    
    # Try main file first
    if os.path.exists('analysis/analysis_report.txt'):
        try:
            with open('analysis/analysis_report.txt', 'r', encoding='utf-8') as f:
                content = f.read()
                analysis_text = content
        except Exception as e:
            print(f"Error reading main file: {e}")
    
    # If main file doesn't exist or is empty, try archive
    if not analysis_text and os.path.exists('analysis/archive'):
        archives = glob.glob('analysis/archive/analysis_report_*.txt')
        if archives:
            latest = max(archives, key=os.path.getctime)
            try:
                with open(latest, 'r', encoding='utf-8') as f:
                    content = f.read()
                    analysis_text = content
            except Exception as e:
                print(f"Error reading archive: {e}")
    
    return analysis_text if analysis_text else None

def format_analysis_beautifully(analysis_text):
    """Format the analysis text into a beautiful HTML display"""
    if not analysis_text:
        return None
    
    # Parse different sections of the analysis
    sections = {
        'anomalies': [],
        'recommendations': [],
        'metrics': [],
        'summary': ''
    }
    
    # Extract key information using patterns
    lines = analysis_text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect sections
        if 'anomal' in line.lower() or 'critical' in line.lower() or 'warning' in line.lower():
            current_section = 'anomalies'
        elif 'recommend' in line.lower() or 'action' in line.lower():
            current_section = 'recommendations'
        elif 'metric' in line.lower() or 'efficiency' in line.lower():
            current_section = 'metrics'
        
        # Add to appropriate section
        if current_section == 'anomalies' and ('sensor' in line.lower() or 'temperature' in line.lower() or 'pressure' in line.lower()):
            sections['anomalies'].append(line)
        elif current_section == 'recommendations' and line.startswith('-') or line.startswith('•'):
            sections['recommendations'].append(line)
        elif current_section == 'metrics' and any(char.isdigit() for char in line):
            sections['metrics'].append(line)
    
    return sections

def display_beautiful_analysis(analysis_text):
    """Display analysis in a beautiful formatted way"""
    
    # Header with gradient
    st.markdown("""
    <div class="ai-analysis-header">
        <h2 style="margin: 0; display: flex; align-items: center;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">🤖</span>
            AI Analysis Results
        </h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">
            Powered by Advanced Anomaly Detection
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if new analysis
    if st.session_state.new_analysis_flag:
        st.markdown("""
        <div class="new-analysis-alert">
            🆕 NEW ANALYSIS AVAILABLE - Fresh insights detected!
        </div>
        """, unsafe_allow_html=True)
        if st.button("Dismiss Alert", key="dismiss_new"):
            st.session_state.new_analysis_flag = False
            st.rerun()
    
    # Main analysis container
    st.markdown('<div class="ai-analysis-container">', unsafe_allow_html=True)
    
    # Try to format the analysis beautifully
    formatted = format_analysis_beautifully(analysis_text)
    
    if formatted:
        # Display key metrics in cards
        col1, col2, col3 = st.columns(3)
        
        # Extract numbers from analysis for metrics
        numbers = re.findall(r'\d+\.?\d*', analysis_text)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}°C</div>
                <div class="metric-label">Peak Temperature</div>
            </div>
            """.format(numbers[0] if numbers else "N/A"), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}%</div>
                <div class="metric-label">System Efficiency</div>
            </div>
            """.format(numbers[1] if len(numbers) > 1 else "N/A"), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Anomalies Detected</div>
            </div>
            """.format(len(formatted['anomalies'])), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display formatted sections
        if formatted['anomalies']:
            st.markdown('<div class="section-title">🔍 Detected Anomalies</div>', unsafe_allow_html=True)
            for anomaly in formatted['anomalies'][:3]:  # Show top 3
                severity = "critical" if "critical" in anomaly.lower() else "warning" if "warning" in anomaly.lower() else "info"
                badge_class = f"{severity}-badge"
                st.markdown(f"""
                <div class="anomaly-card">
                    <span class="{badge_class}">{severity.upper()}</span>
                    {anomaly}
                </div>
                """, unsafe_allow_html=True)
        
        if formatted['recommendations']:
            st.markdown('<div class="section-title">💡 Recommendations</div>', unsafe_allow_html=True)
            for rec in formatted['recommendations'][:3]:
                st.markdown(f"""
                <div class="analysis-highlight">
                    {rec}
                </div>
                """, unsafe_allow_html=True)
    
    # Full analysis in expandable section
    with st.expander("📄 View Complete Analysis Report", expanded=False):
        st.text_area(
            "Full Analysis",
            value=analysis_text,
            height=400,
            disabled=True,
            label_visibility="collapsed"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Analysis", use_container_width=True):
            new_analysis = force_load_analysis()
            if new_analysis:
                st.session_state.last_analysis = new_analysis
                st.session_state.new_analysis_flag = True
                st.rerun()
    
    with col2:
        if st.button("📊 Export Report", use_container_width=True):
            st.download_button(
                label="Download Analysis",
                data=analysis_text,
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

def run_single_cycle():
    """Run a single monitoring cycle"""
    try:
        st.session_state.cycle_in_progress = True
        st.session_state.cycle_count += 1
        
        # Show progress
        progress_container = st.container()
        with progress_container:
            st.info(f"🔄 Running Cycle #{st.session_state.cycle_count}...")
            progress_bar = st.progress(0)
        
        # Step 1: Generate data
        add_status_message(f"📊 Cycle {st.session_state.cycle_count}: Generating data", "info")
        generate_and_save_data()
        progress_bar.progress(33)
        
        # Step 2: Create visualization
        add_status_message(f"📈 Cycle {st.session_state.cycle_count}: Creating visualization", "info")
        create_dashboard()
        progress_bar.progress(66)
        
        # Step 3: Run AI analysis
        add_status_message(f"🤖 Cycle {st.session_state.cycle_count}: Running AI analysis", "info")
        analysis_result = run_plot_analysis()
        progress_bar.progress(100)
        
        if analysis_result:
            save_analysis_report(analysis_result, save_to_analysis_folder=True)
            add_status_message(f"✅ Cycle {st.session_state.cycle_count} completed!", "success")
            st.session_state.new_analysis_flag = True
        else:
            add_status_message(f"⚠️ Cycle {st.session_state.cycle_count} completed (no analysis)", "warning")
        
        # Force load the analysis
        time.sleep(1)
        st.session_state.last_analysis = force_load_analysis()
        
        # Set timings
        st.session_state.last_cycle_time = datetime.now()
        st.session_state.next_cycle_time = datetime.now() + timedelta(seconds=30)
        
        # Clear progress
        progress_container.empty()
        
    except Exception as e:
        st.error(f"Error in cycle: {str(e)}")
        add_status_message(f"❌ Error: {str(e)}", "error")
    finally:
        st.session_state.cycle_in_progress = False

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; background: linear-gradient(90deg, #1f77b4, #ff7f0e); color: white; border-radius: 10px; margin-bottom: 2rem;">
        <h1>🏭 Industrial Process Monitoring</h1>
        <p style="margin: 0; font-size: 1.2rem;">Real-time Waste Heat Recovery System Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load analysis on startup if not loaded
    if not st.session_state.last_analysis:
        st.session_state.last_analysis = force_load_analysis()
    
    # Control Panel
    col1, col2, col3, col4 = st.columns([2, 2, 2, 4])
    
    with col1:
        if st.button("🚀 Start Monitoring", type="primary", disabled=st.session_state.monitoring):
            st.session_state.monitoring = True
            st.session_state.status_messages = []
            add_status_message("🚀 Monitoring started", "success")
            st.rerun()
    
    with col2:
        if st.button("🛑 Stop Monitoring", type="secondary", disabled=not st.session_state.monitoring):
            st.session_state.monitoring = False
            st.session_state.next_cycle_time = None
            add_status_message("🛑 Monitoring stopped", "info")
            st.rerun()
    
    with col3:
        if st.session_state.monitoring:
            if st.session_state.cycle_in_progress:
                st.markdown("🟡 **RUNNING**")
            else:
                st.markdown("🟢 **MONITORING ACTIVE**")
        else:
            st.markdown("🔴 **STOPPED**")
    
    with col4:
        if st.session_state.monitoring:
            st.markdown(f"**Cycle:** {st.session_state.cycle_count} | **Interval:** 30 seconds")
            if st.session_state.next_cycle_time and not st.session_state.cycle_in_progress:
                remaining = (st.session_state.next_cycle_time - datetime.now()).total_seconds()
                if remaining > 0:
                    st.markdown(f"**Next cycle:** {int(remaining)}s")
                else:
                    st.markdown("**Next cycle:** Starting...")
    
    st.markdown("---")
    
    # Run cycle if needed
    if st.session_state.monitoring and not st.session_state.cycle_in_progress:
        if not st.session_state.next_cycle_time or datetime.now() >= st.session_state.next_cycle_time:
            run_single_cycle()
            st.rerun()
    
    # Main content - 3 columns with adjusted widths
    col_left, col_center, col_right = st.columns([1, 1.5, 1.5])
    
    with col_left:
        st.subheader("📊 System Status")
        
        # Recent messages
        if st.session_state.status_messages:
            for msg in reversed(st.session_state.status_messages[-5:]):
                if msg["type"] == "success":
                    st.success(f"[{msg['time']}] {msg['message']}")
                elif msg["type"] == "warning":
                    st.warning(f"[{msg['time']}] {msg['message']}")
                elif msg["type"] == "error":
                    st.error(f"[{msg['time']}] {msg['message']}")
                else:
                    st.info(f"[{msg['time']}] {msg['message']}")
        else:
            st.info("Ready to start monitoring")
        
        # Metrics
        if os.path.exists('data/events.csv'):
            try:
                events_df = pd.read_csv('data/events.csv')
                sensors_df = pd.read_csv('data/sensors.csv')
                st.metric("Events", len(events_df))
                st.metric("Sensors", len(sensors_df))
            except:
                pass
    
    with col_center:
        st.subheader("📈 Visualization")
        
        # Show plot if exists - FIXED: using use_container_width instead of use_column_width
        if os.path.exists('images/culprit_signals_analysis.png'):
            st.image('images/culprit_signals_analysis.png', use_container_width=True)
        else:
            st.info("Visualization will appear here after first cycle")
    
    with col_right:
        # Beautiful AI Analysis Section
        if st.session_state.last_analysis:
            display_beautiful_analysis(st.session_state.last_analysis)
        else:
            # Placeholder when no analysis
            st.markdown("""
            <div class="ai-analysis-header">
                <h2 style="margin: 0;">🤖 AI Analysis</h2>
            </div>
            <div class="ai-analysis-container">
                <div style="text-align: center; padding: 2rem; color: #666;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                    <h3 style="color: #667eea;">No Analysis Available Yet</h3>
                    <p>Start monitoring to generate AI-powered insights</p>
                    <p style="font-size: 0.9rem; opacity: 0.7;">Analysis will appear here after the first cycle completes</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Auto-refresh
    if st.session_state.monitoring:
        time.sleep(2)
        st.rerun()
    
    # Footer
    st.markdown("---")
    if st.session_state.last_cycle_time:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Last Cycle:** {st.session_state.last_cycle_time.strftime('%H:%M:%S')}")
        with col2:
            st.markdown(f"**Total Cycles:** {st.session_state.cycle_count}")
        with col3:
            if st.session_state.next_cycle_time:
                st.markdown(f"**Next:** {st.session_state.next_cycle_time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()