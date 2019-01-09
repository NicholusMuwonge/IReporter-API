import os
from flask import jsonify,json
from psycopg2.extras import RealDictCursor,RealDictConnection
import datetime


import psycopg2

class database:
    
    def __init__(self):
        
        # if os.getenv('APP_Config') == "testing":

        #     self.connect=psycopg2.connect(host="Nicks", database="test_db", user="postgres",
        #         port="5432", password="nicks")
        # else:
        self.connection = psycopg2.connect(host="Nicks", database="test_db", user="postgres",
            port="5432", password="nicks")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.dict_cursor = self.connection.cursor(cursor_factory=RealDictCursor)


    def create_tables(self):
        commands=(
            """CREATE TABLE IF NOT EXISTS "user_list"(
                    user_id SERIAL NOT NULL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    user_name VARCHAR(255) NOT NULL,
                    admin VARCHAR(100) DEFAULT 'FALSE',
                    user_password VARCHAR(255) NOT NULL
                    )""",
                    """
            CREATE TABLE IF NOT EXISTS "records" (
                    record_no SERIAL NOT NULL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES "user_list" (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    record_title VARCHAR(255) NOT NULL,
                    record_geolocation VARCHAR(255) NOT NULL,
                    status VARCHAR(255) NOT NULL DEFAULT 'New',
                    record_type VARCHAR(255) NOT NULL DEFAULT 'Office',
                    registered_date TIMESTAMP DEFAULT NOW() NOT NULL)
                    
            """

        )
        
        try:
            for command in commands: #for each of the tables in the commands each one of them is then created individually

                self.cursor.execute(command)
            self.connection.commit()
            self.cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.connection is not None:

                self.connection.close()


    def post_user(self,user_name,user_password,email):
        # registered_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert=""" INSERT INTO user_list (user_name,user_password,email) VALUES ('{0}','{1}','{2}');""".format(user_name,user_password,email)
        try:
            self.cursor.execute(insert)
            self.cursor.execute("SELECT * FROM user_list WHERE email = '%s';" % (email))
            item = self.cursor.fetchone()
            if item:
                return jsonify({"message":"user successfully inserted"})
        except psycopg2.IntegrityError:
            return jsonify({'message':'user already exists'})

    def get_user_by_id(self,user_id):
        user_to_be_returned="SELECT * FROM  user_list WHERE user_id ='{}'".format(user_id)
        self.cursor.execute(user_to_be_returned)
        get_user_id=self.cursor.fetchone()
        return get_user_id

    def get_user_by_user_name(self,user_name):
        user_to_be_returned="SELECT * FROM user_list WHERE user_name='{}'".format(user_name)
        self.cursor.execute(user_to_be_returned)
        get_user_name=self.cursor.fetchone()
        return get_user_name

    def get_user_by_email(self,email):
        user_to_be_returned="SELECT * FROM user_list WHERE email='{}'".format(email)
        self.cursor.execute(user_to_be_returned)
        get_email=self.cursor.fetchone()
        return get_email

    def get_all_users(self):
        users="""(SELECT * FROM user_list)"""
        self.cursor.execute(users)
        collected=self.cursor.fetchall()
        return jsonify(collected)

    def adminstrator(self):
        set_admin_user="""(UPDATE user_list SET admin='TRUE' WHERE user_id=1)"""
        self.cursor.execute(set_admin_user)

    
    """ Records """
    def insert_record(self,record_title,record_geolocation,record_type,user_id,record_no,record_date,record_status):
        insert_record="""INSERT INTO records (record_title,record_geolocation,record_type,user_id,record_no,record_date,record_status) VALUES ({0},{1},{2},{3},{4},{5},{6});""".format(record_geolocation,record_title,record_type,user_id,record_no,record_date,record_status)
        self.cursor.execute(insert_record)
        return "created"

    def get_all_records(self):
        get_all="""SELECT * FROM records"""
        self.cursor.execute(get_all)
        return "collected"

    def get_record_by_record_no(self,record_no):
        get_record_no="SELECT * FROM records WHERE record_no={}".format(record_no)
        self.cursor.execute(get_record_no)
        returned_record=self.cursor.fetchone()
        return returned_record

    def get_record_by_record_title(self,record_title):
        get_record_title="SELECT * FROM records WHERE record_title={}".format(record_title)
        self.cursor.execute(get_record_title)
        returned_record=self.cursor.fetchone()
        return returned_record

    def get_specific_user_records(self,user_id):
        get_records_per_user="SELECT * FROM records WHERE record_title={}".format(user_id)
        self.cursor.execute(get_records_per_user)
        returned_records=self.cursor.fetchall()
        return returned_records

    def update_redflag_record_geolocation_using_record_no(self,record_no,record_geolocation):
        record_to_be_updated="""(UPDATE records SET record_geolocation='{}' WHERE record_no='{}';)""".format(record_geolocation,record_no)
        self.cursor.execute(record_to_be_updated)
        return "updated"

    def update_redflag_record_geolocation_using_title(self,record_title,record_geolocation):
        record_to_be_updated="""(UPDATE records SET record_geolocation='{}' WHERE record_title='{}';)""".format(record_geolocation,record_title)
        self.cursor.execute(record_to_be_updated)
        return "updated"

    def update_redflag_record_status(self,record_no,status):
        record_to_be_updated="""(UPDATE records SET status='{}' WHERE record_no='{}';)""".format(status,record_no)
        self.cursor.execute(record_to_be_updated)
        return "updated"

    def check_records_approved(self,status):
        records="""(SELECT * FROM records WHERE status='Approved')"""
        self.cursor.execute(records)
        returned_records=self.cursor.fetchall()
        return returned_records

    def check_records_cancelled(self,status):
        records="""(SELECT * FROM records WHERE status='Cancelled')"""
        self.cursor.execute(records)
        returned_records=self.cursor.fetchall()
        return returned_records

    def check_records_Pending(self,status):
        records="""(SELECT * FROM records WHERE status='Pending')"""
        self.cursor.execute(records)
        returned_records=self.cursor.fetchall()
        return returned_records

    def delete_a_particular_record(self,record_no):
        records="""(DELETE * FROM records WHERE record_no=('{}';)).format(record_no)"""
        delete=self.cursor.execute(records)
        if delete:
            return ({"message":"item successfully deleted"})
        else:
            return ({'message':'please try again'})

    def check_admin(self):
        """
        method to set admin to true which gives a user admin privileges.
        :return:
        """
        self.cursor.execute("UPDATE user_list SET admin = 'TRUE' WHERE user_id = 1")

database().create_tables()



    