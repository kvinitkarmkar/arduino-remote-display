"""
Underground Mines Safety System
Sensor Bridge

Data Flow:

Arduino UNO
    ↓ USB Serial
Laptop
    ↓
Python Sensor Bridge
    ↓ WebSocket
Render FastAPI Backend
"""

import asyncio

from config import BACKEND_WS_URL
from serial_reader import ArduinoSerialReader
from websocket_client import BackendWebSocketClient


async def main():
    """Run the sensor bridge."""

    print("=" * 60)
    print(" Underground Mines Safety System - Sensor Bridge")
    print("=" * 60)

    # ---------------------------------------------------------
    # Initialize Arduino Serial Reader
    # ---------------------------------------------------------

    arduino = ArduinoSerialReader()

    # ---------------------------------------------------------
    # Initialize Backend WebSocket Client
    # ---------------------------------------------------------

    backend = BackendWebSocketClient(BACKEND_WS_URL)

    try:
        # Connect Arduino
        arduino.connect()

        # Connect Render backend
        await backend.connect()

        print("[SYSTEM] Sensor bridge started.")
        print("[SYSTEM] Waiting for Arduino data...\n")

        # -----------------------------------------------------
        # Main data forwarding loop
        # -----------------------------------------------------

        while True:

            # Read one JSON object from Arduino
            sensor_data = arduino.read_data()

            if sensor_data is None:
                continue

            # Display received data
            print(f"[ARDUINO] Received: {sensor_data}")

            # Send data to Render backend
            await backend.send_data(sensor_data)

            # Prevent unnecessary CPU usage
            await asyncio.sleep(0.01)

    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutdown requested.")

    except Exception as error:
        print(f"[SYSTEM] Error: {error}")

    finally:
        # Always close connections properly
        arduino.close()
        await backend.close()

        print("[SYSTEM] Sensor bridge stopped.")


if __name__ == "__main__":
    asyncio.run(main())
