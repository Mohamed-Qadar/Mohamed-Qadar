# National Citizen Feedback & Smart Governance System
# Quick Setup Guide

## Prerequisites
- Python 3.10+
- PostgreSQL 13+
- pip (Python package manager)
- Git

## Quick Start (5 minutes)

### 1. Clone and Navigate
```bash
cd core
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
# Create PostgreSQL database
createdb citizen_feedback

# Or use PostgreSQL prompt:
psql -U postgres
CREATE DATABASE citizen_feedback;
\q
```

### 5. Configure Environment
Create a `.env` file in the core directory:
```env
DB_NAME=citizen_feedback
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
```

### 6. Run Migrations
```bash
python manage.py makemigrations users
python manage.py makemigrations institutions
python manage.py makemigrations complaints
python manage.py makemigrations messaging
python manage.py makemigrations analytics
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### 8. Load Sample Data (Optional)
```bash
python manage.py shell
```
```python
from institutions.models import Institution
from users.models import User

# Create sample institutions
Institution.objects.create(
    name="Ministry of Health",
    institution_type="ministry",
    description="Manages national health services",
    email="health@gov.example",
    phone="+1234567890"
)

Institution.objects.create(
    name="Ministry of Education",
    institution_type="ministry",
    description="Oversees national education system",
    email="education@gov.example",
    phone="+1234567891"
)

Institution.objects.create(
    name="Ministry of Infrastructure",
    institution_type="ministry",
    description="Manages roads, bridges, and public infrastructure",
    email="infrastructure@gov.example",
    phone="+1234567892"
)

# Create a presidency user
presidency_user = User.objects.create_user(
    username='presidency_admin',
    email='presidency@gov.example',
    password='admin123',
    role='presidency',
    first_name='Presidency',
    last_name='Admin'
)
presidency_user.is_verified = True
presidency_user.save()

# Create a government user
health_ministry = Institution.objects.get(name="Ministry of Health")
gov_user = User.objects.create_user(
    username='health_official',
    email='official@health.gov.example',
    password='health123',
    role='government',
    first_name='Health',
    last_name='Official',
    institution=health_ministry
)
gov_user.is_verified = True
gov_user.save()

exit()
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Default Test Accounts

After loading sample data, you can use these accounts:

### Presidency Account
- Username: `presidency_admin`
- Password: `admin123`
- Role: Presidency (Full Access)

### Government Official Account
- Username: `health_official`
- Password: `health123`
- Role: Government (Ministry of Health)

### Citizen Account
Register a new citizen account through the web interface at:
http://127.0.0.1:8000/register/citizen/

## Common Commands

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### Run Tests
```bash
python manage.py test
```

### Start Django Shell
```bash
python manage.py shell
```

## Access Points

- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Citizen Registration**: http://127.0.0.1:8000/register/citizen/
- **Government Registration**: http://127.0.0.1:8000/register/government/
- **Login**: http://127.0.0.1:8000/login/

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `.env` file
- Verify database exists: `psql -U postgres -l`

### Migration Errors
```bash
# Reset migrations (DEVELOPMENT ONLY)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Port Already in Use
```bash
# Use a different port
python manage.py runserver 8001
```

## Project Structure Overview

```
core/
├── core/                 # Project settings
├── users/               # User management
├── complaints/          # Complaint system
├── institutions/        # Government institutions
├── messaging/          # Communication system
├── analytics/          # Analytics & AI
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── manage.py           # Django management script
```

## Next Steps

1. Explore the admin panel: http://127.0.0.1:8000/admin/
2. Create sample institutions via admin
3. Register test citizen accounts
4. Submit test complaints
5. Assign complaints to institutions
6. Test the complete workflow

## Production Deployment

For production deployment:
1. Set `DEBUG=False` in settings
2. Configure proper `SECRET_KEY`
3. Set up proper database with backups
4. Use a production server (Gunicorn + Nginx)
5. Enable HTTPS
6. Configure email backend
7. Set up monitoring and logging

## Support

For issues or questions:
- Email: mohamedqadar280@gmail.com
- GitHub: https://github.com/Mohamed-Qadar

---
Built with Django 4.2 | Python 3.10+
