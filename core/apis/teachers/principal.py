from core.models.teachers import Teacher
from core.models.users import User
from core import db
from typing import List
from core.models.assignments import Assignment


def get_teachers():
    teachers_user_id = db.session.query(Teacher.user_id).all()
    # Flatten the list of tuples to a list of IDs
    teachers_user_id = [id for id, in teachers_user_id]
    teacher_in_users = db.session.query(User).filter(
        User.id.in_(teachers_user_id)).all()

    return teacher_in_users


def get_submitted_assignments():

    submitted_assignments = db.session.query(Assignment).filter(
        Assignment.state == 'SUBMITTED').all()
    return submitted_assignments


def get_graded_assignments():
    graded_assignments = db.session.query(Assignment).filter(
        Assignment.state == 'GRADED').all()
    return graded_assignments

def regrade(id, grade):
    db.session.query(Assignment).filter(
        Assignment.id == id).update({Assignment.grade: grade}, synchronize_session=False)
    db.session.commit()
    regraded_assignment = db.session.query(Assignment).filter(Assignment.id == id).first()
    return regraded_assignment