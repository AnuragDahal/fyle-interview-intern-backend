import json
from flask import request
from core.libs import assertions
from functools import wraps
from core.models.users import User
from core.models.students import Student
from core.models.teachers import Teacher
from core.models.principals import Principal
from core import db


class AuthPrincipal:
    def __init__(self, user_id, student_id=None, teacher_id=None, principal_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.principal_id = principal_id


def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper


def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')
        p_dict = json.loads(p_str)
        p = AuthPrincipal(
            user_id=p_dict['user_id'],
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )
        # Retrieve the respective role id's from the database
        principal = db.session.query(Principal).filter(
            Principal.id == p.principal_id).scalar()
        student = db.session.query(Student).filter(
            Student.id == p.student_id).scalar()
        teacher = db.session.query(Teacher).filter(
            Teacher.id == p.teacher_id).first()

        # Check for the respective user id's in the database
        # principal_user_id = db.session.query(Principal.user_id).filter(
        #     Principal.user_id == p.user_id).scalar()
        # student_user_id = db.session.query(Student.user_id).filter(
        #     Student.user_id == p.user_id).scalar()
        # teacher_user_id = db.session.query(Teacher.user_id).filter(
        #     Teacher.user_id == p.user_id).scalar()

        if request.path.startswith('/principal'):
            assertions.assert_true(principal.id == p.principal_id and principal.user_id ==
                                   p.user_id, 'requester should be a principal or principal_id and user_id should be corresponding')
        elif request.path.startswith('/student'):
            assertions.assert_true(
                student.id == p.student_id and student.user_id == p.user_id, 'requester should be a student or student_id and user_id should be corresponding')
        elif request.path.startswith('/teacher'):
            assertions.assert_true(
                teacher.id == p.teacher_id and teacher.user_id == p.user_id, 'requester should be a teacher or teacher_id and user_id should be corresponding')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper
