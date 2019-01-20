"""
This module looks at the user login
"""
import datetime

from flask import request, jsonify
from flask.views import MethodView
from api.Error.responses import Error_message
from api.auth.authenticate import Authenticate
from api.models.database import DatabaseConnection
from api.models.record_model import Record
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
    )
from api.utils.verifications import Verification
# from flasgger import swag_from


class Login(MethodView):
    """
    User login class
    """
    destination = None
    data = DatabaseConnection()
    auth = Authenticate()
    order = Record()
    val = Verification()

    # @swag_from('../docs/login.yml')
    def post(self):
        # to get post data
        post_data = request.get_json()
        keys = ('user_name', 'user_password')
        if not set(keys).issubset(set(post_data)):
            return Error_message.missing_fields(keys)
        try:
            user_name = post_data.get("user_name").strip()
            user_password = post_data.get("user_password").strip()
        except AttributeError:
            return Error_message.invalid_data_format()
        if not user_name or not user_password:
            return Error_message.empty_data_fields()
        user = self.data.find_user_by_username(user_name)

        if user and Authenticate.verify_password(
            user_password, user[4]
            ):
            response_object = {
                'status': 'success',
                'message': 'You are logged in',
                'access_token': create_access_token(
                    identity=user,expires_delta=datetime.timedelta(minutes=60)
                    ),
                'logged_in_as': str(user[1])
                }

            return jsonify(response_object), 200

        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return jsonify(response_object), 404

    @jwt_required
    # @swag_from('..docs/get_user_records.yml')
    def get(self, user_id):
        """
        Method to return a single users record records
        :return:
        """
        user = get_jwt_identity()
        admin = user[3]
        user_id = user[0]

        if user_id and admin == "FALSE" :
            my_records = self.data.get_records_for_specific_users(user_id)
            if isinstance(my_records, object):
                user=self.data.find_user_by_id(user_id)
                return (my_records), 200
            else:
                return Error_message.no_items('record')
        return Error_message.permission_denied()

    @jwt_required
    def put(self, record_geolocation=None, record_no=None):
        """
        Method to update the destination of a record  record
        :param record_geolocation:
        :param record_no:
        :return:
        """
        user = get_jwt_identity()
        admin = user[3]
        user_id = user[0]

        if admin == "FALSE" and user_id:
            post_data=request.get_json()
            keys=('record_geolocation')
            # if not set(keys).issubset((post_data)):
            #     return Error_message.missing_key(keys)
            if not keys:
                return Error_message.missing_fields(record_geolocation)
            try:
                record_geolocation=post_data['record_geolocation'].strip()
            except AttributeError:
                    return Error_message.invalid_data_format()
            if self.data.update_record_geolocation(record_geolocation,record_no):
                response_object = {
                    'message': 'Present location has\
                    been updated successfully'
                    }
                return jsonify(response_object), 202

            return Error_message.no_items('record')
        return Error_message.permission_denied()
