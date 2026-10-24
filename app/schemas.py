from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TelemetryMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: str = Field(min_length=1, max_length=64)
    satellite_id: str = Field(min_length=1, max_length=64)
    subsystem: str = Field(min_length=1, max_length=64)
    metric: str = Field(min_length=1, max_length=64)
    value: float
    unit: str = Field(min_length=1, max_length=24)
    timestamp: datetime

class TelemetryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_id: str
    satellite_id: str
    subsystem: str
    metric: str
    value: float
    unit: str
    timestamp: datetime
    received_at: datetime

class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_id: str
    satellite_id: str
    subsystem: str
    metric: str
    observed_value: float
    unit: str
    severity: str
    message: str
    timestamp: datetime
    created_at: datetime
