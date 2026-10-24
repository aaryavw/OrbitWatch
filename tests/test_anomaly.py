from datetime import datetime, timezone
from app.anomaly import detect_anomaly
from app.schemas import TelemetryMessage

def message(metric="battery_voltage", value=25.0, unit="V"):
    return TelemetryMessage(event_id="test-event", satellite_id="OW-SAT-TEST", subsystem="power",
                            metric=metric, value=value, unit=unit, timestamp=datetime.now(timezone.utc))

def test_normal_value_is_not_anomaly():
    assert detect_anomaly(message()) is None

def test_out_of_range_voltage_is_anomaly():
    result = detect_anomaly(message(value=18.0))
    assert result is not None
    assert result.severity in {"warning", "critical"}
    assert "outside illustrative range" in result.message

def test_unknown_metric_is_ignored():
    assert detect_anomaly(message(metric="unknown_metric", value=999, unit="units")) is None

def test_unexpected_unit_is_warning():
    result = detect_anomaly(message(value=25.0, unit="mV"))
    assert result is not None
    assert result.severity == "warning"
