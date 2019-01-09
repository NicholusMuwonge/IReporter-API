import os
from psycopg2.extras import RealDictCursor,RealDictConnection
import datetime
import re
from app.database.db import database
from flask import jsonify





""" creating users """
class User_class:

    database=database()

    def __init__ (self,user_name=None,user_password=None,email=None):
        
        self.user_name=user_name
        self.user_password=user_password
        self.email=email
        self.user_id= None
        self.registered_date=None
        self.phone_number=None
        self.user_type=True
        # self.increment=self.user_id+1 
        self.status='Pending'
        self.user_list=[]
        
        
    def create_user(self,user_name,user_password,email):
        # user_to_be_created=User_class(user_name,user_password,email,user_id,registered_date,status)
        class_user=User_class(user_name,user_password,email)
        self.database.post_user(user_name,user_password,email)
        del class_user.user_id
        return (class_user)


    # def user_mail_setting(self,email) -> bool :
    #   email_pattern=re.compile(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$")
    #   if email_pattern:
    #       return True
    #   return False


class Record:
    db=database()
    def __init__(self,record_no,record_geolocation,record_status,record_title,record_type,user_id,record_date):
        self.record_no=None
        self.record_geolocation=None 
        self.status= 'Pending'
        self.record_title=None 
        self.record_type='Redflag'
        self.user_id=None
    
    def create_record(self,record_no,record_geolocation,status,record_title,record_type,user_id,record_date,record_status):
        # record_to_be_created=Record(record_no,record_geolocation,status,record_title,record_type,user_id)
        record_to_be_created=self.db.insert_record(record_title,record_geolocation,record_type,user_id,record_date,record_no,record_status)
        return record_to_be_created









































































































# def user_id_setting(self,user_id):
#         for user_id in self.user_list :
#             if self.user_id != 1 and self.user_id >1:
#                 new_user_id=user_id+1
#                 return int(new_user_id)

#     def user_type_setting(self,user_type) -> bool:
#         if user_type !=True:
#             return 'Admin'
#         else:
#             return 'User'
        
#     def user_password_setting(self,user_password):
#         self.user_password=input('')
#         for digit in self.user_password:
#             if not isinstance (digit,str): #or if len(self.user_password) =< 5 :
#                 return "create another password that may contain both words and numbers",400

#             if len(self.user_password) < 5 and len(self.user_password)>13:
#                 return "improve your password",400