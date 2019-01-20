from api.models.database import DatabaseConnection


class User:
    db = DatabaseConnection()

    def __init__(self, user_name=None, email=None, user_password=None):

        """
        User  class initialisation
        :param user_name:
        :param email:
        :param user_password:
        """
        self.user_name = user_name
        self.email = email
        self.user_password = user_password
        self.user_id = None

    def post_user(
        self, user_name=None, email=None, user_password=None
        ):
        """
        Register new user
        :param user_name:
        :param email:
        :param user_password:
        :return:
        """
        user = User(user_name, email, user_password)
        self.db.insert_user(user_name, email,user_password)

        del user.user_id

        return user
