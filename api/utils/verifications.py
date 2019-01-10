"""
Module to handle validation
"""

import re
from api.models.database import DatabaseConnection


class Verification:
    """
    Class has methods to handle validation of data
    """
    data = DatabaseConnection()

    @staticmethod
    def check_string_of_numbers(test_data):
        try:
            int(test_data)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_email(email) -> bool:
        """
        Validate email address
        :param email:
        :return:
        """
        pattern = re.compile(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$")
        if not pattern.match(email):
            return False
        return True

    @staticmethod
    def validate_password(password, length) -> bool:
        """
        password validator
        :param password:
        :param length:
        :return:
        """
        if length > len(password):
            return False
        return password.isalnum()

    def check_if_email_exists(self, email):
        """
        Check if the email already exists
        :param email:
        :return:
        """
        if self.data.find_user_by_email(email):
            return False
        return True

    @staticmethod
    def validate_username(user_name):
        """
        Username validation
        :param name:
        :return:
        """
        username_regex = re.compile(r"^[A-Za-z\s]{4,30}$")
        if not username_regex.match(user_name):
            return False
        return True

    def check_if_user_name_exists(self, user_name):
        """
        Check if the username already exists
        :param username:
        :return:
        """
        if self.data.find_user_by_username(user_name):
            return False
        return True

    @staticmethod
    def validate_phone(phone_number) -> bool:
        """
        Validate contact number. Must be at least 10 digits
        and not more than 13
        :param phone_number:
        :return:
        """
        phone_regex = re.compile("^[0-9]{10,13}$")
        if phone_regex.match(phone_number):
            return True
        return False

    @staticmethod
    def validate_name(name):
        """
        Username validator
        :param name:
        :return:
        """
        username_regex = re.compile(r"^[A-Za-z\s]{4,30}$")
        if not username_regex.match(name):
            return False
        return True

    @staticmethod
    def validate_string_input(input_string):
        """
        String input validator
        :param input_string:
        :return:
        """
        string_regex = re.compile(r"^[A-Za-z\s]{4,30}$")
        if not string_regex.match(input_string):
            return False
        return True
