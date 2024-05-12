from flask import Blueprint, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import ViewSubmittedAssignmentsSchema, ViewGradedAssignmentsSchema
from core.apis.decorators import authenticate_principal
from core.models.teachers import Teacher
from ..teachers.schema import ViewTeachersSchema
from ..teachers.principal import (
    get_teachers,
    get_submitted_assignments,
    get_graded_assignments,
    regrade
)


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
# @authenticate_principal
def view_submitted_assignments(p):
    """Returns list of submitted assignments"""
    submitted_assignments = get_submitted_assignments()
    view_assignments = ViewSubmittedAssignmentsSchema(
        many=True).dump(submitted_assignments, many=True)
    return APIResponse.respond(data=view_assignments)


@principal_assignment_resources.route("/assignments/graded", methods=["GET"], strict_slashes=False)
@authenticate_principal
def view_graded_assignments(p):
    """Returns list of graded assignments"""
    graded_assignments = get_graded_assignments()
    view_assignments = ViewGradedAssignmentsSchema(
        many=True).dump(graded_assignments)
    return APIResponse.respond(data=view_assignments)


@principal_assignment_resources.route("/assignments/regrade/<id>", methods=["POST"], strict_slashes=False)
@authenticate_principal
def regrade_assignment(p, id):
    grade = request.args.get('grade')
    assignment = regrade(id, grade)
    regraded_assignment_dump = ViewGradedAssignmentsSchema(
        many=False).dump(assignment)
    return APIResponse.respond(data=regraded_assignment_dump)
