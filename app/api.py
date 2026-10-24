from fastapi import Depends, FastAPI, Query
from sqlalchemy import desc, func, text
from sqlalchemy.orm import Session
from app.database import get_db, init_db
from app.models import AnomalyAlert, TelemetryRecord
from app.schemas import AlertOut, TelemetryOut

app = FastAPI(title="OrbitWatch API", description="API for simulated satellite telemetry and anomaly alerts.", version="1.0.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected", "data_scope": "simulated telemetry"}

@app.get("/telemetry", response_model=list[TelemetryOut])
def get_telemetry(limit: int = Query(default=100, ge=1, le=1000), satellite_id: str | None = None, subsystem: str | None = None, db: Session = Depends(get_db)):
    query = db.query(TelemetryRecord)
    if satellite_id:
        query = query.filter(TelemetryRecord.satellite_id == satellite_id)
    if subsystem:
        query = query.filter(TelemetryRecord.subsystem == subsystem)
    return query.order_by(desc(TelemetryRecord.timestamp)).limit(limit).all()

@app.get("/telemetry/latest", response_model=list[TelemetryOut])
def latest_by_metric(db: Session = Depends(get_db)):
    records = db.query(TelemetryRecord).order_by(desc(TelemetryRecord.timestamp)).limit(1000).all()
    latest = {}
    for record in records:
        latest.setdefault((record.satellite_id, record.metric), record)
    return list(latest.values())

@app.get("/alerts", response_model=list[AlertOut])
def get_alerts(limit: int = Query(default=100, ge=1, le=1000), severity: str | None = None, db: Session = Depends(get_db)):
    query = db.query(AnomalyAlert)
    if severity:
        query = query.filter(AnomalyAlert.severity == severity.lower())
    return query.order_by(desc(AnomalyAlert.timestamp)).limit(limit).all()

@app.get("/metrics/summary")
def summary(db: Session = Depends(get_db)):
    telemetry_count = db.query(func.count(TelemetryRecord.id)).scalar() or 0
    alert_count = db.query(func.count(AnomalyAlert.id)).scalar() or 0
    return {"telemetry_records": telemetry_count, "anomaly_alerts": alert_count, "data_scope": "simulated telemetry"}
