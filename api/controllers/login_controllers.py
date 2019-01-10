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
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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

        if user and Authenticate.verify_password(user_password, user[4]):

            response_object = {
                'status': 'success',
                'message': 'You are logged in',
                'access_token': create_access_token(identity=user,
                                                    expires_delta=datetime.timedelta(minutes=60)),
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
        admin = user[4]

        if user_id and admin == "FALSE":
            my_records = self.data.get_records_for_specific_users(user_id)
            if isinstance(my_records, object):
                user = self.data.get_records_for_specific_users(user_id)
                records = []
                for record in my_records:
                    res_data = {
                        "user_name": user[1],
                        "record_title": record['record_title'],
                        "record_geolocation": record['record_geolocation'],
                        "record_type": record['record_type'],
                        "status": record['status'],
                        "record_no": record['record_no'],
                        "record_placement_date": record['record_placement_date']
                    }
                    records.append(res_data)
                response_object = {
                    "msg": "Successfully got all records belonging to user",
                    "data": records
                }
                return jsonify(response_object), 200
            else:
                return Error_message.no_items('record')
        return Error_message.permission_denied()

    # @jwt_required
    # # @swag_from('../docs/user_updates.yml')
    # def put(self, record_id):
    #     """
    #     Method for user to cancel a record delivery order
    #     :param record_id:
    #     :return:
    #     """
    #     user = get_jwt_identity()
    #     admin = user[4]
    #     user_id = user[0]

    #     if admin == "FALSE" and user_id:

    #         post_data = request.get_json()

    #         key = "delivery_status"
    #         key1 = "destination"
    #         status = ['cancelled']

    #         if key1 in post_data:
    #             if key1 not in post_data:
    #                 return Error_message.missing_fields(key1)
    #             if not post_data['destination']:
    #                 return Error_message.empty_data_fields()
    #             if DataValidation.check_string_of_numbers(post_data['destination']):
    #                 return Error_message.invalid_data_format()
    #             return self.update_record_destination(post_data['destination'].strip(), record_id)

    #         elif key:
    #             if key not in post_data:
    #                 return Error_message.missing_fields(key)
    #             try:
    #                 delivery_status = post_data['delivery_status'].strip()
    #             except AttributeError:
    #                 return Error_message.invalid_data_format()
    #             if not self.val.validate_string_input(delivery_status):
    #                 return Error_message.invalid_input()
    #             if not delivery_status:
    #                 return Error_message.empty_data_fields()
    #             if DataValidation.check_string_of_numbers(delivery_status):
    #                 return Error_message.invalid_data_format()
    #             if delivery_status not in status:
    #                 return Error_message.delivery_status_not_found(delivery_status)
    #             record = self.data.check_for_cancelled_records(record_id)
    #             if delivery_status == record[0] and delivery_status == 'cancelled':
    #                 return Error_message.record_already_cancelled()
    #             deliver = self.data.check_for_delivered_record(record_id)
    #             print(deliver)
    #             if delivery_status == deliver[0] and delivery_status == 'completed':
    #                 return Error_message.record_already_delivered()
    #             updated_status = self.data.cancel_delivery_order(delivery_status, record_id)
    #             if isinstance(updated_status, object):
    #                 response_object = {
    #                     'message': 'record delivery order has been cancelled successfully'
    #                 }
    #                 return jsonify(response_object), 202

    #     return Error_message.permission_denied()

    # def update_record_destination(self, destination, record_id):
    #     """
    #     Method to update the destination of a record delivery order
    #     :param destination:
    #     :param record_id:
    #     :return:
    #     """
    #     if self.data.get_one_record_order(record_id):

    #         updated_destination = self.data.update_destination(destination, record_id)
    #         if isinstance(updated_destination, object):
    #             response_object = {
    #                 'message': 'Destination has been updated successfully'

    #             }
    #             return jsonify(response_object), 202

    #     return Error_message.no_items('order')
