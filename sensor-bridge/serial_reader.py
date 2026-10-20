"""
Arduino Serial Reader.

Responsible for:
    Arduino UNO → USB → Serial/COM Port → Python
"""

import json
import serial

from config import ARDUINO_PORT, BAUD_RATE, SERIAL_TIMEOUT


class ArduinoSerialReader:
    """Reads JSON sensor data from Arduino over Serial."""

    def __init__(self):
        self.port = ARDUINO_PORT
        self.baud_rate = BAUD_RATE
        self.timeout = SERIAL_TIMEOUT
        self.connection = None

    def connect(self):
        """Open the Arduino serial connection."""

        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=self.timeout,
            )

            print(
                f"[SERIAL] Connected to Arduino "
                f"on {self.port} @ {self.baud_rate} baud"
            )

        except serial.SerialException as error:
            print(f"[SERIAL] Connection failed: {error}")
            raise

    def read_data(self):
        """
        Read one line from Arduino and convert it to JSON.

        Returns:
            dict | None: Parsed sensor data or None if invalid.
        """

        if self.connection is None:
            raise RuntimeError("Serial connection is not open.")

        try:
            raw_data = self.connection.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not raw_data:
                return None

            # Convert Arduino JSON string into Python dictionary
            data = json.loads(raw_data)

            return data

        except json.JSONDecodeError:
            print(f"[SERIAL] Invalid JSON received: {raw_data}")
            return None

        except serial.SerialException as error:
            print(f"[SERIAL] Read error: {error}")
            return None

    def close(self):
        """Close the serial connection."""

        if self.connection and self.connection.is_open:
            self.connection.close()
            print("[SERIAL] Connection closed.")
