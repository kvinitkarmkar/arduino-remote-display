"""
Underground Mines Safety System
--------------------------------
FastAPI WebSocket Backend

Data Flow:

Arduino UNO
    ↓ USB Serial
Laptop Sensor Bridge
    ↓ WebSocket
This FastAPI Server (Render)
    ↓ WebSocket Broadcast
HTML Dashboard(s)
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from config import APP_NAME, APP_VERSION
from websocket_manager import ConnectionManager


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Real-time Underground Mines Safety Monitoring Backend",
)


# ---------------------------------------------------------
# WebSocket Connection Manager
# ---------------------------------------------------------

manager = ConnectionManager()


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
# Render and monitoring services can use this endpoint
# to verify that the backend is running.
# ---------------------------------------------------------

@app.get("/")
async def root():
    """
    Basic API information endpoint.
    """

    return {
        "service": APP_NAME,
        "status": "online",
        "version": APP_VERSION,
        "websocket": "/ws",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns the current backend status and
    number of connected WebSocket clients.
    """

    return {
        "status": "healthy",
        "clients": manager.client_count,
    }


# ---------------------------------------------------------
# WebSocket Endpoint
# ---------------------------------------------------------
# Both the laptop sensor bridge and web dashboards can
# connect through this endpoint.
#
# The server identifies the sender using the "role"
# query parameter:
#
#   /ws?role=sensor
#   /ws?role=dashboard
#
# Example:
#
# Laptop:
# wss://your-backend.onrender.com/ws?role=sensor
#
# Browser:
# wss://your-backend.onrender.com/ws?role=dashboard
# ---------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handle WebSocket connections.

    Sensor clients:
        Receive Arduino data and broadcast it.

    Dashboard clients:
        Receive live sensor data from the server.
    """

    # Get client role from query parameter.
    # Default role is dashboard.
    role = websocket.query_params.get("role", "dashboard").lower()

    # Only allow known roles.
    if role not in {"sensor", "dashboard"}:
        await websocket.close(code=1008)
        return

    # Accept and register the connection.
    await manager.connect(websocket, role)

    try:

        # -------------------------------------------------
        # Sensor Client
        # -------------------------------------------------

        if role == "sensor":

            while True:
                # Wait for JSON data from the laptop.
                data = await websocket.receive_json()

                # Broadcast the sensor data to dashboards.
                await manager.broadcast_to_dashboards(data)

        # -------------------------------------------------
        # Dashboard Client
        # -------------------------------------------------

        else:

            while True:
                # Dashboards normally only receive data.
                #
                # We still wait for incoming messages so
                # that disconnects can be detected cleanly.
                await websocket.receive_text()

    except WebSocketDisconnect:

        # Client disconnected normally.
        manager.disconnect(websocket)

    except Exception as error:

        # Log unexpected WebSocket errors.
        print(f"[WS] Connection error ({role}): {error}")

        manager.disconnect(websocket)
