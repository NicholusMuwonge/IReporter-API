from .controller import User,User_class,Record
from .user_login_controller import user_login
from app import create_app

record_object=Record() #create a record object.


""" we name the app,(create an instance of flask)"""

app=create_app()
user_object=User()
i=User_class()

""" route for the home"""

class routes:
    @staticmethod
    def endpoints(app):
        app.add_url_rule('/', view_func=Record.as_view('home'),methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/records', view_func=Record.as_view('add_record'),methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/records', view_func=Record.as_view('get_all_records'),methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/records/<int:record_no>', view_func=Record.as_view('update_record'),methods=['PUT'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/records/<int:record_no>', view_func=Record.as_view('return_one_record_no'),methods=['GET'], strict_slashes=False)
        #app.add_url_rule('/api/v1/auth/records/<str:record_title>', view_func=Record.as_view('return_one_by_title'),methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/records/<int:user_id>', view_func=Record.as_view('return_one_user_records'),methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/records/<int:record_no>', view_func=Record.as_view('delete_record'),methods=['DELETE'], strict_slashes=False)
        app.add_url_rule('/api/v1/users/signup', view_func=User.as_view('create_user'),methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/users/login', view_func=user_login.as_view('login_user'),methods=['POST','GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/users', view_func=User.as_view('get_all_users'),methods=['GET'], strict_slashes=False)
        
        