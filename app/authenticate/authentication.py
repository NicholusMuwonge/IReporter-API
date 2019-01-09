from werkzeug.security import generate_password_hash, check_password_hash,safe_str_cmp
from app.model import User_class
from flask import json,jsonify



class Password:
    user_class=User_class()

    @staticmethod
    def generate_password(user_password):
        try:
            return generate_password_hash(user_password,method='sha256')

        except:
            return jsonify({'message':'Error'})

    @staticmethod
    def check_password(password_text,hashed):

        try:
            return    check_password_hash(hashed,password_text)
        except:
            return jsonify({'message':'Error'})