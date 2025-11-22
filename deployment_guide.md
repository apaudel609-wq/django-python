# Deployment Guide: Containerized Environment

This guide outlines the steps to deploy the Finance Tracker application using **Docker**, **Gunicorn**, and **Nginx**. This architecture ensures scalability, security, and performance.

## Architecture Overview

1.  **Django Application**: The core web app.
2.  **Gunicorn**: A production-grade WSGI HTTP server that runs the Python code.
3.  **Nginx**: A high-performance reverse proxy that handles static files and forwards requests to Gunicorn.
4.  **PostgreSQL** (Recommended): A robust database for production (replacing SQLite).
5.  **Docker**: Containers to package all the above services consistently.

---

## 1. Dockerfile (The Application Image)

Create a `Dockerfile` in the project root to build the Django app image.

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn

# Copy project
COPY . /app/

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "finance_tracker.wsgi:application"]
```

## 2. Docker Compose (Orchestration)

Create a `docker-compose.yml` to run the App, DB, and Nginx together.

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn finance_tracker.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/static
    expose:
      - 8000
    env_file:
      - .env

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/static
    depends_on:
      - web

volumes:
  static_volume:
```

## 3. Nginx Configuration

Create `nginx/nginx.conf` to handle routing.

```nginx
upstream finance_tracker {
    server web:8000;
}

server {
    listen 80;

    location / {
        proxy_pass http://finance_tracker;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /app/static/;
    }
}
```

## 4. Environment Variables (.env)

**NEVER** commit secrets to version control. Create a `.env` file on the server:

```ini
DEBUG=0
SECRET_KEY=your-production-secret-key-change-this
ALLOWED_HOSTS=yourdomain.com,127.0.0.1
DATABASE_URL=postgres://user:password@db:5432/dbname
```

## 5. Deployment Steps

1.  **Build and Run**:
    ```bash
    docker-compose up -d --build
    ```
2.  **Collect Static Files**:
    ```bash
    docker-compose exec web python manage.py collectstatic --no-input
    ```
3.  **Run Migrations**:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

## Summary
By following this guide, you ensure that your application is:
*   **Portable**: Runs the same on any machine with Docker.
*   **Scalable**: Can handle more traffic via Gunicorn/Nginx.
*   **Secure**: Separates concerns and hides the app server behind a proxy.
