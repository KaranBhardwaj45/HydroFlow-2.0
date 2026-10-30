# HYDROFLOW

> **Smart IoT-Based Hydroponic Farming System with Automated Nutrient Control and Plant Health Monitoring**

HYDROFLOW is a real-time, real-data-driven IoT hydroponic monitoring and automated dosing control platform designed for precision agriculture. It integrates ESP32 microcontrollers, EMQX MQTT broker telemetry, ThingSpeak cloud synchronization, local SQLite time-series persistence, and an algorithmic plant health computer-vision engine.

---

## System Architecture

```
ESP32 Sensors & Actuators
        │  (QoS 1 Telemetry & Heartbeat)
        ▼
EMQX MQTT Broker (TLS / Port 8883)
        │
        ▼
Python Flask MQTT Subscriber (paho-mqtt)
        │
        ├─► Input Validation & Normalization
        │
        ├─► Local SQLite Database (hydroflow.db)
        │       │
        │       ├─► REST APIs (Blueprints)
        │       │       │
        │       │       ▼
        │       │   HTML5 / CSS3 / Vanilla JS Dashboard
        │       │
        │       └─► Offline Buffering & State Machine
        │
        └─► ThingSpeak Cloud Integration (Field 1-8 telemetry sync)
```

---

## Key Features

1. **Page 1: Login**
   - Session-based authentication with bcrypt/pbkdf2 password hashing.
   - Demo credentials: `demo@hydroflow.io` / `hydroflow123`.

2. **Page 2: Main Dashboard**
   - Real-time metric cards: pH, EC/TDS, Water Temp, Humidity, Water Level, Air Quality.
   - 24-hour dual-axis trend chart with target range bands.
   - System Health diagnostics (ESP32, Sensors, Pumps, Light, Camera, SD Card, Cloud).
   - Recent system events and active alert badges.

3. **Page 3: Live Monitoring**
   - Dynamic reservoir gauge showing volume percentage with safe/critical marks.
   - Actuator status indicators (Nutrient Pump, pH-UP/DOWN, Circulation, Light, Camera).
   - Live system clock and heartbeat freshness indicator.

4. **Page 4: Historical Analytics**
   - Filterable date ranges: 24 Hours, 7 Days, 30 Days.
   - 4-panel historical charts: pH, EC/TDS, Temperature & Humidity, Water Level.
   - Key statistics: Average pH, Time in target %, Dosing events, Average dose duration, Warnings, Offline duration.
   - One-click CSV export.

5. **Page 5: Plant Health Monitoring**
   - Algorithmic computer vision analysis using Excess Green Index (ExG) and color space segmentation.
   - Genuine foliage calculations: Green Area %, Yellowing level (chlorosis), Dark spots (necrosis).
   - Real photo upload with instant server-side CV processing.
   - Historical observation timeline.

6. **Page 6: Alerts & Events**
   - Real-time alert feed with severity filtering (Info, Warning, Critical) and text search.
   - In-app alert acknowledgement and deduplication engine.

7. **Page 7: Automation & Configuration**
   - Configurable pH and EC upper/lower limits, pulse durations, mixing delays, and maximum pulse guards.
   - Grow-light photoperiod schedule with automatic duration calculation.
   - Water level safe (30%) and critical (20%) thresholds with local hardware interlocks.

8. **Page 8: Device & Connectivity**
   - Diagnostic hardware metrics: ESP32 status, firmware version, Wi-Fi RSSI, ThingSpeak cloud status.
   - Cloud synchronization counters (Cloud Records vs Local Pending Records).
   - Manual "Sync Now" trigger.
   - Explicit offline mode architecture with local ESP32 safety autonomy.

9. **Page 9: System Logs**
   - Filterable activity table (Module, Severity, Status, Source).
   - Server-side pagination and CSV export.

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- SQLite3 (included with Python)

### Setup & Run on Windows

```cmd
:: 1. Clone or extract the project repository
cd hydroflow

:: 2. Create and activate a Python virtual environment
python -m venv venv
venv\Scripts\activate

:: 3. Install required Python packages
pip install -r requirements.txt

:: 4. Copy the environment configuration
copy .env.example .env

:: 5. Initialize and seed the SQLite database
python database/seed.py

:: 6. Start the HYDROFLOW application
python app.py --port 5000
```

