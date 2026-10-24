import json
import logging
import random
import time
import uuid
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from app.config import MQTT_HOST, MQTT_PORT, MQTT_TOPIC, SIMULATOR_INTERVAL_SECONDS, ANOMALY_INJECTION_RATE

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("orbitwatch.simulator")
SATELLITE_ID = "OW-SAT-01"
METRICS = [
    ("power", "battery_voltage", 25.0, 0.7, "V"),
    ("thermal", "cpu_temperature", 38.0, 7.0, "C"),
    ("compute", "cpu_utilization", 42.0, 12.0, "%"),
    ("communications", "signal_strength", -75.0, 8.0, "dBm"),
    ("compute", "memory_utilization", 55.0, 10.0, "%"),
]

def create_reading():
    subsystem, metric, mean, spread, unit = random.choice(METRICS)
    value = random.gauss(mean, spread)
    if random.random() < ANOMALY_INJECTION_RATE:
        if metric == "battery_voltage":
            value = random.choice([random.uniform(17, 21), random.uniform(30, 34)])
        elif metric == "cpu_temperature":
            value = random.choice([random.uniform(-25, -12), random.uniform(90, 115)])
        elif metric in ("cpu_utilization", "memory_utilization"):
            value = random.choice([random.uniform(-15, -2), random.uniform(105, 125)])
        elif metric == "signal_strength":
            value = random.choice([random.uniform(-145, -125), random.uniform(5, 15)])
    return {
        "event_id": str(uuid.uuid4()), "satellite_id": SATELLITE_ID,
        "subsystem": subsystem, "metric": metric, "value": round(value, 3),
        "unit": unit, "timestamp": datetime.now(timezone.utc).isoformat(),
    }

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="orbitwatch-simulator")
    while True:
        try:
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            client.loop_start()
            break
        except Exception:
            logger.exception("MQTT broker not ready; retrying in 3 seconds")
            time.sleep(3)
    try:
        while True:
            payload = json.dumps(create_reading())
            info = client.publish(MQTT_TOPIC, payload=payload, qos=1)
            info.wait_for_publish(timeout=5)
            logger.info("Published %s", payload)
            time.sleep(SIMULATOR_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logger.info("Simulator stopping")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
