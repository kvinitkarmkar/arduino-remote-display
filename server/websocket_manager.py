"""
WebSocket Connection Manager
----------------------------

Responsible for:

1. Managing connected WebSocket clients.
2. Separating sensor clients from dashboard clients.
3. Broadcasting sensor data to dashboards.
4. Cleaning up disconnected clients.
"""

from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    """
    Central manager for all active WebSocket connections.
    """

    def __init__(self):
        # -------------------------------------------------
        # Store sensor connections.
        #
        # Example:
        # {
        #     websocket_object: "sensor"
        # }
        # -------------------------------------------------

        self.sensor_clients: Dict[WebSocket, str] = {}

        # -------------------------------------------------
        # Store dashboard connections.
        #
        # Multiple browsers can connect simultaneously.
        # -------------------------------------------------

        self.dashboard_clients: Dict[WebSocket, str] = {}

    # -----------------------------------------------------
    # Connect Client
    # -----------------------------------------------------

    async def connect(self, websocket: WebSocket, role: str):
        """
        Accept and register a new WebSocket connection.
        """

        # Accept WebSocket handshake.
        await websocket.accept()

        # Store the connection according to its role.
        if role == "sensor":
            self.sensor_clients[websocket] = role

            print(
                f"[WS] Sensor connected | "
                f"Sensors: {len(self.sensor_clients)}"
            )

        else:
            self.dashboard_clients[websocket] = role

            print(
                f"[WS] Dashboard connected | "
                f"Dashboards: {len(self.dashboard_clients)}"
            )

    # -----------------------------------------------------
    # Disconnect Client
    # -----------------------------------------------------

    def disconnect(self, websocket: WebSocket):
        """
        Remove a disconnected WebSocket client.
        """

        if websocket in self.sensor_clients:
            del self.sensor_clients[websocket]

            print(
                f"[WS] Sensor disconnected | "
                f"Sensors: {len(self.sensor_clients)}"
            )

        elif websocket in self.dashboard_clients:
            del self.dashboard_clients[websocket]

            print(
                f"[WS] Dashboard disconnected | "
                f"Dashboards: {len(self.dashboard_clients)}"
            )

    # -----------------------------------------------------
    # Broadcast to Dashboards
    # -----------------------------------------------------

    async def broadcast_to_dashboards(self, data: dict):
        """
        Send sensor data to every connected dashboard.

        Example data:

        {
            "temp": 28.0,
            "gas": 125,
            "fire": 0,
            "sos": 0,
            "warning": 0,
            "danger": 0,
            "fan": 0
        }
        """

        # If there are no dashboards, there is nothing
        # to broadcast.
        if not self.dashboard_clients:
            return

        # Keep track of clients that disconnected
        # during broadcasting.
        disconnected_clients = []

        # Send the same data to every dashboard.
        for websocket in list(self.dashboard_clients.keys()):

            try:
                await websocket.send_json(data)

            except Exception as error:

                print(
                    f"[WS] Dashboard send failed: {error}"
                )

                disconnected_clients.append(websocket)

        # Remove failed connections.
        for websocket in disconnected_clients:
            self.disconnect(websocket)

    # -----------------------------------------------------
    # Client Count
    # -----------------------------------------------------

    @property
    def client_count(self) -> int:
        """
        Return total number of connected clients.
        """

        return (
            len(self.sensor_clients)
            + len(self.dashboard_clients)
        )

    # -----------------------------------------------------
    # Dashboard Count
    # -----------------------------------------------------

    @property
    def dashboard_count(self) -> int:
        """
        Return number of connected dashboards.
        """

        return len(self.dashboard_clients)

    # -----------------------------------------------------
    # Sensor Count
    # -----------------------------------------------------

    @property
    def sensor_count(self) -> int:
        """
        Return number of connected sensor bridges.
        """

        return len(self.sensor_clients)
