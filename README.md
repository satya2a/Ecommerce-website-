# Simple E-commerce Store — Django

A complete beginner-friendly e-commerce website built with Django, SQLite, HTML, CSS and JavaScript.

## Features
- Product listing and search
- Product details page
- Session-based shopping cart
- Quantity update/remove from cart
- User registration, login and logout
- Checkout and order processing
- Order history for logged-in users
- Django admin for products/orders/users
- Responsive UI
- SQLite database

## Setup

### 1. Create/activate a virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create database
```bash
python manage.py migrate
```

### 4. Add demo products
```bash
python manage.py seed_products
```

### 5. Create admin account
```bash
python manage.py createsuperuser
```

### 6. Start server
```bash
python manage.py runserver
```

Open:
- Store: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Important
This is a learning/demo project. For production, add payment gateway integration, stronger validation, email, deployment settings, environment variables, database such as PostgreSQL, image uploads, security hardening and proper order/payment states.
