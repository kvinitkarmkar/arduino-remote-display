"""
WebSocket Client.

Responsible for:
    Python Sensor Bridge → Render FastAPI WebSocket
"""

import json
import asyncio
import websockets


class BackendWebSocketClient:
    """Maintains a WebSocket connection with the backend."""

    def __init__(self, backend_url: str):
        self.backend_url = backend_url
        self.websocket = None

    async def connect(self):
        """Connect to the Render WebSocket server."""

        self.websocket = await websockets.connect(
            self.backend_url
        )

        print(f"[WS] Connected to backend: {self.backend_url}")

    async def send_data(self, data: dict):
        """Send sensor data to the backend."""

        if self.websocket is None:
            raise RuntimeError("WebSocket is not connected.")

        message = json.dumps(data)

        await self.websocket.send(message)

        print(f"[WS] Sent: {message}")

    async def close(self):
        """Close the WebSocket connection."""

        if self.websocket:
            await self.websocket.close()
            print("[WS] Connection closed.")
