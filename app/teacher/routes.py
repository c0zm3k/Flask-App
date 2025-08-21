from flask import render_template, request, redirect, url_for, flash, send_file, session
from . import teacher_bp
from ..utils.auth import login_required
from ..utils.ids import generate_student_id
from ..utils.export import export_feedback_csv
from ..models.core import Teacher, Student, College, Feedback
from ..models import db
from datetime import datetime
import os

@teacher_bp.route('/')
@login_required(role='teacher')
def dashboard():
    user = session.get('user')
    teacher = Teacher.query.get(user['id'])
    # Only students in allocated colleges
    college_ids = [c.id for c in teacher.colleges]
    students = Student.query.filter(Student.college_id.in_(college_ids)).all()
    return render_template('teacher/dashboard.html', teacher=teacher, students=students)

@teacher_bp.route('/students', methods=['POST'])
@login_required(role='teacher')
def add_student():
    name = request.form['name']
    college_code = request.form['college_code']
    course = request.form['course']
    college = College.query.filter_by(code=college_code).first()
    if not college:
        flash('Invalid college code.', 'danger')
        return redirect(url_for('teacher.dashboard'))
    student_id = generate_student_id(college_code, course)
    student = Student(student_id=student_id, name=name, college_id=college.id, course=course, teacher_id=session['user']['id'])
    db.session.add(student); db.session.commit()
    flash(f'Student added with ID {student_id}', 'success')
    return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/students/<int:student_id>/delete', methods=['POST'])
@login_required(role='teacher')
def delete_student(student_id):
    s = Student.query.get_or_404(student_id)
    # ensure ownership via allocated colleges
    teacher = Teacher.query.get(session['user']['id'])
    if s.college not in teacher.colleges:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('teacher.dashboard'))
    db.session.delete(s); db.session.commit()
    flash('Student deleted.', 'success')
    return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/export')
@login_required(role='teacher')
def export():
    date = request.args.get('date') or datetime.utcnow().strftime('%Y-%m-%d')
    filepath = os.path.join('/mnt/data', f'feedback_{session["user"]["id"]}_{date}.csv')
    export_feedback_csv(session['user']['id'], date, filepath)
    return send_file(filepath, as_attachment=True, download_name=os.path.basename(filepath))
