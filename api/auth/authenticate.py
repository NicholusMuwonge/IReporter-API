from api.models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash


class Authenticate:

    myUser = User()

    @staticmethod
    def hash_password(user_password):
        """
        method to hash password
        :param password:
        :return:
        """
        try:
            return generate_password_hash(user_password, method="sha256")

        except ValueError:
            return False

    @staticmethod
    def verify_password(password_text, hashed):
        """
        verify client password with stored password
        :param password_text:
        :param hashed:
        :return:
        """

        return check_password_hash(hashed, password_text)
