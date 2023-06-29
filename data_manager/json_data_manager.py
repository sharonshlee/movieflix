import json
from typing import List

from .data_manager_interface import DataManagerInterface


def validate_user_data(new_user: dict) -> bool:
    """
    Check if the the new user data is valid
    :param
        new_user: (dict)
    :return:
        True if 'name' and 'movies' fields are present
    """
    return 'name' in new_user and 'movies' in new_user


class JSONDataManager(DataManagerInterface):
    """
    A class for managing data
    to and from a JSON file
    """

    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return None
        except FileExistsError:
            return None

    def write_file(self, users):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(users, file)
        except FileNotFoundError:
            return None
        except FileExistsError:
            return None

    def get_all_users(self):
        """
        Return a list of all users
        :return:
            A list of dictionaries representing users
        """
        return self.read_file()

    def get_user_movies(self, user_id: int) -> List[dict] | None:
        """
        Return a list of movies for a given user
        :param user_id: int
        :return:
            A user's list of movies dict or
            None
        """
        users = self.read_file()

        if users is not None:
            for user in users:
                if user['user_id'] == user_id:
                    return user['movies']

        return None

    def update_user_movie(self, user_id, movies):
        users = self.read_file()

        if users is not None:
            for user in users:
                if user['user_id'] == user_id:
                    user['movies'] = movies
                    self.write_file(users)
                    return True
        return None

    def delete_user_movie(self, user_id: int, movie_id: int) -> None | bool:
        movies = self.get_user_movies(user_id)

        if movies is not None:
            for movie in movies:
                if movie['movie_id'] == movie_id:
                    movies.remove(movie)
                    return self.update_user_movie(user_id, movies)
        return None

    def get_new_user_id(self):
        """
        Return 1 if there is no data in the file
        otherwise, return the highest id plus 1
        :return:
        """
        users = self.read_file()
        if users:
            return max(user['id'] for user in users) + 1
        return 1

    def add_user(self, new_user):
        if validate_user_data():
            new_user.update({'id': self.get_new_user_id()})
            self.write_file(new_user)
        return None


