import csv
from datetime import datetime
from flask import current_app
from ..models.core import Feedback, Student

def export_feedback_csv(teacher_id:int, date_str:str, path:str)->str:
    # date_str expected in YYYY-MM-DD
    dt = datetime.strptime(date_str, '%Y-%m-%d').date()
    q = Feedback.query.filter(
        Feedback.teacher_id==teacher_id,
        Feedback.date.between(datetime.combine(dt, datetime.min.time()),
                              datetime.combine(dt, datetime.max.time()))
    ).all()
    filename = path
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['StudentID','StudentName','TeacherID','Feedback','Date'])
        for fb in q:
            student = Student.query.get(fb.student_id)
            writer.writerow([student.student_id, student.name, fb.teacher_id, fb.feedback_text, fb.date.isoformat()])
    return filename
