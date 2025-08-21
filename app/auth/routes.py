from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from ..models.core import Admin, Teacher, Student
from ..models import db
from ..utils.auth import set_user, clear_user
from ..emailing.mailer import send_mail

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/login')
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
        db.session.add(admin); db.session.commit()
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

# Teacher password reset (email)
@auth_bp.route('/teacher/reset', methods=['GET','POST'])
def teacher_reset():
    if request.method == 'POST':
        email = request.form['email']
        teacher = Teacher.query.filter_by(email=email).first()
        if teacher:
            # In real app, generate token link
            new_pass = 'Temp1234!'
            teacher.set_password(new_pass); db.session.commit()
            send_mail('Password Reset', [email], f'Your temporary password: {new_pass}')
            flash('Temporary password sent to your email.', 'success')
            return redirect(url_for('auth.teacher_login'))
        flash('Email not found.', 'danger')
    return render_template('auth/teacher_reset.html')

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
