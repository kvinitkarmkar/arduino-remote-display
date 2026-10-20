"""
Application configuration.

Loads Arduino serial and backend WebSocket settings
from environment variables.
"""

import os
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()


# Arduino configuration
ARDUINO_PORT = os.getenv("ARDUINO_PORT", "COM6")
BAUD_RATE = int(os.getenv("BAUD_RATE", "9600"))


# Render FastAPI WebSocket endpoint
BACKEND_WS_URL = os.getenv(
    "BACKEND_WS_URL",
    "wss://engineer-day-2026-backend.onrender.com/ws"
)


# Serial read timeout in seconds
SERIAL_TIMEOUT = float(os.getenv("SERIAL_TIMEOUT", "1"))
