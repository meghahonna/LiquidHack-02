# 🏭 Industrial Process Monitoring - Streamlit Web UI

A clean and professional web interface for real-time industrial process monitoring with AI-powered anomaly detection.

## 🌟 Features

### 🎛️ **Real-time Monitoring Dashboard**
- **Start/Stop Controls** - Easy monitoring control with visual status indicators
- **Live Data Generation** - Synthetic data generated every 10 seconds
- **Auto-refresh Interface** - Real-time updates without manual refresh
- **Clean, Professional UI** - Modern design with intuitive layout

### 📊 **Interactive Visualizations**
- **Real-time Sensor Plots** - Interactive Plotly charts for temperature and pressure
- **Multi-panel Analysis** - Complete industrial process visualization
- **Live Data Updates** - Charts update automatically with new data

### 🤖 **AI-Powered Analysis**
- **Automatic Anomaly Detection** - AI analysis runs with each cycle
- **New Trends Alerts** - Visual notifications when new patterns are detected
- **Detailed Analysis Reports** - Full AI insights with expandable view
- **Quick Summaries** - Key findings highlighted for rapid assessment

### 📈 **System Monitoring**
- **Activity Log** - Real-time status messages and system events
- **Cycle Counter** - Track monitoring cycles and intervals
- **System Metrics** - Current data counts and update timestamps
- **Error Handling** - Graceful error reporting and recovery

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Web Interface
```bash
# Option 1: Using the launcher script
streamlit run streamlit_app.py
```

### 3. Access Dashboard
- **URL**: http://localhost:8501
- **Browser**: Opens automatically

## 🎮 How to Use

### **Starting Monitoring**
1. Click **"🚀 Start Monitoring"** button
2. System begins generating data every 10 seconds
3. Watch real-time updates in all panels
4. AI analysis runs automatically with each cycle

### **Monitoring Interface**
- **Left Panel**: System status and activity log
- **Center Panel**: Real-time data visualizations
- **Right Panel**: AI analysis results and alerts

### **Stopping Monitoring**
1. Click **"🛑 Stop Monitoring"** button
2. Current cycle completes gracefully
3. All generated data remains available
4. Can restart monitoring anytime

## 🔧 Technical Details

### **Architecture**
- **Frontend**: Streamlit web framework
- **Backend**: Python pipeline integration
- **Threading**: Background monitoring worker
- **State Management**: Streamlit session state
- **Visualization**: Plotly interactive charts

### **Data Flow**
1. **Background Thread** runs monitoring cycles
2. **Data Generation** creates synthetic industrial data
3. **Visualization** generates analysis plots
4. **AI Analysis** processes plots for anomalies using the LFM2-VL models
5. **UI Updates** refresh automatically via session state

### **Performance**
- **10-second Cycles** - Configurable monitoring interval
- **Automatic Archiving** - All data preserved with timestamps
- **Memory Efficient** - Background thread management
- **Error Recovery** - Graceful handling of failures

## 📊 Data Management

### **Real-time Generation**
- **Events Data**: Temperature, Pressure, Efficiency, Energy, CO₂
- **Sensor Data**: HeatExchanger01.S001, PumpStation01.S002
- **Time Series**: 20 data points per cycle with 5-minute intervals

### **File Structure**
```
data/
├── events.csv                    # Latest event data
├── sensors.csv                   # Latest sensor data
└── archive/                      # Timestamped archives

images/
├── culprit_signals_analysis.png  # Latest visualization
└── archive/                      # Timestamped archives

analysis/
├── analysis_report.txt           # Latest AI analysis
└── archive/                      # Timestamped archives
```

## 🛠️ Troubleshooting

### **Common Issues**

#### **Port Already in Use**
```bash
# Kill existing streamlit processes
pkill -f streamlit
# Or use different port
streamlit run streamlit_app.py --server.port 8502
```

#### **Module Import Errors**
```bash
# Install missing dependencies
pip install -r requirements.txt
```

#### **AI Analysis Fails**
- Check MLX-VLM installation
- Verify model download permissions
- Ensure sufficient system memory

### **Performance Tips**
- **Close unused browser tabs** for better performance
- **Monitor system resources** during continuous operation
- **Use Chrome/Firefox** for best compatibility
- **Enable hardware acceleration** in browser settings

## 🔗 Integration

### **Pipeline Integration**
- **Seamless**: Uses existing pipeline modules
- **Non-intrusive**: Doesn't modify core pipeline
- **Parallel**: Can run alongside command-line tools
- **Compatible**: Works with all existing features

### **API Potential**
- **REST Endpoints**: Could be extended with FastAPI
- **WebSocket**: Real-time data streaming capability
- **Mobile App**: Foundation for native mobile interface
- **Dashboard Embedding**: Can be embedded in larger systems

## 📈 Future Enhancements

### **Planned Features**
- **Historical Data Viewer** - Browse archived analyses
- **Custom Alerts** - User-defined anomaly thresholds
- **Export Functions** - Download reports and data
- **Multi-user Support** - Role-based access control
- **Advanced Filtering** - Data exploration tools

### **Technical Improvements**
- **WebSocket Integration** - True real-time updates
- **Database Backend** - Persistent data storage
- **Caching Layer** - Improved performance
- **Mobile Optimization** - Enhanced mobile experience

---

## 🎯 Perfect For

- **Industrial Engineers** - Real-time process monitoring
- **Data Scientists** - Anomaly detection research
- **System Operators** - Live system oversight
- **Managers** - High-level process insights
- **Students** - Learning industrial monitoring concepts
