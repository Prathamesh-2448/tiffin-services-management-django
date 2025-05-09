# Tiffin Services Management System

A Django-based web application for managing a tiffin (meal delivery) service. It includes customer management, meal option tracking, daily delivery records, and admin functionalities.

## Features

- Customer and subscription management
- Meal options and extras tracking
- Daily delivery and billing reports
- Admin interface for full control
- Deployment-ready with Gunicorn and Docker

## Requirements

- Python 3.12
- Django
- Gunicorn (for production)
- Docker (for containerized deployment)

---

## 🛠️ Setup Instructions (Development Server)

### 1. Clone the Repository

```bash
git clone https://github.com/Prathamesh-2448/tiffin-services-management-django.git
cd tiffin-services-management-django
```

### 2. Create Virtual Environment (Optional but Recommended)

#### For Linux
```bash
python -m venv venv
source venv/bin/activate
```

#### For Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Admin Login)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ on your browser

## 🚀 Docker Deployment

### 1. Build Docker Image

```bash
docker build -t tiffin-app .
```

### 2. Run Container

```bash
docker run -d -p 8000:8000 tiffin-app
```
