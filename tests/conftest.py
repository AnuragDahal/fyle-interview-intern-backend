import pytest
import json
from tests import app
from core import db
from core.models.assignments import Assignment

# !part of the fixture import that I was unable to make it work 
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session

# # setup the engine and sessionmaker
# engine = create_engine('sqlite:///core/store.sqlite3')
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers


@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers


@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers


@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }

    return headers


@pytest.fixture
def reset_assignment_state():
    assignment = db.session.query(Assignment).filter(
        Assignment.id == 2).first()
    if assignment:
        assignment.state = 'DRAFT'
        db.session.commit()
        db.session.refresh(assignment)


#! This is the fixture that I was unable to make it work
# @pytest.fixture
# def db_session():
#     # create a new session
#     session = SessionLocal()

#     yield session  # this is where the testing happens

#     # rollback any changes after the test
#     session.rollback()
#     session.close()
