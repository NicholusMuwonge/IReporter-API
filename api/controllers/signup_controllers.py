"""
module to handle signup of the user
"""
from flask import request, jsonify
from flask.views import MethodView
from api.Error.responses import Error_message
from api.models.user_model import User
from api.utils.verifications import Verification
from api.auth.authenticate import Authenticate
# from flasgger import swag_from


class Signup(MethodView):
    """
    Registering a new user
    """
    myUser = User()
    val = Verification()

    # @swag_from('../docs/signup.yml')
    def post(self):

        post_data = request.get_json()

        keys = ("user_name", "email", "user_password")
        if not set(keys).issubset(set(post_data)):
            return Error_message.missing_fields(keys)
        try:
            user_name = post_data.get('user_name').strip()
            email = post_data.get('email').strip()
            user_password = post_data.get('user_password').strip()

        except AttributeError:
            return Error_message.invalid_data_format()

        if not user_name or not email  or not user_password:
            return Error_message.empty_data_fields()
        elif not self.val.validate_password(user_password, 5):
            return Error_message.invalid_password()
        elif not self.val.validate_email(email):
            return Error_message.invalid_email()
        elif not self.val.validate_name(user_name):
            return Error_message.invalid_name()
        elif not self.val.check_if_email_exists(email):
            return Error_message.email_already_exists()
        
        elif not self.val.check_if_user_name_exists(user_name):
            return Error_message.username_already_exists()

        user = self.myUser.post_user(user_name, email,
                                         Authenticate.hash_password(user_password))

        del user.user_password

        response_object = {
            'status': 'success',
            'message': 'Your account has been created successfully'
            }
        return jsonify(response_object), 201
