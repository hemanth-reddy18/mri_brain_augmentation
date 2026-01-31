# Deploy MRI App

## Goal
Run the MRI application locally, ensuring all dependencies are installed and the server starts correctly.

## Proposed Changes
No code changes are anticipated. 
We will execute `run.sh` which:
1. Installs dependencies from `requirements.txt`.
2. Starts the FastAPI server (`mri/server.py`).

## Verification Plan
### Automated Verification
- Run `curl -I http://localhost:8000` to verify the server is responding.
- Check terminal output for startup logs.
