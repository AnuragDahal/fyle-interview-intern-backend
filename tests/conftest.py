import pytest
import json
from tests import app
from core import db
from core.models.assignments import Assignment
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from core import db

# Setup a test database


@pytest.fixture(scope='module')
def test_db():
    # Use an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    db.Model.metadata.create_all(engine)  # Create the tables
    session = scoped_session(sessionmaker(bind=engine))  # Create a new session
    db.session = session  # Assign the session to your db session
    yield  # This is where the testing happens
    session.remove()  # After testing, remove the session
    db.Model.metadata.drop_all(engine)  # Drop the tables


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
def h_teacher_3():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 3,
            'user_id': 6
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


@pytest.fixture
def reset_assignment_state_2(*args, **kwargs):
    def reset_to_submitted(id, state):
        assignment = db.session.query(Assignment).filter(
            Assignment.id == id).first()
        if assignment:
            assignment.state = state
            assignment.grade = None
            db.session.commit()
            db.session.refresh(assignment)
    return reset_to_submitted


@pytest.fixture
def remove_from_db(*args, **kwargs):
    def remove_assignment(id):
        assignment = db.session.query(Assignment).filter(
            Assignment.id == id).first()
        if assignment:
            db.session.delete(assignment)
            db.session.commit()
    return remove_assignment


@pytest.fixture
def remove_assignments_from_id(*args, **kwargs):
    def remove_assignments(start_id):
        assignments = db.session.query(Assignment).filter(
            Assignment.id >= start_id).all()
        for assignment in assignments:
            db.session.delete(assignment)
        db.session.commit()
    return remove_assignments



    #!This is the fixture that I was unable to make it work
    # @pytest.fixture
    # def db_session():
    #     # create a new session
    #     session = SessionLocal()

    #     yield session  # this is where the testing happens

    #     # rollback any changes after the test
    #     session.rollback()
    # session.close()
