from marshmallow import Schema, EXCLUDE, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, SQLAlchemySchema
from marshmallow_enum import EnumField
from core.models.assignments import Assignment, GradeEnum
from core.libs.helpers import GeneralObject
from core.models.teachers import Teacher
from core.models.users import User


class ViewTeachersSchema(SQLAlchemySchema):
    class Meta:
        model = User
        unknown = EXCLUDE

    id = auto_field()
    username = auto_field()
    email = auto_field()
