from werkzeug.http import parse_cookie

from config import settings
from config.utils import totp
from config.conftest import client


class CustomerTests:

    def test_mail_service(self, client):

        # test without request body
        resp = client.post('/mail/')
        assert resp.status_code == 400

        # test with wrong request body
        resp = client.post('/mail/', json={
            'test': 'test',
        })
        assert resp.status_code == 400

        resp = client.post('/mail/', json={
            'email': 'test@test.com'
        })
        assert resp.status_code == 200

    def test_signin(self, client):

        # test without request body
        resp = client.post('/email_signin/')
        assert resp.status_code == 400

        # test with wrong request body
        resp = client.post('/email_signin/', json={
            "name": 'name'
        })
        assert resp.status_code == 400

        # test email login
        otp = totp.now()  # create a dummy otp token
        resp = client.post('/email_signin/', json={
            'email': 'test123@test.com',
            'otp': otp
        })
        assert resp.status_code == 200

        # test if cookie is being set
        cookies = resp.headers.getlist('Set-Cookie')
        cookie = next(
            (cookie for cookie in cookies if '__USESSID_' in cookie), None)
        assert cookie is not None

        # test if cookie attributes are correct
        cookie_attrs = parse_cookie(cookie)
        assert 'Secure' in cookie_attrs
        assert 'HttpOnly' in cookie_attrs
        assert cookie_attrs['SameSite'] == 'Strict'

    def test_google_signin(self, client):

        # test without request body
        resp = client.post('/google_signin/')
        assert resp.status_code == 400

        # test with wrong request body
        resp = client.post('/google_signin/', json={
            'name': 'test'
        })
        assert resp.status_code == 400

        # test google signin
        resp = client.post('/google_signin/', json={
            'token': settings.GOOGLE_TEST_TOKEN
        })
        assert resp.status_code == 200

        # test if cookie is being set
        cookies = resp.headers.getlist('Set-Cookie')
        cookie = next(
            (cookie for cookie in cookies if '__USESSID_' in cookie), None)
        assert cookie is not None

        # test if cookie attributes are correct
        cookie_attrs = parse_cookie(cookie)
        assert 'Secure' in cookie_attrs
        assert 'HttpOnly' in cookie_attrs
        assert cookie_attrs['SameSite'] == 'Strict'

    def test_get_user(self, client):

        # test without authenticating
        resp = client.get('/me/')
        assert resp.status_code == 401

        # test with google signin
        resp = client.post('/google_signin/', json={
            'token': settings.GOOGLE_TEST_TOKEN
        })
        assert resp.status_code == 200
        resp = client.get('/me/')
        assert resp.status_code == 200

        # test if response has correct data
        assert b'"email":' in resp.data
        assert b'"name":' in resp.data
        assert b'"joined":' in resp.data

        # test email login
        otp = totp.now()  # create a dummy otp token
        resp = client.post('/email_signin/', json={
            'email': 'test123@test.com',
            'otp': otp
        })
        assert resp.status_code == 200
        resp = client.get('/me/')
        assert resp.status_code == 200

        # test if response has correct data
        assert b'"email":"test123@test.com"' in resp.data
        assert b'"name":"test"' in resp.data
        assert b'"joined":' in resp.data

    def test_edit_user(self, client):
        # test without authenticating
        resp = client.patch('/me/')
        assert resp.status_code == 401

        # test email login
        otp = totp.now()  # create a dummy otp token
        resp = client.post('/email_signin/', json={
            'email': 'test123@test.com',
            'otp': otp
        })
        assert resp.status_code == 200
        resp = client.get('/me/')
        assert resp.status_code == 200

        # test if response has correct data
        assert b'"name":"test"' in resp.data

        resp = client.patch('/me/', json={
            'name': 'new_name'
        })
        assert resp.status_code == 200
        resp = client.get('/me/')
        assert resp.status_code == 200

        # test if response has new data
        assert b'"name":"test"' not in resp.data
        assert b'"name":"new_name"' in resp.data

    def test_logout(self, client):

        # test logout
        resp = client.post('/logout/')
        assert resp.status_code == 401

        # test logout with google signin
        resp = client.post('/google_signin/', json={
            'token': settings.GOOGLE_TEST_TOKEN
        })
        assert resp.status_code == 200
        resp = client.post('/logout/')
        assert resp.status_code == 200

        # test logout with email signin
        otp = totp.now()  # create a dummy otp token
        resp = client.post('/email_signin/', json={
            'email': 'test123@test.com',
            'otp': otp
        })
        assert resp.status_code == 200
        resp = client.post('/logout/')
        assert resp.status_code == 200

    def test_address(self, client):

        # test get address without authorization
        resp = client.get('/me/address/')
        assert resp.status_code == 401

        # test post address without authorization
        resp = client.post('/me/address/')
        assert resp.status_code == 401

        # test patch address without authorization
        resp = client.patch('/me/address/10000/')
        assert resp.status_code == 401

        # test patch address without authorization
        resp = client.delete('/me/address/10000/')
        assert resp.status_code == 401

        # test get address
        otp = totp.now()  # create a dummy otp token
        resp = client.post('/email_signin/', json={
            'email': 'test123@test.com',
            'otp': otp
        })
        assert resp.status_code == 200

        resp = client.get('/me/address/')
        assert resp.status_code == 200
        assert b'[]' in resp.data

        # test without request body
        resp = client.post('/me/address/')
        assert resp.status_code == 400

        # test with incomplete request body
        resp = client.post('/me/address/', json={
            'name': "name",
            'address': "address",
            'locality': "locality",
            'pincode': "pincode"
        })
        assert resp.status_code == 400

        # test add address
        resp = client.post('/me/address/', json={
            'name': "name",
            'address': "address",
            'locality': "locality",
            'city': "city",
            'state': "state",
            'mobile': "mobile",
            'pincode': "pincode",
            'office': False,
            'default': False
        })
        assert resp.status_code == 200

        resp = client.get('/me/address/')
        assert resp.status_code == 200

        # test returned data is correct
        assert b'"id":10000' in resp.data
        assert b'"name":"name"' in resp.data
        assert b'"address":"address"' in resp.data
        assert b'"locality":"locality"' in resp.data
        assert b'"city":"city"' in resp.data
        assert b'"state":"state"' in resp.data
        assert b'"mobile":"mobile"' in resp.data
        assert b'"pincode":"pincode"' in resp.data
        assert b'"office":false' in resp.data
        assert b'"default":false' in resp.data

        # test update address without request body
        resp = client.patch('/me/address/10000/')
        assert resp.status_code == 400

        resp = client.patch('/me/address/10000/', json={
            'name': "name",
            'address': "address",
            'office': False,
            'default': False
        })
        assert resp.status_code == 400

        # test update address
        resp = client.patch('/me/address/10000/', json={
            'name': "name_new",
            'address': "address_new",
            'locality': "locality_new",
            'city': "city_new",
            'state': "state_new",
            'mobile': "mobile_new",
            'pincode': "pincode_new",
            'office': True,
            'default': True
        })
        assert resp.status_code == 200

        # test get updated data
        resp = client.get('/me/address/')
        assert resp.status_code == 200

        # test returned data is correct
        assert b'"id":10000' in resp.data
        assert b'"name":"name_new"' in resp.data
        assert b'"address":"address_new"' in resp.data
        assert b'"locality":"locality_new"' in resp.data
        assert b'"city":"city_new"' in resp.data
        assert b'"state":"state_new"' in resp.data
        assert b'"mobile":"mobile_new"' in resp.data
        assert b'"pincode":"pincode_new"' in resp.data
        assert b'"office":true' in resp.data
        assert b'"default":true' in resp.data

        # test delete address
        resp = client.delete('/me/address/10000/')
        assert resp.status_code == 200


        resp = client.patch('/me/address/10000/', json={
            'name': "name_new",
            'address': "address_new",
            'locality': "locality_new",
            'city': "city_new",
            'state': "state_new",
            'mobile': "mobile_new",
            'pincode': "pincode_new",
            'office': True,
            'default': True
        })
        assert resp.status_code == 404
