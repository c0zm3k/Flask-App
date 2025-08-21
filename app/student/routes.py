from flask import render_template, request, jsonify, session, redirect, url_for, flash
from . import student_bp
from ..utils.auth import login_required
from ..models.core import Student, Feedback, Teacher, College
from ..models import db
from datetime import datetime

@student_bp.route('/')
@login_required(role='student')
def dashboard():
    s = Student.query.get(session['user']['id'])
    return render_template('student/dashboard.html', student=s)

@student_bp.route('/verify', methods=['POST'])
def verify_student_id():
    sid = request.json.get('student_id')
    s = Student.query.filter_by(student_id=sid).first()
    if s:
        return jsonify({'valid': True, 'name': s.name, 'college': s.college.code, 'course': s.course, 'teacher_id': s.teacher_id})
    return jsonify({'valid': False}), 404

@student_bp.route('/feedback', methods=['POST'])
@login_required(role='student')
def submit_feedback():
    s = Student.query.get(session['user']['id'])
    text = request.form.get('feedback')
    if not text or len(text) < 5:
        flash('Feedback too short.', 'danger')
        return redirect(url_for('student.dashboard'))
    fb = Feedback(student_id=s.id, teacher_id=s.teacher_id, feedback_text=text, date=datetime.utcnow())
    db.session.add(fb); db.session.commit()
    flash('Feedback submitted. Thank you!', 'success')
    return redirect(url_for('student.dashboard'))
