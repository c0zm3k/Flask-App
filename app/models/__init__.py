from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .core import Admin, College, Teacher, Student, Feedback, teacher_college  # noqa: F401
