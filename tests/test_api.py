"""
Tests module
"""
from flask import json
from flask_jwt_extended import get_csrf_token,jwt_refresh_token_required,jwt_required

import unittest

from run import app


class TestIt(unittest.TestCase):
    """
    Tests run for the api endpoints
    """

    def setUp(self):
        self.app = app
        self.client = self.app.test_client

    def test_home(self):
        item=self.client().get('/',content_type='application/json')
        self.assertEqual(item.status_code,200)
        

    def register_user(self, user_name=None, email=None,  user_password=None):
        return self.client().post(
            '/api/v2/auth/signup/',
            data=json.dumps(dict(
                user_name=user_name,
                email=email,
                user_password=user_password,
            )),
            content_type="application/json"
        )

    def login_user(self, user_name=None, user_password=None):
        return self.client().post(
            '/api/v2/auth/login/',
            data=json.dumps(dict(
                user_name=user_name,
                user_password=user_password,
            )),
            content_type='application/json'
        )

    def post_record(self, record_title=None, record_geolocation=None, record_type=None, token=None):
        return self.client().post(
            '/api/v2/records/',
            headers=dict(
                Authorization='Bearer ' + token
            ),
            data=json.dumps(dict(
                record_title=record_title,
                record_geolocation=record_geolocation,
                record_type=record_type
               

            )),
            content_type="application/json"
        )

    # ....................Testing user authentication, signup and login.............................................. #

    def test_missing_fields_during_signup(self):
        """
        Test for missing fields when registering a new user
        :return:
        """
        register = self.client().post(
            '/api/v2/auth/signup/',
            data=json.dumps(dict(
                user_name='Apple',
                email='apple@gmail.com',
    
            )),
            content_type="application/json"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'some fields are missing')
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_invalid_data_type(self):
        """
        Test user registration with invalid data-type
        :return:
        """
        register = self.register_user(10000, 'apple@gmail.com',  'acireba')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'], 'fail')
        self.assertTrue(received_data['error_message'], 'Please use character strings')
        self.assertFalse(received_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_empty_fields_during_signup(self):
        """
        Test for empty fields during user registration
        :return:
        """
        register = self.register_user(' ', 'nicks@gmail.com', 'nicksbro')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Some fields have no data')
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_invalid_password(self):
        """
        Test for password less than 5 characters
        :return:
        """
        register = self.register_user('Yapsis', 'nick@gmail.com',  'mat')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'],
                        'Password is wrong. It should be at-least 5 characters long, and alphanumeric.')
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_invalid_email_registration(self):
        """
        Test for registration with invalid email
        :return:
        """
        register = self.register_user('Yapsis', 'nicks@gmail',  'nicksbro')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'User email {0} is wrong,'
                                                        'It should be in the format (xxxxx@xxxx.xxx)')
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    # def test_invalid_phone_number(self):
    #     """
    #     testing invalid phone_number
    #     :return:
    #     """
    #     register = self.register_user('Apple', 'app0@gmail.com', '070419', 'acireba')
    #     received_data = json.loads(register.data.decode())
    #     self.assertTrue(received_data['error_message'], 'Contact {0} is wrong. should be in the form, (070*******)'
    #                                                     'and between 10 and 13 digits')
    #     self.assertTrue(received_data['data'])
    #     self.assertTrue(register.content_type, 'application/json')
    #     self.assertEqual(register.status_code, 400)

    def test_invalid_user_name(self):
        """
        testing invalid username
        :return:
        """
        register = self.register_user('Apple56', 'apple@gmail.com',  'acireba')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'], 'fail')
        self.assertTrue(received_data['error_message'], 'A name should consist of only alphabetic characters')
        self.assertTrue(received_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 400)

    def test_user_name_exists(self):
        """
        Test when the user name already exists
        :return:
        """
        self.register_user('Apple', 'apple@gmail.com',  'acireba')
        register = self.register_user('Apple', 'app@gmail.com',  'acireba')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Username already taken')
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type, 'application/json')
        self.assertEqual(register.status_code, 409)

    def test_registered_user_login(self):
        """
        Test for proper registered user login
        :return:
        """
        self.register_user('Joan', 'jojo@gmail.com', 'acireba')
        login_user = self.login_user('Joan','acireba')

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'], 'success')
        self.assertTrue(response_data['message'], 'You are logged in')
        self.assertTrue(response_data['access_token'])
        self.assertTrue(response_data['logged_in_as'], 'Joan')
        self.assertTrue(login_user.content_type, 'application/json')
        self.assertEqual(login_user.status_code, 200)

    def test_non_registered_user_login(self):
        """
        Test for login of a non registered user
        :return:
        """
        login_user = self.login_user( 'acireba','Anna')
        data = json.loads(login_user.data.decode())
        self.assertTrue(data['status'], 'fail')
        self.assertTrue(data['message'], 'User does not exist.')
        self.assertTrue(login_user.content_type, 'application/json')
        self.assertEqual(login_user.status_code, 404)

    def test_login_with_missing_fields(self):
        """
        Test for login with missing fields
        :return:
        """
        self.register_user('Apple', 'apple@gmail.com',  'acireba')
        login_user = self.client().post(
            '/api/v2/auth/login/',
            data=json.dumps(dict(
                user_name="Apple"
            )),
            content_type='application/json'
        )

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'some fields are missing')
        self.assertTrue(login_user.content_type, 'application/json')
        self.assertEqual(login_user.status_code, 400)

    def test_login_with_invalid_data_type(self):
        """
        Test for login with invalid data types
        :return:
        """
        self.register_user('Apple', 'apple@gmail.com',  'acireba')
        login_user = self.login_user('Apple', 100100)

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Please use character strings')
        self.assertTrue(login_user.content_type, 'application/json')
        self.assertEqual(login_user.status_code, 400)

    def test_login_with_empty_fields(self):
        """
        Test for login with empty fields
        :return:
        """
        self.register_user('Apple', 'apple@gmail.com', 'acireba')
        login_user = self.login_user('Apple', '')

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'], 'fail')
        self.assertTrue(response_data['error_message'], 'Some fields have no data')
        self.assertTrue(login_user.content_type, 'application/json')
        self.assertEqual(login_user.status_code, 400)

    # ....................Testing parcels endpoints.............................................. #

    def test_post_record(self):
        """
        Test for posting a record 
        :return:
        """
        # user signup
        self.register_user('Apple', 'apple@gmail.com',  'acireba')

        # user login
        login = self.login_user( 'Apple','acireba')

        # Add parcel
        add_record= self.post_record("Marvin", "Bunga", "Gaba",
                                              json.loads(login.data.decode())['access_token'])

        data = json.loads(add_record.data.decode())

        self.assertTrue(data['message'], 'Successfully posted a parcel delivery order')
        self.assertTrue(add_record.content_type,'application/json')
        self.assertTrue(data['data'])
        self.assertEqual(add_record.status_code, 201)

    def test_post_record_with_empty_fields(self):
        """
        Test for adding a record with empty fields
        :return:
        """
        # signup user
        self.register_user('Sharon', 'Shan@gmail.com', 'acireba')

        # user login
        login = self.login_user('Sharon','acireba' )

        # Add order
        add_parcel = self.post_record(" ", "Gaba", "bunga" ,json.loads(login.data.decode())['access_token'])

        data = json.loads(add_parcel.data.decode())

        self.assertTrue(data['status'], 'fail')
        # self.assertTrue(data['error_message'], 'Some fields have no data')
        # self.assertFalse(data['data'])
        self.assertTrue(add_parcel.content_type, 'application/json')
        # self.assertEqual(add_parcel.status_code, 400)

    def test_post_record_with_missing_fields(self):
        """
        Test for adding a parcel order with missing fields
        :return:
        """
        # sign up user
        self.register_user('Ogal', 'ogal@gmail.com', 'acireba')

        # user login
        login = self.login_user('Ogal', 'acireba')

        make_delivery_order = self.client().post(
            '/api/v2/records/',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['access_token']
            ),
            data=json.dumps(dict()),
            content_type="application/json"
        )

        data = json.loads(make_delivery_order.data.decode())

        self.assertTrue(data['status'], 'fail')
        # self.assertTrue(data['error_message'], 'some fields are missing')
        # self.assertTrue(data['data'])
        self.assertTrue(make_delivery_order.content_type, 'application/json')
        # self.assertEqual(make_delivery_order.status_code, 400)

    def test_post_record_with_wrong_data_type(self):
        """
        Test for adding a parcel order with wrong data type
        :return:
        """

        # signup user
        self.register_user('Suzan', 'sue@gmail.com',  'acireba')

        # user login
        login = self.login_user('Suzan', 'acireba')

        # Add parcel order
        print(login.data.decode())
        add_parcel = self.post_record('', "Bunga", "Gaba",
                                              json.loads(login.data.decode())['access_token'])

        data = json.loads(add_parcel.data.decode())

        self.assertTrue(data['status'], 'fail')
        self.assertTrue(data['error_message'], 'Please use character strings')
        self.assertFalse(data['data'])
        self.assertTrue(add_parcel.content_type, 'application/json')
        self.assertEqual(add_parcel.status_code, 400)
