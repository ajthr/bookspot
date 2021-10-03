from flask import request, make_response as response, jsonify

from config import db
from config.base import BaseView

from products.models import Product
from products.serializers import ProductSchema


class ProductsAPIView(BaseView):

    def get(self):
        try:
            sort = request.args.get('sort')
            page = request.args.get('page')
            limit = 10
            offset = int(page) * 10 if page else 0

            if sort == 'price_desc':
                products = db.Session.query(Product).order_by(
                    Product.price.desc()).limit(limit).offset(offset)
            elif sort == 'price_asc':
                products = db.Session.query(Product).order_by(
                    Product.price.asc()).limit(limit).offset(offset)
            elif sort == 'latest':
                products = db.Session.query(Product).order_by(
                    Product.published.desc()).limit(limit).offset(offset)
            else:
                products = db.Session.query(Product).order_by(
                    Product.popularity.desc()).limit(limit).offset(offset)

            schema = ProductSchema(many=True)
            data = schema.dump(products)
            return response(jsonify(data), 200)
        except:  # catch database and serialization errors
            return response("", 500)


class ProductAPIView(BaseView):

    def get(self, id):
        try:
            product = db.Session.query(Product).filter(
                Product.id == id).first()
            if product is not None:
                # increase popularity by after viewing
                product.popularity += 1
                db.Session.commit()
                
                schema = ProductSchema()
                data = schema.dump(product)
                return response(jsonify(data, 200))
            return response("", 404)
        except:  # catch database and serialization errors
            return response("", 500)
