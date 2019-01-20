import datetime
from api.models.database import DatabaseConnection


class Record:

    """
    This class uses the database to store data persistently
    """
    db = DatabaseConnection()

    def __init__(
        self, record_type=None, record_title=None, 
        record_geolocation=None, status=None, 
        user_id=None,record_no=None
        ):
        self.record_no = None
        self.user_id = user_id
        self.record_title = record_title
        self.record_geolocation = record_geolocation
        self.record_type = record_type
        self.status = 'Pending'
        self.record_placement_date = datetime.datetime.now().strftime\
        ("%Y-%m-%d %H:%M:%S")
        
        

    def post_record(
        self,record_type=None, record_title=None, 
        record_geolocation=None, user_id=None
        ):
        """
        Make new parcel delivery order
        :param receivers_name:
        :param pickup_location:
        :param destination:
        :param weight:
        :param user_id:
        :return:
        """
        record_placed = self.db.post_record(
            record_type, record_title, record_geolocation, user_id
            )

        return record_placed
