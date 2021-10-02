from marshmallow import Schema, fields


class CustomerSchema(Schema):
    name = fields.String()
    email = fields.String(required=True)
    joined = fields.Date()


class AddressSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    address = fields.String(required=True)
    locality = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    mobile = fields.String(required=True)
    pincode = fields.String(required=True)
    office = fields.Boolean()
    default = fields.Boolean()
