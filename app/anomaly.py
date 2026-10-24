from dataclasses import dataclass
from app.schemas import TelemetryMessage

@dataclass(frozen=True)
class Anomaly:
    severity: str
    message: str

# Illustrative thresholds for simulated data only, not real spacecraft limits.
RANGES = {
    "battery_voltage": (22.0, 29.0, "V"),
    "cpu_temperature": (-10.0, 85.0, "C"),
    "cpu_utilization": (0.0, 100.0, "%"),
    "signal_strength": (-120.0, 0.0, "dBm"),
    "memory_utilization": (0.0, 100.0, "%"),
}

def detect_anomaly(message: TelemetryMessage) -> Anomaly | None:
    bounds = RANGES.get(message.metric)
    if bounds is None:
        return None
    low, high, expected_unit = bounds
    if message.unit != expected_unit:
        return Anomaly("warning", f"Unexpected unit {message.unit!r}; expected {expected_unit!r}.")
    if message.value < low or message.value > high:
        span = high - low
        severity = "critical" if message.value < low - 0.1 * span or message.value > high + 0.1 * span else "warning"
        return Anomaly(severity, f"{message.metric}={message.value:g}{message.unit} is outside illustrative range [{low:g}, {high:g}].")
    return None
