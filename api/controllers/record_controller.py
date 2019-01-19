"""
Directors on what to do with data from the models
"""
from flask import request, jsonify
from flask.views import MethodView
from api.models.record_model import Record
from api.Error.responses import Error_message
from api.utils.verifications import Verification
from api.models.database import DatabaseConnection
from flask_jwt_extended import jwt_required, get_jwt_identity
# from flasgger import swag_from


class Record_logic(MethodView):
    """
    Class with  methods to handle get, post and put methods
    """
    record_title = None
    record_geolocation = None
    record_type = None
    status='Pending'
    val = Verification()
    record_data = Error_message()
    data = DatabaseConnection()
    record=Record()

    @jwt_required
    # @swag_from('../docs/post_record.yml')
    def post(self):
        """
        post method to handle posting an record
        :return:
        """
        user = get_jwt_identity()
        admin = user[3]
        user_id = user[0]

        if user_id and admin == "FALSE":

            post_data = request.get_json()
            keys = ("record_title", "record_geolocation", "record_type")

            if not set(keys).issubset(set(post_data)):
                return Error_message.missing_fields(keys)
            

            try:
                self.record_title = post_data['record_title'].strip()
                self.record_geolocation = post_data['record_geolocation'].strip()
                self.record_type = post_data['record_type'].strip()
                

            except AttributeError:
                return Error_message.invalid_data_format()

            if not self.record_title or not self.record_geolocation or not self.record_type :
                return Error_message.empty_data_fields()
            
            # if not self.record_type == 'redflag' or not self.record_type == 'intervention':
            #     return Error_message.non_apprpriate_record_type()
            # elif Verification.check_string_of_numbers(self.receivers_name) or \
            #         val.check_string_of_numbers(self.pickup_location) or \
            #         val.check_string_of_numbers(self.destination):
            #     return Error_message.invalid_data_format()
            # elif self.weight < 0:
            #     return Error_message.negative_number()

            new_record = self.record.post_record(self.record_type,self.record_geolocation,self.record_title,str(user_id))
            response_object = {
                'message': 'Successfully posted a new record ',
                'data': new_record
            }
            return jsonify(response_object), 201
        return Error_message.permission_denied()

    @jwt_required
    # @swag_from('../docs/get_all_records.yml')
    def get(self, record_no=None):
        """
        get method to return a list of record  records
        :param record_no:
        :return:
        """
        user = get_jwt_identity()
        user_id = user[0]
        admin = user[3]

        if admin != "FALSE" and user_id:

            if record_no:
                return self.data.get_one_record_using_record_no(record_no)

            all_records = self.data.get_all_records()

            if all_records:
                records = []
                for record in all_records:

                    user = self.data.find_user_by_id(record['user_id'])
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
                    "msg": "Successfully got all record  records",
                    "data": records
                    }
                return jsonify(response_object), 200
            else:
                return Error_message.no_items('record')

        return Error_message.denied_permission()

    

    # @jwt_required
    # def get_single_record(self, record_no):
    #     """
    #     Method to return a single record  record
    #     :param record_no:
    #     :return:
    #     """
    #     user = get_jwt_identity()
    #     admin = user[4]
    #     user_id = user[0]

    #     if user_id and admin == "TRUE":

    #         single_record = self.data.get_one_record_record(record_no)
    #         if isinstance(single_record, object):
    #             user = self.data.find_user_by_id(single_record['user_id'])
    #             res_data = {
    #                 "user_name": user[1],
    #                 "receivers_name": single_record['receivers_name'],
    #                 "pickup_location": single_record['pickup_location'],
    #                 "destination": single_record['destination'],
    #                 "weight": single_record['weight'],
    #                 "_status": single_record['_status'],
    #                 "record_geolocation": single_record['record_geolocation'],
    #                 "record_date": single_record['record_date']
    #             }

    #             response_object = {
    #                 'msg': 'Successfully got one record  record',
    #                 'data': res_data
    #             }
    #             return jsonify(response_object), 200

    #         else:
    #             return Error_message.record_record_absent()

    #     return Error_message.denied_permission()

    @jwt_required
    # @swag_from('../docs/admin_updates.yml')
    def put(self, record_no=None,record_geolocation=None):
        """
        Method to update the record  status
        :param record_no:
        :return:
        """
        user = get_jwt_identity()
        admin = user[3]
        user_id = user[0]

        if admin == "TRUE" and user_id:

            post_data = request.get_json()

            key = "status"
            status = ['Approved','Denied']

            if key in post_data:
                try:
                    status = post_data['status'].strip()
                except AttributeError:
                    return Error_message.invalid_data_format()
                if not self.val.validate_string_input(status):
                    return Error_message.invalid_input()
                if not status:
                    return Error_message.empty_data_fields()
                if status not in status:
                    return Error_message.record_status_not_found(status)
                updated_status = self.data.change_status(status, record_no)
                if isinstance(updated_status, object):
                    response_object = {
                        'message': 'Status has been updated successfully'
                    }
                    return jsonify(response_object), 202
        
            
        return Error_message.denied_permission()


    @jwt_required
    def update_geolocation(self, record_geolocation, record_no):
        """
        Method to update the destination of a record  record
        :param record_geolocation:
        :param record_no:
        :return:
        """
        user = get_jwt_identity()
        admin = user[4]
        user_id = user[0]

        if admin != "TRUE" and user_id:
            if self.data.update_record_geolocation(record_geolocation,record_no):

                
                response_object = {
                    'message': 'Present location has been updated successfully'

                }
                return jsonify(response_object), 202

        return Error_message.no_items('record')

    @jwt_required
    def delete(self,record_no):
        """
        Method to update the destination of a record  record
        :param record_geolocation:
        :param record_no:
        :return:
        """
        user = get_jwt_identity()
        admin = user[4]
        user_id = user[0]

        if admin != "TRUE" and user_id:
            if self.data.delete_record(record_no):

                
                response_object = {
                    'message': 'Record has been deleted successfully'

                }
                return jsonify(response_object), 202

        return Error_message.no_items('record')

    
