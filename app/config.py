import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://orbitwatch:local_dev_password_change_me@localhost:5432/orbitwatch")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "orbitwatch/telemetry")
SIMULATOR_INTERVAL_SECONDS = float(os.getenv("SIMULATOR_INTERVAL_SECONDS", "2"))
ANOMALY_INJECTION_RATE = float(os.getenv("ANOMALY_INJECTION_RATE", "0.08"))
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
