import requests
from flask import Blueprint, render_template, request, redirect, url_for
from data_manager.json_data_manager import JSONDataManager

movies_bp = Blueprint('movies', __name__)

FILEPATH = 'data_manager/movies.json'
data_manager = JSONDataManager(FILEPATH)

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
    user = data_manager.get_user(user_id)
    user_movies = data_manager.get_user_movies(user_id)

    if user_movies is None or user is None:
        return page_not_found('')

    return render_template('user_movies.html',
                           user=user,
                           user_movies=user_movies)


def fetch_movie_api_response(title: str) -> dict:
    """
    Fetch api response movie info
    given movie title
    :param title: str
    :return: movie info (json)
    """
    response = requests.get(f'{BASE_URL_KEY}&t={title}', timeout=5)
    response.raise_for_status()  # check if there was an error with the request

    return response.json()


def get_new_movie_info() -> dict:
    """
    Get new movie info:
    name from add movie form,
    other movie details from OMDb API
    :return:
        New movie info from OMDb API (dict) |
        New movie name from add movie form (dict)
    """
    try:
        response = fetch_movie_api_response(request.form.get('name'))
        return {'name': response.get('Title', request.form.get('name')),
                'director': response.get('Director', ''),
                'year': int(response.get('Year', 0)),
                'rating': float(response.get('imdbRating', 0.0)),
                'poster': response.get('Poster', ''),
                'website': IMDB_BASE_URL + response.get('imdbID', '')
                }
    except (requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException):
        print("Request error. "
              "Check your internet connection "
              "and make sure the website is accessible.")
        return {'name': request.form.get('name'),
                'director': '',
                'year': 0,
                'rating': 0.0,
                'poster': '',
                'website': ''
                }


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
    user = data_manager.get_user(user_id)

    if request.method == 'POST':
        if data_manager.add_user_movie(user_id, get_new_movie_info()) is None:
            return page_not_found('')
        return redirect(url_for('movies.get_user_movies', user_id=user_id))
    return render_template('add_movie.html', user=user)


def get_updated_movie_info() -> dict:
    """
    Get updated movie info
    from user form
    :return:
        Updated movie info (dict)
    """
    return {'name': request.form.get('name', ''),
            'director': request.form.get('director', ''),
            'year': int(request.form.get('year', 0)),
            'rating': float(request.form.get('rating', 0.0))
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
        if data_manager.update_user_movie(user_id, movie_id, get_updated_movie_info()) is None:
            return bad_request_error('')
        return redirect(url_for('movies.get_user_movies', user_id=user_id))

    user = data_manager.get_user(user_id)
    movie = data_manager.get_user_movie(user_id, movie_id)

    if movie is None or user is None:
        return page_not_found('')
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
    if data_manager.delete_user_movie(user_id, movie_id) is None:
        return page_not_found('')

    return redirect(url_for('movies.get_user_movies', user_id=user_id))


@movies_bp.errorhandler(400)
def bad_request_error(_error):
    """
    Handle 400, Bad Request Error
    returns:
        Bad request page, 400
    """
    return render_template('400.html'), 400


@movies_bp.errorhandler(404)
def page_not_found(_error):
    """
    Handle 404, Not Found Error
    returns:
        Page Not Found page, 404
    """
    return render_template('404.html'), 404


@movies_bp.errorhandler(500)
def page_not_found(_error):
    """
    Handle 500, Internal Server Error
    returns:
        Internal Server page, 500
    """
    return render_template('500.html'), 500
