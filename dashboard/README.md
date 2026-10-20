# Dashboard

Web-based digital display for Arduino Remote Display, designed to visualize incoming sensor data through a custom interface.

## 🌐 Live Demo

[**Open Live Dashboard →**](YOUR_LIVE_DISPLAY_URL)

## 🖥️ Preview

<p align="center">
  <img src="../docs/images/dashboard-preview.png" alt="Arduino Remote Display Dashboard" width="100%">
</p>

## ✨ Features

- **Custom Digital Display:** A dedicated interface for presenting sensor readings.
- **Live Data Visualization:** Display incoming Arduino data.
- **WebSocket Communication:** Receive data through a WebSocket connection.
- **Remote Monitoring:** Access the dashboard from another device when network and server configuration permit.

## ⚙️ Configuration

Configure the dashboard to connect to the appropriate WebSocket server endpoint.

Ensure the server and serial bridge are running and transmitting data in the expected format.

## 📁 Related Components

- `../hardware/arduino-uno/` — Arduino firmware.
- `../bridge/` — Python serial bridge.
- `../server/` — WebSocket server.

## ⚠️ Safety Notice

This dashboard is an experimental prototype for educational and development purposes. It is not certified mine-safety equipment and must not be used as the sole basis for safety-critical decisions.
