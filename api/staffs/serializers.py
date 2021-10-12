from marshmallow import Schema, fields

class StaffSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    name = fields.String()
    is_admin = fields.Boolean()
    joined = fields.Date()
