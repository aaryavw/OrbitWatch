import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="OrbitWatch | Satellite Telemetry & Command",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Endpoint Configuration
API_BASE_URL = "http://localhost:8000"  # Adjust if running inside Docker network differently

# Custom Dark Cyberpunk / Command Center Theme Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #070b12;
            color: #e2e8f0;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        .main-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border: 1px solid #1e3a8a;
            border-radius: 12px;
            padding: 20px 25px;
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        .metric-card {
            background: #0b1329;
            border: 1px solid #1e3a8a;
            border-radius: 10px;
            padding: 15px 20px;
            text-align: center;
            box-shadow: inset 0 2px 4px rgba(59, 130, 246, 0.1);
        }
        .metric-title {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #93c5fd;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #f8fafc;
        }
        .section-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #60a5fa;
            border-bottom: 1px solid #1e3a8a;
            padding-bottom: 8px;
            margin-top: 15px;
            margin-bottom: 15px;
        }
        /* Style Streamlit expanders & sidebars */
        .sidebar .stSidebar {
            background-color: #05080f;
        }
    </style>
""", unsafe_allow_html=True)

# Top Command Header
st.markdown("""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin: 0; font-size: 1.8rem; color: #f8fafc; display: flex; align-items: center; gap: 10px;">
                    <span>🛰️</span> ORBITWATCH COMMAND CENTER
                </h1>
                <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 0.95rem;">
                    Real-time Satellite Telemetry, Orbit Tracking & Telemetry Analytics
                </p>
            </div>
            <div style="text-align: right;">
                <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                    ● LIVE FEED ACTIVE
                </span>
                <p style="margin: 8px 0 0 0; color: #64748b; font-size: 0.8rem;">
                    UTC: {}
                </p>
            </div>
        </div>
    </div>
""".format(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

# Sidebar Fleet & Filters
with st.sidebar:
    st.markdown("### 📡 Fleet Control")
    search_query = st.text_input("Search Satellite / ID", placeholder="e.g. SAT-01")
    
    st.markdown("---")
    st.markdown("### 🎛️ Display Layers")
    show_orbit_paths = st.checkbox("Show Orbital Vectors", value=True)
    show_footprints = st.checkbox("Ground Station Coverage", value=True)
    anomaly_filter = st.selectbox("Filter Status", ["All Fleets", "Nominal Only", "Advisory / Anomalies"])
    
    st.markdown("---")
    st.markdown("### ⚙️ Telemetry Settings")
    refresh_rate = st.slider("Refresh Interval (s)", 1, 10, 3)
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #475569; font-size: 0.75rem;'>OrbitWatch Engine v2.4<br/>Secure Telemetry Link</p>", unsafe_allow_html=True)

# Main Dashboard Layout - Top Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Active Satellites</div>
            <div class="metric-value" style="color: #38bdf8;">12 / 12</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Nominal Systems</div>
            <div class="metric-value" style="color: #34d399;">145</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Advisories / Flags</div>
            <div class="metric-value" style="color: #fbbf24;">3</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Downlink Bitrate</div>
            <div class="metric-value" style="color: #a855f7;">48.2 Mbps</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Middle Section: Map Visualizer & Live Gauges
map_col, gauges_col = st.columns([2, 1])

with map_col:
    st.markdown('<div class="section-title">🌍 Global Orbital Tracking & Ground Stations</div>', unsafe_allow_html=True)
    
    # Generate mock satellite coordinates for map display
    map_data = pd.DataFrame({
        'lat': [38.8951, 51.5074, 35.6762, -33.8688, 1.3521, 45.5017, -22.9068],
        'lon': [-77.0364, -0.1278, 139.6503, 151.2093, 103.8198, -73.5673, -43.1729],
        'satellite': ['SAT-Alpha', 'SAT-Beta', 'SAT-Gamma', 'SAT-Delta', 'SAT-Epsilon', 'SAT-Zeta', 'SAT-Theta'],
        'status': ['Nominal', 'Nominal', 'Advisory', 'Nominal', 'Nominal', 'Nominal', 'Nominal']
    })
    
    st.map(map_data, latitude='lat', longitude='lon', size=30, color='#38bdf8')

with gauges_col:
    st.markdown('<div class="section-title">📊 Subsystem Telemetry Gauges</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: #0b1329; border: 1px solid #1e3a8a; border-radius: 10px; padding: 15px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.9rem;">
                <span style="color: #93c5fd;">Solar Array Power Output</span>
                <span style="color: #38bdf8; font-weight: bold;">4.2 kW</span>
            </div>
            <div style="background: #1e293b; border-radius: 4px; height: 10px; width: 100%;">
                <div style="background: linear-gradient(90deg, #3b82f6, #06b6d4); width: 84%; height: 100%; border-radius: 4px;"></div>
            </div>
        </div>
        
        <div style="background: #0b1329; border: 1px solid #1e3a8a; border-radius: 10px; padding: 15px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.9rem;">
                <span style="color: #93c5fd;">Core Thermal Regulation</span>
                <span style="color: #34d399; font-weight: bold;">24.5 °C</span>
            </div>
            <div style="background: #1e293b; border-radius: 4px; height: 10px; width: 100%;">
                <div style="background: linear-gradient(90deg, #10b981, #34d399); width: 49%; height: 100%; border-radius: 4px;"></div>
            </div>
        </div>

        <div style="background: #0b1329; border: 1px solid #1e3a8a; border-radius: 10px; padding: 15px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.9rem;">
                <span style="color: #93c5fd;">Battery State of Charge</span>
                <span style="color: #38bdf8; font-weight: bold;">92.1%</span>
            </div>
            <div style="background: #1e293b; border-radius: 4px; height: 10px; width: 100%;">
                <div style="background: linear-gradient(90deg, #3b82f6, #6366f1); width: 92%; height: 100%; border-radius: 4px;"></div>
            </div>
        </div>

        <div style="background: #0b1329; border: 1px solid #1e3a8a; border-radius: 10px; padding: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.9rem;">
                <span style="color: #93c5fd;">Gyro Drift Compensation</span>
                <span style="color: #fbbf24; font-weight: bold;">0.02 deg/s</span>
            </div>
            <div style="background: #1e293b; border-radius: 4px; height: 10px; width: 100%;">
                <div style="background: linear-gradient(90deg, #f59e0b, #fbbf24); width: 25%; height: 100%; border-radius: 4px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Bottom Section: Live Telemetry Streams & Charts
st.markdown('<div class="section-title">📈 Real-Time Downlink Telemetry Streams</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

# Generate sample streaming time-series data
chart_data = pd.DataFrame({
    'Time': pd.date_range(start='2026-10-24 17:00:00', periods=20, freq='s'),
    'Altitude (km)': [550 + (i % 3) * 0.2 for i in range(20)],
    'Signal SNR (dB)': [15.2 + (i % 5) * 0.4 for i in range(20)]
})

with chart_col1:
    st.markdown_text = "**Orbital Altitude Variation (km)**"
    st.line_chart(chart_data.set_index('Time')['Altitude (km)'], color='#38bdf8')

with chart_col2:
    st.markdown_text = "**Downlink Signal-to-Noise Ratio (SNR dB)**"
    st.line_chart(chart_data.set_index('Time')['Signal SNR (dB)'], color='#a855f7')
