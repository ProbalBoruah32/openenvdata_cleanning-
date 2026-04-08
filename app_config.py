"""
Explicit app configuration to resolve HF Spaces deployment issues.
This ensures the FastAPI app instance is available at module level.
"""

from server.app import app, main

# Ensure app is importable as: from app_config import app
# And main is available as: from app_config import main

__all__ = ['app', 'main']
