from marshmallow import Schema, fields

from products.serializers import ProductSchema

class OrderSchema(Schema):
    id = fields.String()
    customer = fields.String()
    address_id = fields.Integer(required=True)
    completed = fields.Boolean()
    amount = fields.Integer()

class OrderItemSchema(Schema):
    order_id = fields.Integer(required=True)
    product = fields.Nested(ProductSchema)
    quantity = fields.Integer()
