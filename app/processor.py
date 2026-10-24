import logging
import time
from datetime import timezone
import paho.mqtt.client as mqtt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.config import MQTT_HOST, MQTT_PORT, MQTT_TOPIC
from app.database import SessionLocal, init_db
from app.models import AnomalyAlert, TelemetryRecord
from app.schemas import TelemetryMessage
from app.anomaly import detect_anomaly

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("orbitwatch.processor")

def process_payload(payload: bytes) -> str:
    try:
        message = TelemetryMessage.model_validate_json(payload)
    except Exception as exc:
        logger.warning("Rejected invalid telemetry payload: %s", exc)
        return "invalid"

    timestamp = message.timestamp
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    db = SessionLocal()
    try:
        db.add(TelemetryRecord(
            event_id=message.event_id, satellite_id=message.satellite_id,
            subsystem=message.subsystem, metric=message.metric, value=message.value,
            unit=message.unit, timestamp=timestamp,
        ))
        db.flush()
        anomaly = detect_anomaly(message)
        if anomaly:
            db.add(AnomalyAlert(
                event_id=message.event_id, satellite_id=message.satellite_id,
                subsystem=message.subsystem, metric=message.metric,
                observed_value=message.value, unit=message.unit,
                severity=anomaly.severity, message=anomaly.message, timestamp=timestamp,
            ))
        db.commit()
        return "stored"
    except IntegrityError:
        db.rollback()
        logger.info("Ignoring duplicate event_id=%s", message.event_id)
        return "duplicate"
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database failure while processing event_id=%s", message.event_id)
        return "database_error"
    finally:
        db.close()

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logger.info("Connected to MQTT broker at %s:%s", MQTT_HOST, MQTT_PORT)
        client.subscribe(MQTT_TOPIC, qos=1)
    else:
        logger.error("MQTT connection failed: %s", reason_code)

def on_message(client, userdata, msg):
    process_payload(msg.payload)

def main():
    while True:
        try:
            init_db()
            break
        except Exception:
            logger.exception("Database not ready; retrying in 3 seconds")
            time.sleep(3)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="orbitwatch-processor")
    client.on_connect = on_connect
    client.on_message = on_message
    while True:
        try:
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            client.loop_forever()
        except Exception:
            logger.exception("MQTT processor connection failed; retrying in 3 seconds")
            time.sleep(3)

if __name__ == "__main__":
    main()
