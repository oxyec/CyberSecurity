# CyberSecurity Project

This repository contains a Django backend and a React frontend.

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Getting Started

### Backend (Django)

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Install dependencies (if you haven't already):
    ```bash
    pip install django django-sslserver django-widget-tweaks django-tailwind django-tinymce argon2-cffi bcrypt bleach django-browser-reload Pillow feedparser requests
    ```

3.  Apply database migrations:
    ```bash
    python manage.py migrate
    ```

4.  **Fetch Latest News** (Optional but recommended):
    ```bash
    python manage.py fetch_news
    ```
    This command scrapes the latest cybersecurity news from various RSS feeds and populates the database.

5.  Start the development server:
    ```bash
    python manage.py runserver
    ```
    The backend will run at `http://127.0.0.1:8000/`.

### Frontend (React + Vite)

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Start the development server:
    ```bash
    npm run dev
    ```
    The frontend will typically run at `http://localhost:5173/`.

## Project Structure

-   `backend/`: Django project files (settings in `backend/websitebackend/`).
-   `frontend/`: React application (Vite).
