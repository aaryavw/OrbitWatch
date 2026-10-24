import pytest
from pydantic import ValidationError
from app.schemas import TelemetryMessage

def test_valid_telemetry_payload():
    payload = {"event_id": "event-1", "satellite_id": "OW-SAT-01", "subsystem": "power",
               "metric": "battery_voltage", "value": 24.5, "unit": "V",
               "timestamp": "2026-10-24T12:00:00+00:00"}
    message = TelemetryMessage.model_validate(payload)
    assert message.metric == "battery_voltage"
    assert message.value == 24.5

def test_extra_fields_are_rejected():
    payload = {"event_id": "event-1", "satellite_id": "OW-SAT-01", "subsystem": "power",
               "metric": "battery_voltage", "value": 24.5, "unit": "V",
               "timestamp": "2026-10-24T12:00:00+00:00", "unexpected": True}
    with pytest.raises(ValidationError):
        TelemetryMessage.model_validate(payload)
