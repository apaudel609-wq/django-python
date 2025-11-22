# Finance Tracker

A Django-based personal finance management application that allows users to track their income and expenses, manage categories, and view their financial health.

## Features

*   **User Authentication**: Secure login and registration system, including social authentication via Google and GitHub (using `django-allauth`).
*   **Transaction Tracking**: Record income and expense transactions with details like amount, date, and notes.
*   **Category Management**: Create and manage custom categories for transactions.
*   **User Scoping**: All data (transactions and categories) is scoped to the logged-in user, ensuring privacy.
*   **Financial Precision**: Uses `DecimalField` for all monetary values to ensure accuracy.
*   **REST API**: Includes support for API endpoints (via Django REST Framework).

## Tech Stack

*   **Backend**: Django 5.2.8
*   **Database**: SQLite (default)
*   **Authentication**: Django Allauth
*   **API**: Django REST Framework

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/apaudel609-wq/django-python.git
    cd django-python
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (optional):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the application:**
    Open your browser and go to `http://127.0.0.1:8000/`.

## Configuration

*   **Social Login**: To enable Google or GitHub login, you need to configure the Social Applications in the Django Admin (`/admin/`) and add your Client IDs and Secrets.
