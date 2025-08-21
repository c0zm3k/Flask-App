from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from ..models.core import Admin, Teacher, Student, PasswordReset
from ..models import db
from sqlalchemy.exc import IntegrityError
from ..utils.auth import set_user, clear_user
from ..emailing.mailer import send_mail
from datetime import datetime, timedelta
import secrets

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/login')
@auth_bp.route('/login_select')
def login_select():
    return render_template('auth/login_select.html')

@auth_bp.route('/logout')
def logout():
    clear_user()
    flash('Logged out.', 'success')
    return redirect(url_for('auth.login_select'))

# --- Admin signup & login ---
@auth_bp.route('/admin/signup', methods=['GET','POST'])
def admin_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        from ..utils.ids import generate_institution_id
        inst_id = generate_institution_id(name)
        admin = Admin(institution_id=inst_id, name=name, email=email, phone=phone, username=username)
        admin.set_password(password)
        try:
            db.session.add(admin)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Email or username already exists. Please use different credentials.', 'danger')
            return redirect(url_for('auth.admin_signup'))
        except Exception as e:
            db.session.rollback()
            flash('Could not create account. Please try again.', 'danger')
            return redirect(url_for('auth.admin_signup'))
        send_mail('Your Institution ID', [email], f'Hello {name}, your Institution ID is: {inst_id}')
        flash('Signup successful. Check your email for Institution ID.', 'success')
        return redirect(url_for('auth.admin_login'))
    return render_template('auth/admin_signup.html')

@auth_bp.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        inst_id = request.form['institution_id']
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(institution_id=inst_id, username=username).first()
        if admin and admin.check_password(password):
            set_user('admin', admin.id, username)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('auth/admin_login.html')

# --- Teacher login ---
@auth_bp.route('/teacher/login', methods=['GET','POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        teacher = Teacher.query.filter_by(username=username).first()
        if teacher and teacher.check_password(password):
            set_user('teacher', teacher.id, username)
            return redirect(url_for('teacher.dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('auth/teacher_login.html')

# Teacher password reset (redirects to unified flow)
@auth_bp.route('/teacher/reset', methods=['GET','POST'])
def teacher_reset():
    return redirect(url_for('auth.password_reset_request', role='teacher'))

# Unified password reset: request link
@auth_bp.route('/reset/request', methods=['GET', 'POST'])
def password_reset_request():
    role = request.args.get('role', 'teacher')
    if request.method == 'POST':
        role = request.form.get('role') or role
        email = request.form['email']
        # Look up user silently
        user_exists = bool(Admin.query.filter_by(email=email).first()) if role == 'admin' else bool(Teacher.query.filter_by(email=email).first())
        if user_exists:
            token = secrets.token_urlsafe(32)
            reset = PasswordReset(role=role, email=email, token=token, expires_at=datetime.utcnow() + timedelta(hours=1))
            db.session.add(reset); db.session.commit()
            link = url_for('auth.password_reset', token=token, _external=True)
            send_mail('Password Reset Request', [email], f'Click this link to reset your password: {link}\nThis link expires in 1 hour.')
        flash('If the email exists, a reset link has been sent.', 'info')
        return redirect(url_for('auth.login_select'))
    return render_template('auth/password_reset_request.html', role=role)

# Unified password reset: set new password
@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    pr = PasswordReset.query.filter_by(token=token, used=False).first()
    if not pr or pr.expires_at < datetime.utcnow():
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('auth.login_select'))
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.password_reset', token=token))
        user = Admin.query.filter_by(email=pr.email).first() if pr.role == 'admin' else Teacher.query.filter_by(email=pr.email).first()
        if not user:
            flash('Account not found.', 'danger')
            return redirect(url_for('auth.login_select'))
        user.set_password(password)
        pr.used = True
        db.session.commit()
        flash('Password has been reset. You can log in now.', 'success')
        return redirect(url_for('auth.login_select'))
    return render_template('auth/password_reset.html')

# --- Student login ---
@auth_bp.route('/student/login', methods=['GET','POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form['student_id']
        student = Student.query.filter_by(student_id=student_id).first()
        if student:
            set_user('student', student.id, student.student_id)
            return redirect(url_for('student.dashboard'))
        flash('Invalid Student ID.', 'danger')
    return render_template('auth/student_login.html')

@auth_bp.route('/student/feedback')  
def student_feedback_link():
    return render_template('auth/student_feedback.html')
