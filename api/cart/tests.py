from config import db
from config.utils import totp
from config.conftest import client

from products.models import Product


def create_products():
    products = [
        Product(
            isbn="test",
            title="test",
            author="test",
            publisher="test",
            msrp=1340,
            price=1199,
            copies=10,
            genre="test"
        ),
        Product(
            isbn="test_1",
            title="test_1",
            author="test_1",
            publisher="test_1",
            msrp=1240,
            price=1099,
            copies=10,
            genre="test_1"
        )
    ]
    db.Session.bulk_save_objects(products)
    db.Session.commit()


class CartTests:

    def test_post_cart_items(self, client):

        create_products()

        otp = totp.now()  # create a dummy otp token
        resp = client.post('/email_signin/', json={
            'email': 'test123@test.com',
            'otp': otp
        })
        assert resp.status_code == 200

        resp = client.post('/cart/', json={
            "product_id": 10000,
            "quantity": 2
        })

        assert resp.status_code == 200

    def test_get_cart_items(self, client):
        create_products()

        otp = totp.now()  # create a dummy otp token
        resp = client.post('/email_signin/', json={
            'email': 'test123@test.com',
            'otp': otp
        })
        assert resp.status_code == 200

        resp = client.post('/cart/', json={
            "product_id": 10000,
            "quantity": 2
        })
        assert resp.status_code == 200

        resp = client.post('/cart/', json={
            "product_id": 10001,
            "quantity": 3
        })
        assert resp.status_code == 200

        resp = client.get('/cart/')
        assert resp.status_code == 200
        
        assert b'"product_id\\": 10000' in resp.data
        assert b'"product_id\\": 10001' in resp.data

        resp = client.post('/cart/', json={
            "product_id": 10000,
            "quantity": 0
        })

        resp = client.post('/cart/', json={
            "product_id": 10001,
            "quantity": 5
        })
        assert resp.status_code == 200

        resp = client.get('/cart/')
        assert resp.status_code == 200

        assert b'"product_id\\": 10000' not in resp.data
        assert b'"product_id\\": 10001' in resp.data
        assert b'"quantity\\": 5' in resp.data
