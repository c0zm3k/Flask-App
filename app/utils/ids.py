from datetime import datetime
from ..models.core import Student
from ..models import db

COURSE_CODES = {'AI','CS','CC','DA','CB'}

def generate_student_id(college_code:str, course_code:str)->str:
    year_prefix = str(datetime.now().year % 100).zfill(2)
    if course_code not in COURSE_CODES:
        raise ValueError('Invalid course code')
    base = f"{year_prefix}{college_code}{course_code}"
    # find last roll for this college+course+year
    like_pattern = base + '%'
    last_student = (Student.query
                    .filter(Student.student_id.like(like_pattern))
                    .order_by(Student.student_id.desc())
                    .first())
    last_roll = int(last_student.student_id[-3:]) if last_student else 0
    next_roll = str(last_roll + 1).zfill(3)
    return base + next_roll

def generate_institution_id(name:str)->str:
    prefix = ''.join([c for c in name.upper() if c.isalnum()])[:4]
    ts = datetime.now().strftime('%y%m%d%H%M%S')
    return f"{prefix}-{ts}"
