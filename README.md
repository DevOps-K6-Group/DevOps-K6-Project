## The project is a class work for a group of four MSc Software Engineering Students at the University of Bolton
 # The course is DevOps
 
 The aim of the course is to learn DevOps operations with a practical sotware solution
 
 This software is a web based currency converter
 It is built with Python, Django, HTML, CSS
 
 Thank you.


# Django Project

A comprehensive Django web application with instructions for setup and development.

## Table of Contents
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Running the Server](#running-the-server)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## Requirements

- Python 3.8+
- pip (Python package manager)
- virtualenv or venv (recommended)
- PostgreSQL (or your database of choice)

## Setup and Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/username/django-project.git
   cd django-project
   ```

2. **Create and activate a virtual environment**

   ```bash
   # Using virtualenv
   virtualenv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create an environment file**

   Copy the example environment file and update it with your settings:

   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file with your database credentials and other settings.

## Running the Server

1. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

2. **Create a superuser (admin)**

   ```bash
   python manage.py createsuperuser
   ```

3. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   The application will be available at http://127.0.0.1:8000/

## Project Structure

```
currency_converter/
├── manage.py
├── db.sqlite3
├── currency_converter/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── styles.css
│   │   ├── js/
│   │   │   ├── scripts.js
│   │   ├── images/
│   ├── templates/
│       ├── base.html
│       ├── converter/
│           ├── dashboard.html
│           ├── index.html
│           ├── login.html
│           ├── register.html
│   ├── media/ 
│       ├── profile_pictures/
│   ├── migrations/
│       ├── __init__.py
├── converter/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── userauths/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── requirements.txt
├── README.md
```

## Environment Variables

The following environment variables need to be set in your `.env` file:

- `DEBUG` - Set to True for development, False for production
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

## Database Setup

By default, the project uses SQLite for development. To set up a PostgreSQL database:

1. **Install PostgreSQL** and create a database

2. **Update your .env file** with the database connection details:

   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/database_name
   ```

3. **Run migrations**

   ```bash
   python manage.py migrate
   ```

## Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test apps.app_name
```
