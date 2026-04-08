# Data Cleaning Environment - Deployment

## Quick Start for HF Spaces

The application is configured to run on port 7860.

**Server Entry Point:** `server.app:main`

**To start locally:**
```bash
python -m server.app
```

**To run with uvicorn:**
```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

## Deployment Configuration

- **App file:** server/app.py
- **Main function:** Available for import as `from server.app import main`
- **FastAPI app:** Available as `from server.app import app`
- **Port:** 7860

All deployment requirements are configured in `pyproject.toml` and `Spacefile`.
