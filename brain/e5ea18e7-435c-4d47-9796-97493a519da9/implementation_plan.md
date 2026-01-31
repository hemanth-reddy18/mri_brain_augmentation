# MRI Web Viewer Deployment Plan (Updated for NeuroGAN)

## Goal
Deploy the user's provided `mri.html` (NeuroGAN) as the main web interface.

## User Review Required
> [!WARNING]
> **Missing API Key**: The provided code requires a Google Gemini API key (`const apiKey = "";`) to function fully (chat and analysis). I will deploy it with the empty key, so AI features will need a key to work.

## Proposed Changes

### Frontend (`index.html`)
- **[REPLACE]** Overwrite `index.html` with the content of `mri.html`.
- This switches the app from a simple Slice Viewer to the "NeuroGAN" dashboard.

### Backend (`mri/server.py`)
- No changes required. The server still serves `index.html`. 
- *Note*: The new frontend does not currently use the `/api/slice` endpoints, but they will remain available if we want to integrate them later.

## Verification Plan
1.  **Deploy**: Overwrite `index.html`.
2.  **Verify**: Reload `http://localhost:8000`.
3.  **Check**: Ensure the React app loads (Hero section, Navigation).
