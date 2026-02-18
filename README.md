# CyberSecurity Platform (BECAUSE OF OTHER PROJECTS THİS PROJECT İS NO LONGER GETTİNG DEVELOPED)

A Django + React web application for aggregating cybersecurity news, blogging, and user behavior analysis.

> **Status:** Work in progress

## Features

- **News Aggregation** - Fetches cybersecurity news from configurable RSS feeds (The Hacker News, BleepingComputer, Wired Security, etc.)
- **Blog / Forum** - Create posts and threaded comments with HTML sanitization
- **User Accounts** - Custom user model with profiles, student ID, and GitHub handle
- **Behavior Analysis** - Login attempt tracking, IP monitoring, and anomaly detection
- **Security** - Argon2 password hashing, CSRF protection, HSTS headers in production

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Getting Started

### 1. Clone and configure

```bash
git clone <repo-url>
cd CyberSecurity
```

### 2. Backend setup

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and set DJANGO_SECRET_KEY (see .env.example for instructions)

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Fetch initial news
python manage.py fetch_news

# Start the dev server
python manage.py runserver
```

The backend runs at `http://127.0.0.1:8000/`.

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173/` and proxies `/api` requests to the Django backend.

## Project Structure

```
CyberSecurity/
├── backend/
│   ├── account/          # User management, login tracking, behavior analysis
│   ├── blog/             # Blog posts and comments
│   ├── haberler/         # News aggregation (RSS feeds + web scraping)
│   ├── websitebackend/   # Django project settings and root URL config
│   ├── templates/        # HTML templates
│   ├── theme/            # Tailwind CSS theme
│   ├── requirements.txt  # Python dependencies
│   └── .env.example      # Environment variable template
├── frontend/
│   ├── src/              # React application source
│   └── vite.config.js    # Vite config with backend proxy
└── README.md
```

## Configuration

All configuration is done through environment variables. See `backend/.env.example` for the full list.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | Yes | - | Django secret key |
| `DEBUG` | No | `False` | Enable debug mode |
| `ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `DATABASE_ENGINE` | No | `sqlite3` | Database backend |
| `DATABASE_NAME` | No | `db.sqlite3` | Database name |




## License

This project is for educational purposes.
