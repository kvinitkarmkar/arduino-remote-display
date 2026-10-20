# ⛏️ Underground Mines Safety System — Backend

> Real-time backend for the Underground Mines Safety System — built with **FastAPI** and **WebSockets** to receive live sensor data from the laptop-side Sensor Bridge and broadcast it to connected web dashboards.

---

## 📡 Architecture

```
Arduino UNO
     │
     │ USB Serial
     ▼
Laptop — Sensor Bridge
     │
     │ WebSocket
     ▼
FastAPI Backend — Render
     │
     │ WebSocket Broadcast
     ▼
HTML Dashboard
```

---

## 🎯 Backend Responsibilities

The backend is responsible for:

- 📥 Receiving live sensor data from the laptop
- 🔌 Managing WebSocket connections
- 📢 Broadcasting sensor data to connected dashboards
- ❤️ Providing health/status endpoints
- 👥 Supporting multiple dashboard clients
- ☁️ Running as a cloud service on Render

> ⚠️ The backend does **not** communicate directly with the Arduino.
> Flow: `Arduino → Laptop → Backend → Dashboard`

---

## 📁 Project Structure

```
backend/
│
├── main.py                 # FastAPI application and WebSocket endpoint
├── websocket_manager.py     # WebSocket connection and broadcast management
├── config.py                 # Application configuration
├── requirements.txt          # Python dependencies
├── .env                       # Local environment configuration
├── .env.example                # Environment configuration template
├── .gitignore                   # Git ignored files
└── README.md                     # Backend documentation
```

---

## 📦 Sensor Data Format

The laptop Sensor Bridge sends sensor data in JSON format:

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

### Data Fields

| Field | Description |
|---|---|
| `temp` | Temperature in °C |
| `gas` | Gas sensor reading |
| `fire` | Fire detection status |
| `sos` | Emergency SOS status |
| `warning` | Warning status |
| `danger` | Danger status |
| `fan` | Fan status |

**Status field convention:**
- `0` = OFF / NORMAL
- `1` = ON / ACTIVE

---

## 🔌 WebSocket Endpoint

The main WebSocket endpoint is:

```
/ws
```

### 🛰️ Sensor Connection

The laptop Sensor Bridge connects using:

```
/ws?role=sensor
```

**Example:**
```
wss://your-backend.onrender.com/ws?role=sensor
```

> The sensor client sends JSON data to the backend.

### 🖥️ Dashboard Connection

The web dashboard connects using:

```
/ws?role=dashboard
```

**Example:**
```
wss://your-backend.onrender.com/ws?role=dashboard
```

> The dashboard receives the latest sensor data broadcast by the backend.

---

## 🔄 WebSocket Flow

**Sensor →**
```
Laptop Sensor Bridge
        │  JSON
        ▼
FastAPI WebSocket
        │
        ▼
Connection Manager
```

**→ Dashboard**
```
Connection Manager
        │  JSON
        ▼
Web Dashboard
```

---

## 🌐 HTTP Endpoints

### `GET /`

Returns basic backend information.

```json
{
  "service": "Underground Mines Safety System",
  "status": "online",
  "version": "1.0.0",
  "websocket": "/ws"
}
```

### `GET /health`

Used to check whether the backend is healthy.

```json
{
  "status": "healthy",
  "clients": 2
}
```

> `clients` represents the total number of currently connected WebSocket clients.

---

## ⚙️ Local Development

**1. Create a virtual environment**
```bash
python -m venv venv
```

**2. Activate the environment**

- **Windows**
  ```bash
  venv\Scripts\activate
  ```
- **Linux / macOS**
  ```bash
  source venv/bin/activate
  ```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment**

Create a `.env` file:

```env
APP_NAME=Underground Mines Safety System
APP_VERSION=1.0.0

HOST=0.0.0.0
PORT=8000

ENVIRONMENT=development

CORS_ORIGINS=*
```

**5. Start the server**
```bash
uvicorn main:app --reload
```

The local backend will be available at:

| Type | URL |
|---|---|
| HTTP | `http://localhost:8000` |
| WebSocket | `ws://localhost:8000/ws` |

---

## ☁️ Render Deployment

Create a new **Web Service** on Render and connect this repository.

**Build Command**
```bash
pip install -r requirements.txt
```

**Start Command**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

> Render provides the `PORT` environment variable automatically.

### Render Environment Variables

Add these in the Render dashboard:

```env
APP_NAME=Underground Mines Safety System
APP_VERSION=1.0.0
ENVIRONMENT=production
CORS_ORIGINS=*
```

> ⚠️ Do **not** upload the local `.env` file to GitHub.

### Production WebSocket URLs

After deployment, the backend will be available at:

```
https://YOUR-SERVICE.onrender.com
```

| Client | URL |
|---|---|
| Sensor Bridge | `wss://YOUR-SERVICE.onrender.com/ws?role=sensor` |
| Dashboard | `wss://YOUR-SERVICE.onrender.com/ws?role=dashboard` |

---

## 🔄 Complete Data Flow

```
┌──────────────────────┐
│      Arduino UNO      │
│                        │
│ Temperature            │
│ Gas Sensor              │
│ Fire Sensor              │
│ SOS Button                │
│ Fan                         │
└──────────┬─────────────────┘
           │ USB Serial
           ▼
┌──────────────────────┐
│        Laptop         │
│                        │
│   Sensor Bridge        │
│ Serial Reader            │
│ WebSocket Client           │
└──────────┬─────────────────┘
           │ WSS
           ▼
┌──────────────────────┐
│   FastAPI — Render     │
│                        │
│ WebSocket Server        │
│ Connection Manager        │
└──────────┬─────────────────┘
           │ WSS
           ▼
┌──────────────────────┐
│    HTML Dashboard      │
│                        │
│ Temperature             │
│ Gas Level                 │
│ Fire Status                 │
│ SOS Status                    │
│ Warning                         │
│ Danger                            │
│ Fan Status                          │
└──────────────────────┘
```

---

## 🔒 Security Note

The current version is designed for a **project prototype and demonstration**.

For production deployment, consider adding:

- 🔑 WebSocket authentication
- 🪪 API keys or tokens
- ✅ Input validation
- 🚦 Rate limiting
- 🌐 Restricted CORS origins
- 🔐 HTTPS/WSS only
- 🛡️ Sensor client authentication

---

## 🏗️ Project Overview

**Underground Mines Safety System** — a real-time IoT-based monitoring system designed to monitor critical underground mining safety parameters and present them through a live web dashboard.

### 🧰 Technology Stack

| Layer | Technology |
|---|---|
| Hardware | Arduino UNO + Sensors |
| Laptop | Python + PySerial + WebSockets |
| Backend | FastAPI + WebSockets |
| Deployment | Render |
| Frontend | HTML + CSS + JavaScript |

---

## 📄 License

Add your license here (e.g., MIT).
