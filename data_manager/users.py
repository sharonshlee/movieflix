"""
Users class
Managing Users' CRUD operations
"""
from typing import List

from movieflix.data_manager.data_manager_interface import DataManagerInterface


class Users:
    """
    Users class
    Implementing Users' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager

    def get_all_users(self) -> List[dict] | None:
        """
        Return a list of all users
        :return:
            A list of dictionaries representing users
        """
        return self._data_manager.get_all_data()

    def get_user(self, user_id: int) -> dict | None:
        """
        Return a specific user given user_id
        :param user_id: int
        :return:
            User (dict) |
            None
        """
        return self._data_manager.get_item_by_id(user_id)

    @staticmethod
    def __validate_user_data(new_user: dict) -> bool:
        #  __ enforce stricter access control
        # accessible to internal class only
        """
        Check if  the new user data is valid
        :param
            new_user: (dict)
        :return:
            True if 'name' and 'movies' fields are present
        """
        return 'name' in new_user and 'movies' in new_user

    def add_user(self, new_user: dict) -> bool | None:
        """
        Add new user to json file
        :param new_user: (dict)
        :return:
            Successfully add user, True (bool)
            Invalid new user data, None
        """
        if self.__validate_user_data(new_user):
            return self._data_manager.add_item(new_user)
        return None

    def update_user(self, updated_user: dict):
        """
        Update a user info
        :param updated_user: dict
        :return:
            True for success update user (bool) |
            None
        """
        return self._data_manager.update_item(updated_user)

    def delete_user(self, user_id: int) -> bool | None:
        """
        Delete a user
        :param user_id: int
        :return:
            True for success delete user (bool) |
            None
        """
        return self._data_manager.delete_item(user_id)

    def get_user_movies(self, user_id: int) -> list:
        """
        Return a list of movies for a given user id
        :param user_id: int
        :return:
            A user's list of movies
        """
        return self.get_user(user_id)['movies']

    def get_user_movie(self, user_id: int, movie_id: int) -> dict | None:
        """
        Return a user's specific movie given movie_id
        :param user_id: int
        :param movie_id: int
        :return:
            a movie (dict) |
            None
        """
        movies = self.get_user_movies(user_id)
        if movies:
            for movie in movies:
                if movie['movie_id'] == movie_id:
                    return movie
        return None

    def add_user_movie(self, user_id: int, new_movie_info: dict) -> bool | None:
        """
        Add a movie to a user
        :param user_id: int
        :param new_movie_info: dict
        :return:
            True for success add (bool) |
            None
        """
        user = self.get_user(user_id)
        if user:
            new_movie_info.update({"movie_id":
                                       self._data_manager.generate_new_id(user['movies'],
                                                                          'movie_id')})
            user['movies'].append(new_movie_info)
            return self._data_manager.update_item(user)
        return None

    def update_user_movie(self, user_id: int, movie_id: int, updated_movie: dict):
        """
        Update a user movie info
        :param user_id: int
        :param movie_id: int
        :param updated_movie: dict
        :return:
            True for success update movie (bool) |
            None
        """
        user = self.get_user(user_id)

        if user:
            for movie in user['movies']:
                if movie['movie_id'] == movie_id:
                    movie.update(updated_movie)
            return self._data_manager.update_item(user)
        return None

    def delete_user_movie(self, user_id: int, movie_id: int) -> bool | None:
        """
        Delete a user movie
        :param user_id: int
        :param movie_id: int
        :return:
            True for success delete movie (bool) |
            None
        """
        user = self.get_user(user_id)
        movie = self.get_user_movie(user_id, movie_id)

        if user and movie:
            user['movies'].remove(movie)
            return self._data_manager.update_item(user)
        return None
