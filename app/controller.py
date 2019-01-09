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

class Record(MethodView):
     #initialize record lists
    def __init__(self):
        record_title=None
        record_type=None
        record_geolocation=None
        user_id=None

    def home(self):
        return "welcome"


    @jwt_required
    def   post(self,record):#record is the new redflag being created.
        """creating fields that will be returned automatically"""
        user= get_jwt_identity()
        adminstrator=user[4]
        user_id=user[0]

        if user_id and adminstrator =='FALSE':
            new_record=("record_title","record_type",'record_geolocation',"user_id")
            data=request.get_json()
            records=database.get_all_records()

            if not data or new_record not in data:
                return jsonify({'message':'missing keys'})
            
            if not "record_title" or not "record_type" or not "record_geolocation" in data:
                return jsonify({'message':'missing keys'})

            try:
                record_title=data.get['record_title'].strip()
                record_type=data.get['record_type'].strip()
                record_geolocation=data.get['record_geolocation'].strip()
                record_no= len(database.get_all_records())+1
                user_id = len(database.get_all_users())+1
                record_status= 'Pending'
                record_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            except:
                response={'message':'invalid format'}
                return jsonify(response),400

            if record_title or record_type or record_geolocation is None:
                response={'message':'fill in the missing fields'}
                return jsonify(response)
            elif not isinstance(record_geolocation,str):
                return jsonify({'message':'invalid format'})
            
            for user in records :
                if record_title==user['record_title'] :
                    response={'message':'This Title is already Taken'}
                    return jsonify(response),400
            created_record=database.insert_record(record_title,record_geolocation,record_type,user_id,record_no,record_date,record_status)

            response_object={'meassge':'record successfully created',
            'data':created_record}
            return jsonify(response_object),201


        

    @jwt_required
    def    get(self):
        user=get_jwt_identity()
        admin=user[4]
        
        if admin != "FALSE":
            records_to_be_returned= database.get_all_records()
            response_object={'message':'Dear adminstrator all the records have been retrieved',
            'data':records_to_be_returned}

            return jsonify(response_object),200
        else:
            response_object={'message':'There are no records to retrieve'}
            return jsonify(response_object),404

    

    @jwt_required
    def put(self,record_no,record_geolocation,status):
        user=get_jwt_identity()
        user_id=user[0]
        admin=user[4]

        
        if admin != "FALSE" and user_id:
            fields=('status','record_no')

            data=request.get_json()
            if fields not in data or not data:
                return jsonify({'message':'There are some missing fields'})
            try:
                status=data.get['status'].strip()
                record_no=data.get['record_no'].strip()

            except AttributeError:
                return jsonify({'message':'invalid format'})

            update_record=database.update_redflag_record_status(record_no,status)
            
            for fields in update_record:
                if fields['record_no']== record_no:
                    response_object={'message':'successfully updated',
                    'data':update_record}
                else:
                    return jsonify({'message':'record not found'})
                
            return jsonify(response_object)


        elif admin == "FALSE" and user_id:
            data=request.get_json()
            if fields not in data or not data:
                return jsonify({'message':'There are some missing fields'})
            try:
                record_geolocation=data.get['record_geolocation'].strip()
                record_no=data.get['record_no'].strip()

            except AttributeError:
                return jsonify({'message':'invalid format'})

            update_record=database.update_redflag_record_geolocation_using_record_no(record_no,record_geolocation)
            
            for fields in update_record:
                if fields['record_no']== record_no:
                    response_object={'message':'successfully updated',
                    'data':update_record}
                else:
                    return jsonify({'message':'record not found'})
                
            return jsonify(response_object)

        else:
            return jsonify({'message':'Error'})

            


            

    @jwt_required
    def return_one_record_no(self,record_no):
        user=get_jwt_identity()
        user_id=user[0]
        adminstrator=user[4]

        if user_id and adminstrator != "FALSE":
            all_records_returned=database.get_record_by_record_no(record_no)
            response_object= {'message':'successfully retrieved',
            'data':all_records_returned}
            return response_object,200

        else:
            response_object={'message':'the record is non existent'}
            return jsonify(response_object)

    @jwt_required
    def return_one_by_title(self,record_title):
        user=get_jwt_identity()
        user_id=user[0]
        adminstrator=user[4]

        if user_id and adminstrator != "FALSE":
            all_records_returned=database.get_record_by_record_title(record_title)
            response_object= {'message':'successfully retrieved',
            'data':all_records_returned}
            return response_object
        else:
            response_object={'message':'the record is non existent'}
            return jsonify(response_object)

        
    @jwt_required
    def GET(self,user_id):
        user=get_jwt_identity()
        user_id=user[0]
        adminstrator=user[4]

        if user_id and adminstrator != "FALSE":
            all_records_returned=database.get_specific_user_records(user_id)
            response_object= {'message':'successfully retrieved',
            'data':all_records_returned}
            return jsonify(response_object)
        else:
            response_object={'message':'the records are non existent'}
            return jsonify(response_object)

    
    






    @jwt_required
    def delete(self,record_no):
        user=get_jwt_identity()
        admin=user[4]
        user_id=user[0]
        if admin=='FALSE' and user_id:
            field=('record_no')
            data= request.get_json()
            if field not in data or not data:
                return jsonify({'message':'fields missing'})

            try:
                record_no=data.get['record_no'].strip()
            except ArithmeticError:
                return jsonify({'message':'Error'})
        record_deleted=database.delete_a_particular_record(record_no)

    
        for record in record_deleted:
            if record['record_no']==record_no:
                response_object={'message':'record successfuly deleted',
                'data':record_deleted}
                return jsonify(response_object)
            else:
                return jsonify({'message':'record not found'})
        return jsonify(response_object),200




