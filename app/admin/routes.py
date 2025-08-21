from flask import render_template, request, redirect, url_for, flash
from . import admin_bp
from ..utils.auth import login_required
from ..models.core import Admin, Teacher, College
from ..models import db
from ..emailing.mailer import send_mail

@admin_bp.route('/')
@login_required(role='admin')
def dashboard():
    teachers = Teacher.query.all()
    colleges = College.query.all()
    return render_template('admin/dashboard.html', teachers=teachers, colleges=colleges)

@admin_bp.route('/colleges', methods=['POST'])
@login_required(role='admin')
def add_college():
    name = request.form['name']
    code = request.form['code']
    if College.query.filter_by(code=code).first():
        flash('College code already exists.', 'danger')
        return redirect(url_for('admin.dashboard'))
    db.session.add(College(name=name, code=code)); db.session.commit()
    flash('College added.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/teachers', methods=['POST'])
@login_required(role='admin')
def add_teacher():
    name = request.form['name']; email = request.form['email']; phone = request.form['phone']
    username = request.form['username']; password = request.form['password']
    t = Teacher(name=name,email=email,phone=phone,username=username)
    t.set_password(password)
    db.session.add(t); db.session.commit()
    flash('Teacher added.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/teachers/<int:teacher_id>/assign', methods=['POST'])
@login_required(role='admin')
def assign_colleges(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    codes = request.form.getlist('college_codes')
    colleges = College.query.filter(College.code.in_(codes)).all()
    teacher.colleges = colleges
    db.session.commit()
    flash('Colleges assigned.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/teachers/<int:teacher_id>/reset', methods=['POST'])
@login_required(role='admin')
def reset_teacher_password(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    new_pass = 'Temp1234!'
    teacher.set_password(new_pass); db.session.commit()
    send_mail('Password Reset', [teacher.email], f'Your temporary password: {new_pass}')
    flash('Teacher password reset and emailed.', 'success')
    return redirect(url_for('admin.dashboard'))
