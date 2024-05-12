from core.models.teachers import Teacher
from core.models.users import User
from core import db
from typing import List

def get_teachers():
    teachers_user_id = db.session.query(Teacher.user_id).all()
    # Flatten the list of tuples to a list of IDs
    teachers_user_id = [id for id, in teachers_user_id]
    teacher_in_users = db.session.query(User).filter(User.id.in_(teachers_user_id)).all()

    return teacher_in_users