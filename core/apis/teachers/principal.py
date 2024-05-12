from core.models.teachers import Teacher
from core.models.users import User
from core import db
from typing import List
from core.models.assignments import Assignment
from core.libs import assertions
from sqlalchemy.sql import or_


def get_teachers():
    teachers_user_id = db.session.query(Teacher.user_id).all()
    # Flatten the list of tuples to a list of IDs
    teachers_user_id = [id for id, in teachers_user_id]
    teacher_in_users = db.session.query(User).filter(
        User.id.in_(teachers_user_id)).all()

    return teacher_in_users


def get_assignments():
    submitted_and_graded_assignments = db.session.query(Assignment).filter(
        or_(Assignment.state == 'SUBMITTED', Assignment.state == "GRADED")).all()
    return submitted_and_graded_assignments


def regrade(id, grade):
    # Check if id exists in the database
    assignment = db.session.query(Assignment).filter(
        Assignment.id == id).first()
    if assignment is None:
        assertions.assert_found(
            assignment, 'No assignment with this id was found')
    if grade not in ["A", "B", "C", "D"]:
        assertions.assert_unprocessable(
            False, 'Grade must be one of A, B, C, D')

    try:
        db.session.query(Assignment).filter(
            Assignment.id == id).update({Assignment.grade: grade, Assignment.state: "GRADED"}, synchronize_session=False)
        db.session.commit()
        regraded_assignment = db.session.query(
            Assignment).filter(Assignment.id == id).first()
        return regraded_assignment
    except Exception as e:
        db.session.rollback()
        raise e
