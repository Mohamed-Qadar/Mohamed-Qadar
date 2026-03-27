# National Citizen Feedback & Smart Governance System

A comprehensive full-stack Django application designed to facilitate transparent communication between citizens and government institutions, enabling efficient complaint management, real-time tracking, and data-driven governance improvements.

## 🌟 Features

### For Citizens
- **Easy Complaint Submission**: Submit complaints with title, description, category, location, and optional images
- **Real-time Tracking**: Monitor complaint status (Pending → In Progress → Resolved)
- **Direct Communication**: Send messages directly to the presidency
- **Service Rating**: Rate government services and resolution quality
- **Transparency**: Full visibility into complaint handling process

### For Government Officials
- **Complaint Management**: View and manage complaints assigned to their institution
- **Status Updates**: Update complaint status and add responses
- **Response System**: Communicate with citizens about their complaints
- **Performance Tracking**: Monitor institution performance metrics

### For Presidency
- **National Overview**: Comprehensive dashboard with nationwide statistics
- **Analytics & Insights**: Performance metrics, trends, and data visualization
- **Institution Management**: Monitor and evaluate ministry performance
- **Complaint Assignment**: Assign complaints to appropriate institutions
- **Public Announcements**: Send announcements to all citizens
- **Direct Oversight**: Review all complaints and communications

### Smart AI Features
- **Auto-categorization**: AI-based complaint categorization
- **Priority Detection**: Automatic priority level assignment
- **Sentiment Analysis**: Analyze citizen sentiment in complaints
- **Performance Scoring**: Automated institution performance evaluation
- **Trend Analysis**: Identify trending issues and categories

## 🏗️ Project Structure

```
core/
├── core/                   # Main Django project settings
│   ├── settings.py        # Configuration
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI config
│   └── asgi.py           # ASGI config
├── users/                 # User management & authentication
│   ├── models.py         # User, UserProfile models
│   ├── views.py          # Registration, login, dashboards
│   ├── forms.py          # User forms
│   └── urls.py           # User URLs
├── complaints/            # Complaint management
│   ├── models.py         # Complaint, Response, Rating models
│   ├── views.py          # CRUD operations
│   ├── forms.py          # Complaint forms
│   └── urls.py           # Complaint URLs
├── institutions/          # Government institutions
│   ├── models.py         # Institution model
│   ├── views.py          # Institution views
│   └── urls.py           # Institution URLs
├── messaging/             # Communication system
│   ├── models.py         # Message, Announcement models
│   ├── views.py          # Messaging functionality
│   └── urls.py           # Messaging URLs
├── analytics/             # Analytics & AI
│   ├── models.py         # Performance metrics
│   ├── views.py          # Dashboard views
│   ├── ai_utils.py       # AI utilities
│   └── urls.py           # Analytics URLs
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Landing page
│   ├── users/            # User templates
│   ├── complaints/       # Complaint templates
│   └── messaging/        # Messaging templates
├── static/                # Static files
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript
└── manage.py              # Django management script
```

## 🎨 Design System

The application follows a modern, clean design with the following color scheme:

- **Primary Green**: `#12AD2B` - Success, positive actions
- **Secondary Red**: `#D40000` - Alerts, urgent items
- **Tertiary Blue**: `#0056B3` - Information, in-progress items
- **Neutral Dark**: `#1A1C1E` - Text, navigation

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Mohamed-Qadar/Mohamed-Qadar.git
cd Mohamed-Qadar/core
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database
Create a PostgreSQL database:
```sql
CREATE DATABASE citizen_feedback;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE citizen_feedback TO postgres;
```

Set environment variables (create `.env` file):
```env
DB_NAME=citizen_feedback
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Create Sample Institutions (Optional)
```bash
python manage.py shell
```
```python
from institutions.models import Institution

Institution.objects.create(
    name="Ministry of Health",
    institution_type="ministry",
    description="Responsible for health services nationwide"
)

Institution.objects.create(
    name="Ministry of Education",
    institution_type="ministry",
    description="Oversees education sector"
)

# Add more institutions as needed
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 👥 User Roles

### 1. Citizen
- Register with national ID, phone, location
- Submit and track complaints
- Send messages to presidency
- Rate resolved complaints

### 2. Government Official
- Assigned to specific institution
- Manage assigned complaints
- Update complaint status
- Respond to citizens

### 3. Presidency
- Full system access
- View all complaints nationwide
- Access analytics dashboards
- Assign complaints to institutions
- Send public announcements

## 📊 AI & Analytics

### AI Features Implementation
The system includes basic AI utilities with room for advanced ML integration:

1. **Categorization**: Rule-based + ML-ready architecture
2. **Priority Detection**: Keyword + sentiment analysis
3. **Performance Scoring**: Multi-factor evaluation
4. **Trend Analysis**: Time-series and clustering

### Extending AI Capabilities
To add advanced AI features:

```python
# Uncomment in requirements.txt:
# transformers==4.35.2
# torch==2.1.1

# Then use in analytics/ai_utils.py:
from transformers import pipeline

classifier = pipeline("text-classification", model="bert-base-uncased")
result = classifier(complaint_text)
```

## 🔒 Security Features

- CSRF protection enabled
- Password hashing with Django's default backend
- User authentication and authorization
- Role-based access control
- SQL injection prevention through ORM
- XSS protection via template escaping

### Production Security (Uncomment in settings.py)
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

## 🌐 Deployment

### Using Gunicorn + Nginx

1. **Collect Static Files**:
```bash
python manage.py collectstatic
```

2. **Run with Gunicorn**:
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

3. **Configure Nginx** (example):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📝 API Endpoints

Main URL patterns:

- `/` - Home page
- `/register/citizen/` - Citizen registration
- `/register/government/` - Government registration
- `/login/` - User login
- `/dashboard/` - Role-based dashboard
- `/complaints/` - Complaint list
- `/complaints/create/` - Submit complaint
- `/complaints/<id>/` - Complaint details
- `/messaging/` - Messages
- `/analytics/` - Analytics dashboard (presidency only)
- `/institutions/` - Institution list
- `/admin/` - Django admin panel

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

## 📄 License

This project is open source and available for educational and governmental use.

## 👨‍💻 Developer

**Mohamed Ibrahim Abdi**
- Email: mohamedqadar280@gmail.com
- LinkedIn: [mohamed-ibrahim-abdi](https://tr.linkedin.com/in/mohamed-ibrahim-abdi-572475232)
- GitHub: [@Mohamed-Qadar](https://github.com/Mohamed-Qadar)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support, please contact:
- Email: mohamedqadar280@gmail.com
- Open an issue on GitHub

## 🎯 Future Enhancements

- [ ] Mobile application (React Native/Flutter)
- [ ] Real-time notifications (WebSockets)
- [ ] Advanced ML models for categorization
- [ ] Geolocation mapping for complaints
- [ ] Multi-language support
- [ ] Email notification system
- [ ] SMS integration
- [ ] RESTful API for third-party integration
- [ ] Advanced reporting and export features
- [ ] Chat system for real-time communication

---

**Built with Django | Empowering Citizens, Improving Governance**
