# Deploying Your MRI App from GitHub

Since your application requires a **Python backend** (to process MRI files and serve the API), you cannot use **GitHub Pages** (which only hosts static HTML/CSS).

Instead, you use a cloud provider that **connects to your GitHub repository** and builds your app automatically whenever you push code. **Render** is the easiest free option for this type of app.

## Step-by-Step Guide (Render)

### 1. Create a Render Account
1.  Go to [dashboard.render.com](https://dashboard.render.com/).
2.  Sign up or Log in using your **GitHub account**. This creates the link between Render and your code.

### 2. Create a "Web Service"
1.  On the Render dashboard, click the **"New +"** button.
2.  Select **"Web Service"**.
3.  You will see a list of your GitHub repositories. Find `mri_brain_augmentation` and click **"Connect"**.
    *   *If you don't see it, click "Configure account" on the right to grant Render permission to access your repositories.*

### 3. Configure the Deployment
Render will try to auto-detect settings, but verify them against this list:

*   **Name**: `mri-app` (or any unique name)
*   **Region**: Choose the one closest to you (e.g., Singapore, Frankfurt, Oregon).
*   **Branch**: `main`
*   **Runtime**: `Python 3`
*   **Build Command**: `pip install -r requirements.txt`
*   **Start Command**: `uvicorn mri.server:app --host 0.0.0.0 --port $PORT`
    *   *Note: Render might auto-fill this because we added a `Procfile`.*
*   **Instance Type**: Select **"Free"**.

### 4. Deploy
1.  Click **"Create Web Service"**.
2.  Render will start building your app. You will see a terminal window showing logs (installing dependencies, etc.).
3.  Once it says "Live", your app is online!
4.  The URL will be shown at the top (e.g., `https://mri-app.onrender.com`).

## Updates
Whenever you change your code and push to GitHub:
```bash
git add .
git commit -m "Fixed a bug"
git push origin main
```
Render will handle the rest! It detects the new commit and automatically re-deploys your site.
