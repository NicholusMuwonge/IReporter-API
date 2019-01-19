
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask,json,jsonify # test db db for travis , discover flask configurations
# from dotenv import load_dotenv


class DatabaseConnection:

    def __init__(self):

        if os.getenv("HEROKU_ENV") == 'heroku_database':
            self.connection = psycopg2.connect(
                host="ec2-54-225-227-125.compute-1.amazonaws.com", database="d95nn0mi29nlqj", user="mretfseraxhfos",
                port="5432", password="50f7e8f2d88a9fd05fe86691b7ae23d2529577ed0bb1a10ab6a6154581f404a3")
        else:
            
            self.connection = psycopg2.connect(host="localhost", database="trying", user="postgres",
            port="5432", password="")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.dict_cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def create_tables(self):
        """
        This method creates tables one after the other in the database after the connection has been established.

        """

        commands = (
            """
            CREATE TABLE IF NOT EXISTS "user_list" (
                    user_id SERIAL NOT NULL PRIMARY KEY,
                    user_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    admin VARCHAR(100) DEFAULT 'FALSE',
                    user_password VARCHAR(255) NOT NULL

                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "records" (
                    record_no SERIAL NOT NULL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES "user_list" (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    record_title VARCHAR(255) NOT NULL,
                    record_geolocation VARCHAR(255) NOT NULL,
                    record_type VARCHAR(255) NOT NULL,
                    status VARCHAR(255) NOT NULL DEFAULT 'Pending',
                    record_placement_date TIMESTAMP DEFAULT NOW() NOT NULL
                    )
            """
        )

        try:
            for command in commands:
                self.cursor.execute(command)
            self.connection.commit()
            self.cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.connection is not None:
                self.connection.close()

    def insert_user(self, user_name, email,user_password):
        """
        add new user to database
        :param user_name:
        :param email:
        :param user_password:
        :return:
        """
        add_user = """INSERT INTO user_list (user_name, email,user_password)
                   VALUES ('{0}', '{1}', '{2}');""".format(user_name, email, user_password)
        self.cursor.execute(add_user)
        return jsonify({'message':'user_created successfuly'})

    def find_user_by_username(self, user_name):
        """
        find a specific user given a user name
        :param user_name:
        :return:
        """

        name = "SELECT * FROM user_list WHERE user_name ='{}'".format(user_name)
        self.cursor.execute(name)
        username_returned = self.cursor.fetchone()
        return username_returned

    def find_user_by_id(self, user_id):
        """
        adminstrator can request for details about a particular user
        :param user_id:
        :return:
        """

        user = "SELECT * FROM user_list WHERE user_id ='{}'".format(user_id)
        self.cursor.execute(user)
        user_returned = self.cursor.fetchone()
        return user_returned

    def find_user_by_email(self, email):
        """
        find a specific user using an email
        :param email:
        :return:
        """
        user_returned = "SELECT * FROM user_list WHERE email = '{}'".format(email)
        self.cursor.execute(user_returned)
        check_email = self.cursor.fetchone()
        return check_email

    def post_record(self, record_title,record_geolocation,record_type, user_id):
        """
        insert record details into the table records
        :param record_title:
        :param record_geolocation:
        :param record_type:
        :param status:
        :param user_id:
        :return:
        """
        record_posted = """INSERT INTO records (record_title,record_geolocation,record_type, user_id)
                    VALUES ('{0}', '{1}', '{2}', '{3}');""".format(record_title,record_geolocation,record_type, user_id)
        self.cursor.execute(record_posted)
        return ('created')

    def get_all_records(self):
        """
        return all records created
        :return:
        """
        all_records = "SELECT * FROM records;"
        self.dict_cursor.execute(all_records)
        records_returned = self.dict_cursor.fetchall()
        return records_returned

    def get_one_record_using_record_no(self, record_no):
        """
        get a specific record from the records table using the record_no
        :param record_no:
        :return:
        """
        one = "SELECT * FROM records WHERE record_no = '{}';".format(record_no)
        self.dict_cursor.execute(one)
        record = self.dict_cursor.fetchone()
        return jsonify(record)

    def get_records_for_specific_users(self, user_id):
        """
        return all records created by a particular user
        :param user_id:
        :return:
        """
        user_records = "SELECT * FROM records WHERE user_id ='{}'".format(user_id)
        self.dict_cursor.execute(user_records)
        get_records = self.dict_cursor.fetchall()
        return jsonify(get_records)

    def update_record_geolocation(self,record_geolocation,record_no):
        """
        user updates a specific record by adjusting the geolocation figures
        :param record_geolocation:
        :param record_no:
        :return:
        """
        record_update = "UPDATE records SET record_geolocation = '{}' WHERE record_no = '{}'".format(record_geolocation,record_no)
        self.cursor.execute(record_update)
        return True

    def record_status(self,status,record_no):
        """
        update the  status of a given record  order
        :param status:
        :param record_no:
        :return:
        """
        update = "UPDATE records SET status = '{}' WHERE record_no = '{}'".format(status,record_no)
        self.cursor.execute(update)

    def change_status(self, status, record_no):
        """
        change the state of the posted record by adminstrator
        :param status:
        :param record_no:
        :return:
        """
        update = """UPDATE records SET status = '{}' WHERE record_no = '{}';""".format(status,record_no)
        self.cursor.execute(update)
        return True

    # def update_(self, present_location,  record_no):
    #     """
    #     update the present location of a record  order
    #     :param present_location:
    #     :param record_no:
    #     :return:
    #     """
    #     update = """UPDATE records SET present_location = '{}' WHERE record_no = '{}';""".format(present_location,
    #                                                                                              record_no)
    #     self.cursor.execute(update)
    def check_records_approved(self,status):
        """
        get all records that have been approved by the adminstrator
        :param status:
        :return:
        """
        records="""(SELECT * FROM records WHERE status='Approved')"""
        self.cursor.execute(records)
        returned_records=self.cursor.fetchall()
        return returned_records

    def check_for_cancelled_records(self, record_no):
        """
        get all records that have been denied by the adminstrator
        :param status:
        :return:
        """
        records="""(SELECT * FROM records WHERE status='Cancelled')"""
        self.cursor.execute(records)
        returned_records=self.cursor.fetchall()
        return returned_records

    def delete_record(self, record_no):
        """
        Get a specific record to check whether  status has been delivered
        :param record_no:
        :return:
        """
        records="DELETE FROM records WHERE record_no='{}'".format(record_no)
        delete=self.cursor.execute(records)
        if delete:
            return ({"message":"item successfully deleted"})
        else:
            return ({'message':'please try again or item not found'})

    def check_admin(self):
        """
        method to set admin to true which gives a user admin privileges.
        :return:
        """
        self.cursor.execute("UPDATE user_list SET admin = 'TRUE' WHERE user_id = 1")


DatabaseConnection().create_tables()
