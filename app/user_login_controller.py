from flask import Flask,json,jsonify,make_response,request
from .model import User_class
from werkzeug.security import generate_password_hash, check_password_hash,safe_str_cmp
import datetime
from app.database.db import database
import re
from app.authenticate.authentication import Password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask.views import MethodView
from .model import User_class


class_object=User_class()
database=database()
Password=Password()


class user_login(MethodView):

    def post(self):
        # auth=request.authorisation
        data=request.get_json()

        user_fields=('email','user_password')

        if not set(user_fields).issubset(set(data)):
            response={'message':'missing fields'}
            return jsonify(response),400

        try:
            self.email =data.get('email').strip() 
            self.user_password =data.get('user_password').strip()
        except:
            return jsonify({'message':'invalid data format'}),400

        # current_user =database.get_user_by_email(self.email)
        # if current_user:
        #     continue
        # elif user['user_password'] != self.user_password :
        #     return jsonify({"Message": "wrong password "}),400
        # else:
        #     return jsonify({"Message": "No username  Found"}),404

        user_access=database.get_user_by_email(self.email)
        if user_access and Password.check_password(self.user_password,user_access[4]):

            response={'message':'user_logged_in','access_token':create_access_token(identity=user_access,
                                                    expires_delta=datetime.timedelta(hours=24)),'logged_in_as': str(user_access[2])}
            return jsonify(response)
        else:
            return jsonify({'message':'user_not_found, signup instead'}),404