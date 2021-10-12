import bcrypt
from werkzeug.http import parse_cookie

from config.conftest import client
from config import db

from staffs.models import Staff


def create_staff(username="staff", name="staff_name", admin=False):
    password = bcrypt.hashpw("supersecret", bcrypt.gensalt())
    staff = Staff(username=username, name=name,
                  password=password, is_admin=admin)
    db.Session.add(staff)
    db.Session.commit()


class StaffTests:

    def test_staff_permissions(self, client):

        # test without logging in
        resp = client.post('/staff/create/', json={
            "username": "name",
            "name": "name",
            "password": "password"
        })

        assert resp.status_code == 401

        # test as non admin
        create_staff()
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })

        resp = client.post('/staff/create/', json={
            "username": "name",
            "name": "name",
            "password": "password"
        })

        assert resp.status_code == 401

    def test_create_staff(self, client):

        # test create staff without authorization
        resp = client.post('/staff/create/')
        assert resp.status_code == 401

        # test create staff not as admin
        create_staff()
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        resp = client.post('/staff/create/')
        assert resp.status_code == 401

        # logout from staff
        resp = client.post('/staff/logout/')
        assert resp.status_code == 200

        # login as admin
        create_staff(username="admin", admin=True)
        resp = client.post('/staff/login/', json={
            "username": "admin",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        # test create staff with incomplete request body
        resp = client.post('/staff/create/', json={
            "username": "username",
        })
        assert resp.status_code == 400

        # test create staff with wrong request body
        resp = client.post('/staff/create/', json={
            "email": "username",
            "name": "name",
            "password": "password"
        })
        assert resp.status_code == 400

        # test create staff without request body
        resp = client.post('/staff/create/')
        assert resp.status_code == 400

        # test create staff
        resp = client.post('/staff/create/', json={
            "username": "username",
            "name": "name",
            "password": "password"
        })
        assert resp.status_code == 200

    def test_login_staff(self, client):
        # test login with without request body
        resp = client.post('/staff/login/')
        assert resp.status_code == 400

        # test login with incomplete request body
        resp = client.post('/staff/login/', json={
            "username": "staff",
        })
        assert resp.status_code == 400

        # test login with wrong request body
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "wrong": "wrong"
        })
        assert resp.status_code == 400

        # test login with non existing account
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 401

        create_staff()

        # test with wrong password
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecretbutwrong"
        })
        assert resp.status_code == 403

        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        # test if cookie is being set
        cookies = resp.headers.getlist('Set-Cookie')
        cookie = next(
            (cookie for cookie in cookies if '__STSSID_' in cookie), None)
        assert cookie is not None

        # test if cookie attributes are correct
        cookie_attrs = parse_cookie(cookie)
        assert 'Secure' in cookie_attrs
        assert 'HttpOnly' in cookie_attrs
        assert cookie_attrs['SameSite'] == 'Strict'

    def test_staff_details(self, client):
        create_staff()

        # test get data without authorization
        resp = client.get('/staff/')
        assert resp.status_code == 401

        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        # test get staff data
        resp = client.get('/staff/')
        assert resp.status_code == 200

        assert b'"name":"staff_name"' in resp.data
        assert b'"username":"staff"' in resp.data
        assert b'"is_admin":false' in resp.data
        assert b'"joined":' in resp.data
        assert b'"password:"' not in resp.data

    def test_staff_update(self, client):

        # test update data without authorization
        resp = client.patch('/staff/')
        assert resp.status_code == 401

        create_staff()
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        # test get data without request body
        resp = client.patch('/staff/')
        assert resp.status_code == 400

        # test get data with wrong request body
        resp = client.patch('/staff/', json={
            "username": "name"
        })
        assert resp.status_code == 400

        # test name is correct
        resp = client.get('/staff/')
        assert resp.status_code == 200

        assert b'"name":"staff_name"' in resp.data

        resp = client.patch('/staff/', json={
            "name": "new_staff_name"
        })

        resp = client.get('/staff/')
        assert resp.status_code == 200

        assert b'"name":"staff_name"' not in resp.data
        assert b'"name":"new_staff_name"' in resp.data

    def test_staff_logout(self, client):

        # test cannot logout without logging in
        resp = client.post('/staff/logout/')
        assert resp.status_code == 401

        create_staff()
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        # test logout
        resp = client.post('/staff/logout/')
        assert resp.status_code == 200

        # test authorized routes are being rejected after login
        resp = client.get('/staff/')
        assert resp.status_code == 401

    def test_staff_change_password(self, client):

        # test change password without authorization
        resp = client.post('/staff/change_password/')
        assert resp.status_code == 401

        create_staff()
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        # test without request body
        resp = client.post('/staff/change_password/')
        assert resp.status_code == 400

        # test with wrong request body
        resp = client.post('/staff/change_password/', json={
            "old_password": "supersecret",
            "password": "new_supersecret"
        })
        assert resp.status_code == 400

        # test with wrong password
        resp = client.post('/staff/change_password/', json={
            "password": "supersecret_",
            "new_password": "new_supersecret"
        })
        assert resp.status_code == 403

        # test change password
        resp = client.post('/staff/change_password/', json={
            "password": "supersecret",
            "new_password": "new_supersecret"
        })
        assert resp.status_code == 200

        # login with new_password
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "new_supersecret"
        })
        assert resp.status_code == 200

    def test_reset_password(self, client):

        # test reset password without authorization
        resp = client.post('/staff/reset_password/')
        assert resp.status_code == 401

        # test reset password not as admin
        create_staff()
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        resp = client.post('/staff/reset_password/')
        assert resp.status_code == 401

        # logout from staff
        resp = client.post('/staff/logout/')
        assert resp.status_code == 200

        # login as admin
        create_staff(username="admin", admin=True)
        resp = client.post('/staff/login/', json={
            "username": "admin",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        # test without request body
        resp = client.post('/staff/reset_password/')
        assert resp.status_code == 400

        # test with wrong request body
        resp = client.post('/staff/reset_password/', json={
            "staff": "staff",
            "password": "password"
        })
        assert resp.status_code == 400

        # test with incomplete request body
        resp = client.post('/staff/reset_password/', json={
            "password": "password"
        })
        assert resp.status_code == 400

        # test change password
        resp = client.post('/staff/reset_password/', json={
            "username": "staff",
            "password": "new_password"
        })
        assert resp.status_code == 200

        # logout from admin
        resp = client.post('/staff/logout/')
        assert resp.status_code == 200

        # test logging in with old password
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 403

        # test logging in with new password
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "new_password"
        })
        assert resp.status_code == 200

    def test_manage_products(self, client):

        # test post product without authorization
        resp = client.post('/staff/products/')
        assert resp.status_code == 401

        # test patch product without authorization
        resp = client.patch('/staff/products/10000/')
        assert resp.status_code == 401

        # test delete product without authorization
        resp = client.delete('/staff/products/10000/')
        assert resp.status_code == 401

        # test manage product
        create_staff()
        resp = client.post('/staff/login/', json={
            "username": "staff",
            "password": "supersecret"
        })
        assert resp.status_code == 200

        # test without request body
        resp = client.post('/staff/products/')
        assert resp.status_code == 400

        # test with incomplete request body
        resp = client.post('/staff/products/', json={
            "isbn": "isbn_test",
            "title": "title_test",
            "msrp": 100,
            "price": 90,
            "genre": "genre_test"
        })
        assert resp.status_code == 400

        # test with wrong request body
        resp = client.post('/staff/products/', json={
            "isbn": "isbn_test",
            "title": "title_test",
            "author": "author_test",
            "publisher": "publisher_test",
            "msrp": "msrp_test",
            "price": "price_test",
            "genre": "genre_test",
        })
        assert resp.status_code == 400

        # test post product request body
        resp = client.post('/staff/products/', json={
            "isbn": "isbn_test",
            "title": "title_test",
            "author": "author_test",
            "publisher": "publisher_test",
            "msrp": 100,
            "price": 90,
            "copies": 10,
            "genre": "genre_test"
        })
        assert resp.status_code == 200

        resp = client.get('/books/10000/')
        assert resp.status_code == 200

        # test returned data contains correct data
        assert b'"isbn":"isbn_test"' in resp.data
        assert b'"author":"author_test"' in resp.data
        assert b'"publisher":"publisher_test"' in resp.data
        assert b'"msrp":100' in resp.data
        assert b'"price":90' in resp.data
        assert b'"copies":10' in resp.data
        assert b'"genre":"genre_test"' in resp.data

        # test patch without request body
        resp = client.patch('/staff/products/10000/')
        assert resp.status_code == 400

        # test patch with wrong request body
        resp = client.patch('/staff/products/10000/', json={
            "isbn": "isbn_test",
            "title": "title_test",
            "author": "author_test",
            "publisher": "publisher_test",
            "msrp": "msrp_test",
            "price": "price_test",
            "genre": "genre_test",
        })
        assert resp.status_code == 400

        # test patch non existing product
        resp = client.patch('/staff/products/10005/', json={
            "isbn": "isbn_test",
            "title": "title_test",
            "author": "author_test",
            "publisher": "publisher_test",
            "msrp": 150,
            "price": 120,
            "copies": 10,
            "genre": "genre_test",
        })
        assert resp.status_code == 404

        # test patch product
        resp = client.patch('/staff/products/10000/', json={
            "isbn": "isbn_test",
            "title": "title_test",
            "author": "author_test",
            "publisher": "publisher_test",
            "msrp": 150,
            "price": 120,
            "copies": 10,
            "genre": "genre_test",
        })
        assert resp.status_code == 200

        # get updated product
        resp = client.get('/books/10000/')
        assert resp.status_code == 200

        # test returned data contains correct data
        assert b'"isbn":"isbn_test"' in resp.data
        assert b'"author":"author_test"' in resp.data
        assert b'"publisher":"publisher_test"' in resp.data
        assert b'"msrp":150' in resp.data
        assert b'"price":120' in resp.data
        assert b'"copies":10' in resp.data
        assert b'"genre":"genre_test"' in resp.data

        # test delete non existing product
        resp = client.delete('/staff/products/10005/')
        assert resp.status_code == 404

        # test delete product
        resp = client.delete('/staff/products/10000/')
        assert resp.status_code == 200

        # test product deleted
        resp = client.get('/books/10000/')
        assert resp.status_code == 404
