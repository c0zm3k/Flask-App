from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from .emailing.mailer import init_mail
from .models import db
from .utils.filters import register_filters

mail = Mail()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.DevConfig")

    db.init_app(app)
    Migrate(app, db)
    mail.init_app(app)
    init_mail(mail)

    # Blueprints
    from .admin.routes import admin_bp
    from .teacher.routes import teacher_bp
    from .student.routes import student_bp
    from .auth.routes import auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(teacher_bp, url_prefix="/teacher")
    app.register_blueprint(student_bp, url_prefix="/student")

    # Jinja filters
    register_filters(app)

    # Create tables (dev only)
    with app.app_context():
        db.create_all()

    return app
