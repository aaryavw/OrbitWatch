import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
st.set_page_config(page_title="OrbitWatch", page_icon="🛰️", layout="wide")
st.title("OrbitWatch")
st.caption("Satellite telemetry monitoring · simulated data")

with st.sidebar:
    st.header("Controls")
    record_limit = st.slider("Records to display", min_value=25, max_value=500, value=100, step=25)
    subsystem_filter = st.selectbox("Subsystem", ["All", "power", "thermal", "compute", "communications"])
    st.markdown(f"[API documentation]({API_BASE_URL}/docs)")

try:
    health = requests.get(f"{API_BASE_URL}/health", timeout=3)
    health.raise_for_status()
    telemetry_response = requests.get(f"{API_BASE_URL}/telemetry", params={"limit": record_limit}, timeout=5)
    telemetry_response.raise_for_status()
    alert_response = requests.get(f"{API_BASE_URL}/alerts", params={"limit": 100}, timeout=5)
    alert_response.raise_for_status()
    summary_response = requests.get(f"{API_BASE_URL}/metrics/summary", timeout=5)
    summary_response.raise_for_status()
    telemetry, alerts, summary = telemetry_response.json(), alert_response.json(), summary_response.json()
except requests.RequestException as exc:
    st.error(f"Could not reach OrbitWatch API at {API_BASE_URL}: {exc}")
    st.info("Start the services with `docker compose up --build`, then refresh this page.")
    st.stop()

telemetry_df, alerts_df = pd.DataFrame(telemetry), pd.DataFrame(alerts)
if not telemetry_df.empty:
    telemetry_df["timestamp"] = pd.to_datetime(telemetry_df["timestamp"], utc=True)
if not alerts_df.empty:
    alerts_df["timestamp"] = pd.to_datetime(alerts_df["timestamp"], utc=True)

m1, m2, m3 = st.columns(3)
m1.metric("Telemetry records", f"{summary['telemetry_records']:,}")
m2.metric("Anomaly alerts", f"{summary['anomaly_alerts']:,}")
m3.metric("API status", "Connected" if health.ok else "Unavailable")

st.subheader("Telemetry measurements")
if telemetry_df.empty:
    st.warning("No telemetry has arrived yet. Wait a few seconds and refresh.")
else:
    if subsystem_filter != "All":
        telemetry_df = telemetry_df[telemetry_df["subsystem"] == subsystem_filter]
    metric_options = sorted(telemetry_df["metric"].dropna().unique().tolist())
    if metric_options:
        selected_metric = st.selectbox("Metric", metric_options)
        metric_df = telemetry_df[telemetry_df["metric"] == selected_metric].sort_values("timestamp")
        if not metric_df.empty:
            fig = px.line(metric_df, x="timestamp", y="value", color="subsystem", markers=True,
                          hover_data=["satellite_id", "unit", "event_id"], title=f"{selected_metric} over time")
            fig.update_layout(xaxis_title="Timestamp (UTC)", yaxis_title="Value")
            st.plotly_chart(fig, use_container_width=True)
    st.dataframe(telemetry_df.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)

st.subheader("Anomaly alerts")
if alerts_df.empty:
    st.success("No anomaly alerts recorded yet.")
else:
    severity_order = {"critical": 0, "warning": 1}
    alerts_df["severity_rank"] = alerts_df["severity"].map(severity_order).fillna(2)
    st.dataframe(alerts_df.sort_values(["severity_rank", "timestamp"], ascending=[True, False]).drop(columns=["severity_rank"]),
                 use_container_width=True, hide_index=True)
st.caption("Refresh the browser page to load new data. The dashboard queries the API when the page runs.")
