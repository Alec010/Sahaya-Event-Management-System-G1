# Sahaya - Event Management System

Sahaya is a comprehensive event management platform designed to streamline the process of creating, managing, and participating in events. Built with Django, this system provides a robust set of tools for event organizers and participants.

![Sahaya Logo](sahaya/sahayamainlogo.png)

## Features

### EMS-01: Event Creation
- **Intuitive Forms**: User-friendly interfaces for creating and updating events
- **Secure Database**: Robust storage of all event-related data
- **Event APIs**: Backend APIs for event submission and updates

### EMS-02: Event Management
- **Organizer Dashboard**: Centralized control panel for monitoring and managing events
- **Participant Integration**: Seamless connection between participant data and events
- **Email Notifications**: Automated emails for registrations, updates, and reminders
- **Event Calendar**: Interactive calendar for visualizing and organizing event schedules

### EMS-03: Participant Registration and Tracking
- **Seamless Registration**: Streamlined process for student registration
- **Participant Database**: Comprehensive storage of participant information
- **Participant Dashboard**: Tools for organizers to monitor and update participation
- **CRUD Operations**: Full functionality to add, update, and delete participant records

### EMS-04: Basic Reporting
- **Report Generation**: Create and download attendance and performance reports in PDF format
- **Reporting Interface**: Simple UI for selecting report parameters and generating outputs

### EMS-05: User Management
- **Secure Profiles**: Tools for users to create and manage their profiles
- **Efficient Database**: Optimized storage and retrieval of user data
- **Role Management**: Functionality for account role updates, profile picture uploads, and account deletion

### EMS-06: Discover More Events
- **Event Discovery**: Platform to showcase external events with search and filter capabilities
- **User Submissions**: Allow users to add, update, and delete external event entries
- **External Links**: Redirection to external websites for detailed information or registration

## Technology Stack

- **Backend**: Django 5.1.x
- **Database**: SQLite (development)
- **Frontend**: HTML/CSS with Django templates
- **Media Handling**: Django's built-in media handling with Pillow
- **PDF Generation**: WeasyPrint
- **Email**: SMTP configuration

## Installation and Setup

### Prerequisites

- Python 3.10+ 
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/sahaya.git
cd sahaya
```

### Step 2: Create a Virtual Environment

```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# macOS/Linux
python -m venv myenv
source myenv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available, install the following packages:

```bash
pip install django pillow weasyprint
```

### Step 4: Configure Database

```bash
cd sahaya
python manage.py migrate
```

### Step 5: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Project Structure

```
sahaya/
├── discover/             # Event discovery app
├── event/                # Core event management app
├── media/                # User-uploaded files
├── notification/         # Email and notification system
├── registration/         # Participant registration app
├── report/               # Reporting functionality
├── sahaya/               # Project configuration
├── users/                # User management app
└── manage.py             # Django management script
```

## Usage Guide

### For Administrators

1. Access the admin panel at `/admin` using your superuser credentials
2. Manage users, events, and system settings

### For Event Organizers

1. Create an account or log in
2. Navigate to the dashboard to create and manage events
3. Monitor registrations and participant data
4. Generate reports for completed events

### For Participants

1. Create an account or log in
2. Browse available events on the dashboard or discover page
3. Register for events of interest
4. View your registered events in your personal dashboard

## Email Configuration

The system is configured to send emails for notifications. Update the email settings in `settings.py` with your SMTP credentials:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
```

## Development

### Creating New Apps

```bash
python manage.py startapp app_name
```

Don't forget to add the new app to INSTALLED_APPS in settings.py.

### Running Tests

```bash
python manage.py test
```

### Making Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure a production-ready database (PostgreSQL recommended)
3. Set up static file serving with a web server (Nginx/Apache)
4. Use WSGI server like Gunicorn or uWSGI

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django framework and community
- All contributors to the project

---

Developed for Cebu Institute of Technology - University, September 2024
