from flask import Blueprint, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema
from core.apis.decorators import authenticate_principal
from core.models.teachers import Teacher
from ..teachers.schema import ViewTeachersSchema
from ..teachers.principal import (
    get_teachers,
    get_assignments,
    regrade
)
from core.libs import assertions
from .schema import AssignmentSchema

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
@authenticate_principal
def view_submitted_assignments(p):
    """Returns list of submitted assignments"""
    submitted_assignments = get_assignments()
    graded_submitted_assignments = AssignmentSchema(
        many=True).dump(submitted_assignments, many=True)
    return APIResponse.respond(data=graded_submitted_assignments)


@principal_assignment_resources.route("/assignments/regrade", methods=["POST"], strict_slashes=False)
@authenticate_principal
@decorators.accept_payload
def regrade_assignment(payload, authenticated_principal):
    """Regrade an assignment"""

    assignment_id = payload.get('id')
    new_grade = payload.get('grade')

    regraded_assignment = regrade(assignment_id, new_grade)
    serialized_assignment = AssignmentSchema(
        many=False).dump(regraded_assignment)
    return APIResponse.respond(data=serialized_assignment)
