# Underground Mines Safety System — Sensor Bridge

> A real-time bridge connecting Arduino-based mining safety sensors to a cloud-hosted FastAPI backend via WebSocket.

---

## Architecture

```
Arduino UNO
    │
    │ USB Serial
    ▼
  Laptop
    │
    │ Python Sensor Bridge
    ▼
Render FastAPI
    │
    │ WebSocket
    ▼
Web Dashboard
```
```
https://drive.google.com/drive/folders/1Thhx-196MS_y5KyWBvx8XwMBEpddcZnx
```
---
## server
```
https://engineer-day-2026-backend.onrender.com/
```

## Responsibilities

The Sensor Bridge is responsible for:

- 📥 Reading real-time sensor data from the Arduino Serial/COM port
- 🧩 Parsing the incoming JSON payload
- ☁️ Transmitting processed data to the Render FastAPI WebSocket endpoint
- 🔁 Maintaining a continuous, robust loop between hardware and the cloud backend

---

## Expected Arduino Data Format

The Arduino must transmit **one valid JSON object per line**:

```json
{
  "temp": 28.0,
  "gas": 125,
  "fire": 0,
  "sos": 0,
  "warning": 0,
  "danger": 0,
  "fan": 0
}
```

| Field | Type | Description |
|---|---|---|
| `temp` | float | Ambient temperature (°C) |
| `gas` | int | Gas concentration level |
| `fire` | 0/1 | Fire detection flag |
| `sos` | 0/1 | Manual SOS trigger |
| `warning` | 0/1 | Warning threshold flag |
| `danger` | 0/1 | Danger threshold flag |
| `fan` | 0/1 | Ventilation fan status |

---

## Installation & Setup

**1. Clone the repository and navigate to the project folder**

```bash
git clone https://github.com/kvinitkarmkar/sensor-bridge
cd sensor-bridge
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
```

- **Windows**
  ```bash
  venv\Scripts\activate
  ```
- **macOS / Linux**
  ```bash
  source venv/bin/activate
  ```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the root directory:

```env
ARDUINO_PORT=COM6
BAUD_RATE=9600
BACKEND_WS_URL=wss://engineer-day-2026-backend.onrender.com/ws
SERIAL_TIMEOUT=1
```

> **Note:** Replace `COM6` with the port assigned to your Arduino UNO.
> On Linux/macOS, use something like `/dev/ttyUSB0` or `/dev/ACM0`.

---

##  Running the Application

```bash
python main.py
```

### Expected Output

```
============================================================
 Underground Mines Safety System - Sensor Bridge
============================================================

[SERIAL] Connected to Arduino on COM6 @ 9600 baud
[WS] Connected to backend: wss://engineer-day-2026-backend.onrender.com/ws
[SYSTEM] Sensor bridge started.
[SYSTEM] Waiting for Arduino data...

[ARDUINO] Received: {'temp': 28.0, 'gas': 125, 'fire': 0, ...}
[WS] Sent: {"temp": 28.0, "gas": 125, "fire": 0, ...}
```

---

## Data Flow Pipeline

```
Sensor
  ↓
Arduino UNO
  ↓
USB Serial
  ↓
serial_reader.py
  ↓
main.py
  ↓
websocket_client.py
  ↓
Render FastAPI WebSocket
```

---

## Important Guidelines

- **Port Conflict:** Do not run the Arduino IDE Serial Monitor while the Sensor Bridge is running — most operating systems allow only one application to access a COM port at a time.
- **Security:** Never commit your `.env` file to GitHub. Make sure it's listed in `.gitignore`.

---

## Tech Stack

- **Hardware:** Arduino UNO
- **Bridge:** Python (`pyserial`, `websockets` / `websocket-client`)
- **Backend:** FastAPI (deployed on Render)
- **Transport:** USB Serial → WebSocket
