from marshmallow import Schema, fields

class ProductSchema(Schema):
    id = fields.String()
    isbn = fields.String(required=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    publisher = fields.String(required=True)
    msrp = fields.Integer(required=True)
    price = fields.Integer(required=True)
    genre = fields.String(required=True)
    published = fields.Date()
    copies = fields.Integer(required=True)
    created = fields.Date()
