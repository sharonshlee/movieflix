from .data_manager_interface import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    """
    A class for managing data
    to and from a CSV file
    """

    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        """
        Return a list of all users
        :return:
        """
        pass

    def get_user_movies(self, user_id):
        """
        Return a list of all movies for a given user
        :param user_id: int
        :return:
        """
        pass