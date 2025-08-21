# Student Feedback Management System (Flask)

Multi-role Student Feedback Management System with Admin, Teacher, and Student portals.
Mobile-first, minimal UI using a custom blue palette.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app wsgi.py db upgrade

# Option 1: Run the application with mail server in a separate terminal
python start_mail_server.py
flask --app wsgi.py run

# Option 2: Run the application with automatic mail server startup
SET START_MAIL_SERVER=true  # Linux/Mac: export START_MAIL_SERVER=true
flask --app wsgi.py run
```

### Environment variables (development)
Create a `.env` or export these before running:

```
FLASK_ENV=development
SECRET_KEY=change-this
MAIL_SERVER=localhost
MAIL_PORT=1025
MAIL_DEFAULT_SENDER=noreply@example.com
# For real SMTP, provide MAIL_USERNAME / MAIL_PASSWORD / MAIL_USE_TLS or SSL
```

> Tip: In dev, run a debug smtp server to see emails in console:
> 
> **Option 1:** Use the provided script (recommended):
> ```
> python start_mail_server.py
> ```
> This script automatically detects your Python version and starts the appropriate mail server.
> 
> **Option 2:** Run manually:
> 
> For Python 3.11 and earlier:
> ```
> python -m smtpd -c DebuggingServer -n localhost:1025
> ```
> 
> For Python 3.12 and later (smtpd is deprecated):
> ```
> pip install aiosmtpd
> aiosmtpd -n -l localhost:1025
> ```

## Roles

- **Admin**: manages teachers, assigns colleges, resets passwords
- **Teacher**: manages students, exports daily feedback
- **Student**: logs in with Student ID and submits feedback

## Tech
- Flask, SQLAlchemy, Alembic (Flask-Migrate)
- Jinja2 templates
- Flask-Mail (email stubs for dev)
- SQLite (default), easy PG migration

## Structure
```
student_feedback_system/
  app/
    admin/         # admin blueprint
    teacher/       # teacher blueprint
    student/       # student blueprint
    auth/          # auth blueprint
    models/        # SQLAlchemy models
    utils/         # helpers (auth decorators, id generation, export)
    emailing/      # email helper
    templates/     # base templates
    static/        # css/js assets
  config.py
  wsgi.py
  requirements.txt
  README.md
```
