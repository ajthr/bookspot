from config.conftest import client

from config import db

from products.models import Product


class ProductTests:

    def test_database(self, client):

        # test add single data
        product = Product(
            isbn="test_single",
            title="test_single",
            author="test_single",
            publisher="test_single",
            msrp=1340,
            price=1199,
            genre="test_single"
        )
        db.Session.add(product)
        db.Session.commit()

        # test add multiple data
        products = [
            Product(
                isbn="test",
                title="test",
                author="test",
                publisher="test",
                msrp=1340,
                price=1199,
                genre="test"
            ),
            Product(
                isbn="test_1",
                title="test_1",
                author="test_1",
                publisher="test_1",
                msrp=1240,
                price=1099,
                genre="test_1"
            )
        ]
        db.Session.bulk_save_objects(products)
        db.Session.commit()

    def test_get_products(self, client):

        # add data to database
        products = [
            Product(
                isbn="test",
                title="test",
                author="test",
                publisher="test",
                msrp=1340,
                price=1199,
                genre="test"
            ),
            Product(
                isbn="test_1",
                title="test_1",
                author="test_1",
                publisher="test_1",
                msrp=1240,
                price=1099,
                genre="test_1"
            )
        ]
        db.Session.bulk_save_objects(products)
        db.Session.commit()

        # test get products
        resp = client.get('/books/')
        assert resp.status_code == 200

        # test get products with price low to high
        resp = client.get('/books/?sort_by=price_asc')
        assert resp.status_code == 200

        # test get products with price high to low
        resp = client.get('/books/?sort_by=price_desc')
        assert resp.status_code == 200

        # test get products added last
        resp = client.get('/books/?sort_by=latest')
        assert resp.status_code == 200

        # test get single data
        resp = client.get('/books/10000/')
        assert resp.status_code == 200

    def test_get_single_product(self, client):

        # add single product to database
        product = Product(
            isbn="test",
            title="test",
            author="test",
            publisher="test",
            msrp=1340,
            price=1199,
            genre="test"
        )
        db.Session.add(product)
        db.Session.commit()

        # test get single data
        resp = client.get('/books/10000/')
        assert resp.status_code == 200

        # test returned data contains correct data
        assert b'"isbn":"test"' in resp.data
        assert b'"author":"test"' in resp.data
        assert b'"publisher":"test"' in resp.data
        assert b'"msrp":1340' in resp.data
        assert b'"price":1199' in resp.data
        assert b'"genre":"test"' in resp.data

        # test populaity is increased on viewing
        product = db.Session.query(Product).filter(
            Product.id == 10000).first()

        # assert popularity increased by 1 after viewing book
        assert product.popularity == 1
