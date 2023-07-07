from abc import ABC, abstractmethod  # Abstract Based Classes
from typing import List


class DataManagerInterface(ABC):
    """
    An Interface Class that reading the JSON file,
    parsing the JSON into Python
    data structures (lists and dictionaries),
    and providing methods to
    manipulate the data
    (like adding, updating, or removing movies)

    Data management for a JSON file
    and other sources such as
    a CSV file or a database.
    """
    @abstractmethod
    def get_all_users(self) -> List[dict]:
        """
        Return a list of all users
        :return:
            a list of users dictionaries (List[dict])
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id: int) -> List[dict] | None:
        """
        Return a list of all movies for a given user
        :param
            user_id: int
        :return:
            a list of movies dictionaries for the given user (List[dict])
        """
        pass