class User(MethodView):
    def __init__(self):
       pass
        

    def post(self):
        data=request.get_json()
        new_user=("user_name","user_password","email")
        email_pattern=re.compile(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$")
        username_pattern = re.compile(r"^[A-Za-z\s]{4,15}$")
        if not set(new_user).issubset(set(data)):
            response=({'message':"INVALID FORMAT ,FILL IN THE MISSING KEYS"})
            return jsonify(response),400
        try:
            user_name=data.get('user_name').strip()
            user_password=data.get('user_password').strip()
            email=data.get('email').strip()
            
            

        except:
            response={'message':'Invalid data format'}
            return jsonify(response),400
        if len(user_name)==0 or len(user_password)==0 or len(email)==0:
            response={'message':'Fill in the missing fields'}
            return jsonify(response),400
        
        
        elif len(user_password)<5 or len(user_password)>13:
            response={'message':'improve your password quality'}
            return jsonify(response),400

        elif not isinstance (user_password,str):
            response={'message':'your password is supposed to contain letters or letters and numbers'}
            return jsonify(response),400
        
        
        if not email_pattern.match(email):
            return jsonify({'message':'invalid email format'}),400
        if not username_pattern.match(user_name):
            return jsonify({'message':'invalid user_name format'}),400
        
        list_to_be_checked=database.get_user_by_email(email)
        name_validation=database.get_user_by_user_name(user_name)
        if list_to_be_checked:
                return jsonify({'message':'user_exists'}),400
        if name_validation:
            return jsonify({'message':'user_name_taken_already,try yo pet name'}),400

        user_created=class_object.create_user(user_name,Password.generate_password(user_password),email)
        del user_created.user_password
        response=({'message':'user-successfully created','status': 'success'})
        return jsonify(response),201

        
        




    



    @jwt_required
    def get(self):
        user=get_jwt_identity()
        admin=user[4]
        if admin != "FALSE":
            users=database.get_all_users()
            response_object={'message':'users retrieved','data':users}
            return jsonify(response_object),200










