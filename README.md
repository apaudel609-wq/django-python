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

## Comprehensive Finance Tracker Report

### 1. Financial Foundation & Data Integrity
*   **Core Models**: Implemented `Category` and `Transaction` models (`models.py`) to structure financial data effectively.
*   **Precision**: Utilized `DecimalField` (12 max digits, 2 decimal places) for all monetary values. This is a critical fintech standard, as `FloatField` uses approximations that lead to cumulative errors, whereas `DecimalField` guarantees mathematical precision.
*   **Constraints**: Enforced unique categories per user via `unique_together = ('name', 'user')` constraints in the Category model, ensuring organization and privacy.
*   **Validation**: Implemented robust validation in `TransactionForm` (`forms.py`), including custom `clean_amount()` to ensure positive values and `clean_date()` to prevent future-dated transactions, essential for accurate real-time reporting.
*   **Basic CRUD**: Established `ListView` and `CreateView` to demonstrate immediate application of models and forms.

### 2. Security & Multi-User Scalability
*   **Authentication**: Integrated `django-allauth` to allow secure sign-up and login via social providers (Google/GitHub). This aligns with real-world production standards, avoiding insecure custom username/password flows.
*   **User Isolation**: Applied strict user scoping where all views and forms automatically associate data with `request.user`. This ensures all data belongs to a specific `user_id`, a core principle of multi-tenant applications.
*   **Authorization**: Implemented `get_queryset()` filtering in all list/detail views. This is a security essential to prevent Insecure Direct Object Reference (IDOR) vulnerabilities, ensuring users can only access their own data.
*   **Access Control**: Secured all application endpoints using `@login_required` decorators or `LoginRequiredMixin`.

### 3. Modern Backend Architecture
*   **REST API**: Configured Django REST Framework (DRF), the industry standard for building RESTful APIs in Django, to support future modern web/mobile clients.
*   **Serialization**: Created `TransactionSerializer` to securely translate Python models to JSON, handling `DecimalField` precision and input validation correctly.
*   **ViewSets**: Implemented `TransactionViewSet` to provide authenticated CRUD operations, leveraging DRF's built-in filtering and pagination for efficiency.
*   **Service Layer**: Established a Service Layer pattern (`services/financial.py`) to decouple business logic from models and views, enhancing maintainability and testability.

### 4. Reporting & User Interface
*   **Dashboard**: Developed a `DashboardView` that serves as a central hub, retrieving the user's latest 10 transactions and overall Month-to-Date (MTD) Net Balance.
*   **Visualization**: Designed a responsive `dashboard.html` template using Tailwind CSS for professional presentation across devices.
*   **Analytics**: Enhanced the service layer to calculate MTD Net Balance (Income - Expenses) using efficient ORM aggregation (`Sum` and `Filter`), introducing basic OLAP techniques.
*   **Deployment Readiness**: Documented necessary steps for containerized deployment (Docker/Gunicorn/Nginx) to prepare for scalability.
