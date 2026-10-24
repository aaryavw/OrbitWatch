# OrbitWatch: Satellite Telemetry Monitoring Dashboard

OrbitWatch is an educational software-engineering project that monitors **simulated satellite telemetry**. A Python simulator publishes measurements over MQTT; a Python processor validates readings, detects anomalies, and stores telemetry and alerts in PostgreSQL. FastAPI exposes the data, and Streamlit presents a dashboard.

> This project does not connect to real spacecraft or operational NRO systems. Its live feed is simulated. Public datasets can be added later for historical replay and evaluation.

## Features
- Simulated telemetry stream over MQTT using Eclipse Mosquitto
- Pydantic message validation and transparent rule-based anomaly detection
- PostgreSQL storage for telemetry and anomaly alerts
- FastAPI REST API and interactive Streamlit/Plotly dashboard
- Docker Compose deployment, pytest tests, and GitHub Actions CI

## Architecture

```text
Python simulator -> MQTT/Mosquitto -> Python processor -> PostgreSQL
                                          |                  |
                                          v                  v
                                     validation          FastAPI API
                                     anomaly rules           |
                                                            v
                                                     Streamlit dashboard
```

## Technology stack
Python, FastAPI, PostgreSQL, MQTT, Eclipse Mosquitto, Docker, Docker Compose, Streamlit, Plotly, Pydantic, SQLAlchemy, pytest, GitHub Actions.

## Quick start

Prerequisites: Docker Desktop or Docker Engine with Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

Open:
- Dashboard: http://localhost:8501
- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

The simulator publishes a measurement about every two seconds. Occasional injected anomalies are intentional so you can test the alert pipeline.

Stop with `Ctrl+C`, then:

```bash
docker compose down
```

To also delete stored database records and the local database volume:

```bash
docker compose down -v
```

**Warning:** `docker compose down -v` permanently deletes the local PostgreSQL volume.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API/database health |
| GET | `/telemetry?limit=100` | Recent telemetry records |
| GET | `/telemetry/latest` | Latest record per satellite/metric |
| GET | `/alerts?limit=100` | Recent anomaly alerts |
| GET | `/metrics/summary` | Telemetry and alert counts |

Examples:

```bash
curl http://localhost:8000/health
curl 'http://localhost:8000/telemetry?limit=20'
curl 'http://localhost:8000/alerts?limit=20'
curl http://localhost:8000/metrics/summary
```

## MQTT message format

Topic: `orbitwatch/telemetry`

```json
{
  "event_id": "c20a4a70-8e72-43df-94c6-7a6ad1c6f8a1",
  "satellite_id": "OW-SAT-01",
  "subsystem": "power",
  "metric": "battery_voltage",
  "value": 24.8,
  "unit": "V",
  "timestamp": "2026-10-24T14:00:00+00:00"
}
```

Each message has a unique `event_id`. PostgreSQL enforces uniqueness so duplicate events are ignored.

## Anomaly detection

The starter implementation uses explainable threshold rules for battery voltage, CPU temperature, CPU utilization, memory utilization, and signal strength. These are **illustrative values for simulated data, not real spacecraft operating limits**. The rules live in `app/anomaly.py`.

For a stronger evaluation, add a public telemetry dataset, document its license and source, and compare detections with its labels where available. Candidate sources include the [ESA anomaly dataset](https://github.com/esa/anomaly-dataset) and [Telemanom NASA SMAP/MSL benchmark](https://github.com/khundman/telemanom). Check dataset-specific licenses and conditions before redistribution.

## Tests

Create a local environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

The unit tests do not require a running database or MQTT broker.

## Local run without Docker

A PostgreSQL instance and MQTT broker must already be running. Copy `.env.example` to `.env` and adjust hostnames: outside Compose, use `localhost` rather than `db` or `mqtt`.

Then run each process in a separate terminal:

```bash
python -m app.processor
uvicorn app.api:app --host 0.0.0.0 --port 8000
streamlit run dashboard.py --server.port 8501
python -m app.simulator
```

## Troubleshooting

- **No data:** wait a few seconds and refresh the dashboard. Check `docker compose ps`.
- **Database errors:** `docker compose logs db api processor`.
- **MQTT errors:** `docker compose logs mqtt simulator processor`.
- **Port conflicts:** edit host-side port mappings in `docker-compose.yml`.
- **Inspect live logs:** `docker compose logs -f processor`.

## Security and limitations

- `.env` is ignored by Git. Never commit credentials or sensitive operational data.
- The Mosquitto configuration allows anonymous access for local development only. Do not expose this broker to an untrusted network; add authentication, authorization, and TLS before any shared deployment.
- The API has no authentication in this starter project. Keep it local unless you add access controls.
- `Base.metadata.create_all()` is suitable for this small starter. Use Alembic migrations as the schema evolves.
- The dashboard currently refreshes on manual page reload; the refresh interval control is informational only in this version.

## Suggested extensions
1. Add a replay adapter for public telemetry data.
2. Add filters for satellite, subsystem, time range, and alert severity.
3. Evaluate anomaly detection with precision, recall, and false-positive rate.
4. Add structured logging, Prometheus metrics, and Grafana.
5. Add API authentication and MQTT TLS/authentication before deployment beyond localhost.

## Data attribution
The default project contains generated simulated telemetry only. If you integrate external data, document the exact source, citation, license, and required attribution. Do not assume all agency-published datasets share the same reuse terms.

## License
Educational starter project. Add a license file before publishing if you want to grant explicit reuse rights.
