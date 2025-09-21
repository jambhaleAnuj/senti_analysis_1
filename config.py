"""Central configuration module.

Loads environment variables and exposes constants used across the app.
Provides sensible fallbacks for educational use while encouraging
secure configuration for production deployments.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY: str = os.getenv("OMDB_API_KEY", "36650a58")  # demo key fallback
YOUTUBE_API_KEY: str | None = os.getenv("YOUTUBE_API")
FLASK_DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() == "true"
TMDB_BEARER: str | None = os.getenv("TMDB_BEARER")
