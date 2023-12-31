"""
Movies Blueprint routes page:
implementing
list user movies
add movie
update movie
delete movie
routes
"""
import requests
from flask import Blueprint, render_template, request, redirect, url_for, abort

from movieflix.data_manager.json_data_manager import JSONDataManager
from movieflix.data_manager.users import Users

movies_bp = Blueprint('movies', __name__)

FILEPATH = 'data/movies.json'
users_data_manager = Users(JSONDataManager(FILEPATH, 'user_id'))

API_KEY = 'Your_API_KEY'
BASE_URL_KEY = f'http://www.omdbapi.com/?apikey={API_KEY}'
IMDB_BASE_URL = 'https://www.imdb.com/title/'


@movies_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_movies(user_id: int):
    """
    Get user's movies list given user id
    :param
        user_id: int
    :return:
        Render to user_movies.html
            with user_id and
            list of users movies dictionaries
            arguments
        User not found error message
    """
    user = users_data_manager.get_user(user_id)
    user_movies = users_data_manager.get_user_movies(user_id)

    if user_movies is None or user is None:
        abort(404)

    return render_template('user_movies.html',
                           user=user,
                           user_movies=user_movies)


def fetch_movie_api_response(title: str) -> dict:
    """
    Fetch api response movie info
    given movie title
    :param title: str
    :return: movie info (dict)
    """
    response = requests.get(f'{BASE_URL_KEY}&t={title}', timeout=5)
    response.raise_for_status()  # check if there was an error with the request

    return response.json()


def get_error_messages(movie_info: dict) -> list:
    """
    Validates user inputs and
    return specific error messages
    based on user input error
    :param movie_info: dict
    :return:
        error messages (list)
    """
    movie_name = movie_info.get('name', '')
    director = movie_info.get('director', '')
    year = movie_info.get('year', '')
    rating = movie_info.get('rating', '')

    error_messages = []
    if len(movie_name) == 0:
        error_messages.append('Movie name cannot be empty')

    if len(movie_name) != 0 and not movie_name[0].isalpha():
        error_messages.append('Movie name must start with letter')

    if len(director) != 0 and not director[0].isalpha():
        error_messages.append('Director name must start with letter')

    if len(year) != 0:
        if not year.isdigit():
            error_messages.append('Year must be number')

        if year.isdigit() and len(year) != 4:
            error_messages.append('Year must be 4 digits')

    if len(rating) != 0:
        if not isfloat(rating):
            error_messages.append('Rating must be a number')
        elif not 1.0 <= float(rating) <= 10.0:
            error_messages.append('Rating must be between 1.0 - 10.0')

    return error_messages


def format_movie_info(response: dict, movie_name: str) -> dict:
    """
    Format movie info
    :param response: dict
    :param movie_name: str
    :return:
        movie info (dict)
    """
    return {'name': response.get('Title', movie_name),
            'director': response.get('Director', ''),
            'year': int(response.get('Year', '0000')[:4]),
            'rating': float(response.get('imdbRating', 0.0)),
            'poster': response.get('Poster', ''),
            'website': IMDB_BASE_URL + response.get('imdbID', '')
            }


def get_empty_info(movie_name: str) -> dict:
    """
    Return empty movie info
    :param movie_name: str
    :return:
        empty movie info (dict)
    """
    return {'name': movie_name,
            'director': '',
            'year': 0,
            'rating': 0.0,
            'poster': '',
            'website': ''
            }


def get_new_movie_info() -> dict:
    """
    Get new movie info:
    name from add movie form,
    other movie details from OMDb API
    :return:
        New movie info from OMDb API (dict) |
        New movie name from add movie form (dict)
    """
    movie_name = request.form.get('name', '')

    error_messages = get_error_messages({'name': movie_name})
    if error_messages:
        abort(400, error_messages)

    try:
        response = fetch_movie_api_response(movie_name)
        return format_movie_info(response, movie_name)

    except (requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException):
        print("Request error. "
              "Check your internet connection "
              "and make sure the website is accessible.")
        return get_empty_info(movie_name)


@movies_bp.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id: int):
    """
    Render add_movie form to add movie
    for a given user id
    Redirect to user_movies page
    after adding a new user
    :param user_id: int
    :return:
        GET: render add_movie page
        POST:
            redirect to user_movies page |
            user not found error message
    """
    user = users_data_manager.get_user(user_id)
    if user is None:
        abort(404)

    if request.method == 'POST':
        if users_data_manager.add_user_movie(user_id, get_new_movie_info()) is None:
            abort(404)
        return redirect(url_for('movies.get_user_movies', user_id=user_id))
    return render_template('add_movie.html', user=user)


def isfloat(number: str) -> bool:
    """
    Check if the given number is float type
    :param number:
    :return:
        True or False (bool)
    """
    try:
        float(number)
        return True
    except ValueError:
        return False


def get_movie_info_from_user() -> dict:
    """
    Get updated movie details
    from update_movie.html form
    :return:
        updated movie details (dict)
    """
    return {'name': request.form.get('name', ''),
            'director': request.form.get('director', ''),
            'year': request.form.get('year', 0),
            'rating': request.form.get('rating', 0.0)
            }


def get_updated_movie_info() -> dict:
    """
    Get updated movie info
    from user form
    :return:
        Updated movie info (dict)
    """
    updated_movie_info = get_movie_info_from_user()
    error_messages = get_error_messages(updated_movie_info)

    if len(error_messages) != 0:
        abort(400, error_messages)

    year = updated_movie_info['year']
    if len(year) == 0:
        year = 0

    rating = updated_movie_info['rating']
    if len(rating) == 0:
        rating = 0.0

    return {'name': updated_movie_info['name'],
            'director': updated_movie_info['director'],
            'year': int(year),
            'rating': float(rating)
            }


@movies_bp.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id: int, movie_id: int):
    """
    -Render update_movie form
    to update a movie
    for a given user id
    -Redirect to user_movies page
    after update
    :param user_id: int
    :param movie_id: int
    :return:
        GET: render update_movie.html | movie not found error message
        POST: redirect to user_movies page | bad request error message
    """

    if request.method == 'POST':
        if users_data_manager.update_user_movie(user_id,
                                                movie_id,
                                                get_updated_movie_info()) is None:
            abort(400, ['No such movie'])
        return redirect(url_for('movies.get_user_movies', user_id=user_id))

    user = users_data_manager.get_user(user_id)
    movie = users_data_manager.get_user_movie(user_id, movie_id)

    if movie is None or user is None:
        abort(404)
    return render_template('update_movie.html', user=user, movie=movie)


@movies_bp.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id: int, movie_id: int):
    """
    Delete a specific movie from a given user id
    :param user_id: int
    :param movie_id: int
    :return:
        redirect to user_movies page |
        movie not found error message
    """
    if users_data_manager.delete_user_movie(user_id, movie_id) is None:
        abort(404)

    return redirect(url_for('movies.get_user_movies', user_id=user_id))
