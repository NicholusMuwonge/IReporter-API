"""
Module to handle url requests
"""
from api.controllers.signup_controllers import Signup
from api.controllers.login_controllers import Login
from api.controllers.record_controller import Record_logic


class Routes:
    """
        Class to generate urls
    """

    @staticmethod
    def generate(app):
        """
        Generate urls
        :param app:
        :return:
        """
        app.add_url_rule('/api/v2/auth/signup/', view_func=Signup.as_view('register_user'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v2/auth/login/', view_func=Login.as_view('login_user'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v2/records/', view_func=Record_logic.as_view('post_record'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v2/records/', view_func=Record_logic.as_view('get_all_records'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v2/record/<int:record_no>', view_func=Record_logic.as_view('get_one_record'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v2/users/<int:user_id>/records/',
                         view_func=Record_logic.as_view('get_specific_user_records'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v2/records/<int:record_no>/delete/',
                         view_func=Record_logic.as_view('delete_record'),
                         methods=['DELETE'], strict_slashes=False)
        app.add_url_rule('/api/v2/record_no/<int:record_no>/',
                         view_func=Record_logic.as_view('update_record_geolocation'),
                         methods=['PUT'], strict_slashes=False)
        app.add_url_rule('/api/v2/record/<int:record_no>/status/',
                         view_func=Record_logic.as_view('update_delivery_status'),
                         methods=['PUT'], strict_slashes=False)
        # app.add_url_rule('/api/v2/parcels/<int:Record_logic_no>/presentLocation/',
        #                  view_func=Record_logic.as_view('update_present_location'),
        #                  methods=['PUT'], strict_slashes=False)
