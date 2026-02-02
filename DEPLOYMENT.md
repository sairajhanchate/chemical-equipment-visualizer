# Deployment Guide

This guide explains how to upload your project to GitHub and deploy the "Hybrid" web application.

## 1. Upload to GitHub

The project is already initialized as a Git repository.

1.  **Create a new repository** on [GitHub](https://github.com/new).
    *   Name it `chemical-equipment-visualizer` (or similar).
    *   Do **not** check "Initialize with README", .gitignore, or license (we already have them).

2.  **Push your code**:
    Run the following commands in your terminal (replace `YOUR_USERNAME` with your GitHub username):

    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/chemical-equipment-visualizer.git
    git branch -M main
    git push -u origin main
    ```

## 2. Deploy Web App (Backend + Frontend)

The easiest way to deploy this Django + React app is using **Render** or **Heroku**. This guide uses **Render** (free tier available).

### Prerequisites
- GitHub account
- Render account (https://render.com)

### Steps

1.  **Sign up/Log in to Render**.
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub account and select the `chemical-equipment-visualizer` repository.
4.  Configure the service:
    *   **Name**: `equipment-visualizer`
    *   **Region**: Closest to you (e.g., Singapore/Ohio)
    *   **Branch**: `main`
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt && python backend/manage.py collectstatic --noinput && python backend/manage.py migrate`
    *   **Start Command**: `gunicorn backend.backend.wsgi:application`
5.  **Environment Variables**:
    Add the following environment variables in the "Environment" tab:
    *   `PYTHON_VERSION`: `3.10.12` (or similar stable version)
    *   `SECRET_KEY`: (Generate a random string)
    *   `DEBUG`: `False`
    *   `ALLOWED_HOSTS`: `*` (or your render URL)
6.  Click **Create Web Service**.

### Frontend Note
Since this is a hybrid app, the Django backend can serve the frontend if you build it and place it in the static files, OR you can deploy the frontend separately on **Vercel** or **Netlify** (Recommended for better performance).

#### Option A: Deploy Frontend on Vercel (Recommended)
1.  Go to [Vercel](https://vercel.com) and Import Project.
2.  Select your GitHub repo.
3.  Select `frontend` as the **Root Directory**.
4.  Build Command: `npm run build`
5.  Output Directory: `build`
6.  **IMPORTANT**: You will need to update the `API_BASE_URL` in your frontend code (`frontend/src/services/api.js`) to point to your new Render Backend URL (e.g., `https://equipment-visualizer.onrender.com/api`).

## 3. Desktop App Distribution
To let others use the desktop app:
1.  They need Python installed.
2.  They can clone the repo.
3.  Run `pip install -r requirements.txt`.
4.  Run `python desktop-files/main.py`.

*Alternatively, you can use PyInstaller to create an `.exe` file.*