Open your browser and navigate to:
**http://127.0.0.1:5000**

Default Login Credentials:
- **Email:** `demo@hydroflow.io`
- **Password:** `hydroflow123`

---

## Environment Variables (`.env`)

| Variable | Default | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | `hydroflow-secure-dev-session-key-2026` | Flask session cryptographic secret |
| `DATABASE_PATH` | `instance/hydroflow.db` | Local SQLite database file location |
| `PORT` | `3000` | Port for the web server |
| `DEVICE_ID` | `ESP32-001` | Active hydroponic controller device ID |
| `DEMO_MODE` | `true` | Enable realistic demo data simulation when no hardware is attached |
| `SENSOR_STALE_SECONDS`| `30` | Timeout in seconds before sensor telemetry is marked stale |
| `EMQX_HOST` | *(empty)* | EMQX Broker hostname (e.g. `broker.emqx.io` or cluster URI) |
| `EMQX_PORT` | `8883` | EMQX Broker port (8883 for TLS, 1883 for TCP) |
| `EMQX_USERNAME` | *(empty)* | EMQX client username |
| `EMQX_PASSWORD` | *(empty)* | EMQX client password |
| `EMQX_USE_TLS` | `true` | Enable TLS encryption |
| `THINGSPEAK_API_KEY` | *(empty)* | ThingSpeak Channel Write API Key |
| `THINGSPEAK_CHANNEL_ID`| *(empty)* | ThingSpeak Channel ID |
| `THINGSPEAK_READ_API_KEY`| *(empty)* | ThingSpeak Channel Read API Key |

---

## EMQX MQTT Broker Integration

### Topic Structure

- **Telemetry:** `hydroflow/devices/<DEVICE_ID>/telemetry`
- **Device Status:** `hydroflow/devices/<DEVICE_ID>/status`
- **Events / Alerts:** `hydroflow/devices/<DEVICE_ID>/events`
- **Commands:** `hydroflow/devices/<DEVICE_ID>/commands`
- **Command Acknowledgement:** `hydroflow/devices/<DEVICE_ID>/command-ack`

### Sample MQTT Telemetry Payload

```json
{
  "device_id": "ESP32-001",
  "message_id": "msg-1042-uuid",
  "timestamp": "2026-10-19T10:10:00Z",
  "sequence": 1042,
  "sensors": {
    "ph": 6.22,
    "ec_ms_cm": 1.44,
    "water_temperature_c": 24.5,
    "humidity_pct": 68.0,
    "water_level_pct": 74.0,
    "air_quality": "Good"
  },
  "actuators": {
    "nutrient_pump": false,
    "ph_up_pump": false,
    "ph_down_pump": false,
    "water_pump": true,
    "grow_light": true,
    "camera_ready": true,
    "sd_card_ready": true
  }
}
```

### Manual MQTT Publishing Test Tool

Run the diagnostic publisher script:
```bash
python scripts/test_mqtt_publish.py
```

---

## ThingSpeak Channel Configuration

To sync telemetry to ThingSpeak, create a channel with the following 8 fields:

- **Field 1:** pH
- **Field 2:** EC/TDS (mS/cm)
- **Field 3:** Water Temperature (°C)
- **Field 4:** Humidity (%)
- **Field 5:** Water Level (%)
- **Field 6:** Air Quality
- **Field 7:** Nutrient Pump Status (0/1)
- **Field 8:** Grow Light Status (0/1)

Populate `THINGSPEAK_API_KEY` and `THINGSPEAK_CHANNEL_ID` in `.env`.

---

## Automated Test Suite

Run the full automated test suite:
```bash
python -m unittest tests/test_hydroflow.py
```

Test coverage includes:
- Database initialization and schema creation
- Login, session cookie auth, and logout
- Sensor boundary and physical unit validation
- ESP32 telemetry ingestion
- Alert generation, deduplication, and acknowledgement
- Automation configuration validation
- Device heartbeat staleness detection
- Hardware actuator safety bounding
