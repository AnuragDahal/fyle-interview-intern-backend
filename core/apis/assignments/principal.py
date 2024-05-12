from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.apis.decorators import authenticate_principal
from core.models.teachers import Teacher
from ..teachers.schema import ViewTeachersSchema
from ..teachers.principal import get_teachers


principal_assignment_resources = Blueprint(
    "principal_assignment_resources", __name__)


@principal_assignment_resources.route('/teacher', methods=['GET'], strict_slashes=False)
@authenticate_principal
def view_teachers(p):
    """Returns list of teachers"""
    teachers = get_teachers()
    schema = ViewTeachersSchema(many=True)
    teachers_dump = schema.dump(teachers)
    return APIResponse.respond(data=teachers_dump)


@principal_assignment_resources.route("/assignments/submitted", methods=["GET"], strict_slashes=False)
def view_submitted_assignments():
    """Returns list of submitted assignments"""
    submitted_assignments = Assignment.get_submitted_assignments()
    return APIResponse.respond(data=submitted_assignments)


@principal_assignment_resources.route("/assignments/graded", methods=["GET"], strict_slashes=False)
def view_graded_assignments():
    """Returns list of graded assignments"""
    graded_assignments = Assignment.get_graded_assignments()
    return APIResponse.respond(data=graded_assignments)


@principal_assignment_resources.route("/assignments/regrade", methods=["POST"], strict_slashes=False)
def regrade_assignment():
    pass
