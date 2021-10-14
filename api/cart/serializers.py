from marshmallow import Schema, fields

from products.serializers import ProductSchema

class CartItemSchema(Schema):
    id = fields.Integer()
    customer = fields.String()
    product_id = fields.Integer()
    product = fields.Nested(ProductSchema)
    quantity = fields.Integer(required=True)
