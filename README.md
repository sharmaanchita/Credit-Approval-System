# Credit Approval System

## Project Description
The **Credit Approval System** is built to process past customer and loan data to approve credit applications. This project demonstrates Python/Django proficiency, the use of background tasks, and database operations.

---

## Features
- Automated ingestion of customer and loan data using background workers.
- RESTful APIs with proper error handling and status codes.
- Fully containerized using Docker for consistent environments.
- PostgreSQL as the primary database.

---

## Requirements
- Python 3.10
- Django 4+
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sharmaanchita/Credit-Approval-System.git
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt     
```

### 3. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
``` 

### 4. Start the Development Server
```bash
python manage.py runserver
```

### 5. Running Tests
```bash
python manage.py test loans
```



