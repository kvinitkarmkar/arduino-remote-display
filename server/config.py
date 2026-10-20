"""
Application Configuration
-------------------------

Central place for backend configuration.

Environment variables can be provided through
Render Environment Variables or a local .env file.
"""

import os

from dotenv import load_dotenv


# ---------------------------------------------------------
# Load .env
# ---------------------------------------------------------
# Useful during local development.
#
# On Render, environment variables can be configured
# directly from the Render dashboard.
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Application Information
# ---------------------------------------------------------

APP_NAME = os.getenv(
    "APP_NAME",
    "Underground Mines Safety System"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)


# ---------------------------------------------------------
# Server Configuration
# ---------------------------------------------------------

HOST = os.getenv(
    "HOST",
    "0.0.0.0"
)

# Render provides the PORT environment variable.
# Locally, 8000 will be used if PORT is not defined.

PORT = int(
    os.getenv(
        "PORT",
        "8000"
    )
)


# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
# During development, "*" allows requests from any
# frontend origin.
#
# For production, you can replace this with your actual
# frontend domain.
# ---------------------------------------------------------

CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "*"
).split(",")
