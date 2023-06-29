"""
API routes for users movies app using Flask
"""
from typing import Tuple

from flask import Flask, render_template, jsonify, Response, request, url_for, redirect
from data_manager.json_data_manager import JSONDataManager

FILEPATH = 'data_manager/movies.json'

app = Flask(__name__)

data_manager = JSONDataManager(FILEPATH)


@app.route('/')
def home():
    """
    Home page
    :return:
        render an index.html page.
    """
    return render_template('index.html')


@app.route('/users', methods=['GET'])
def list_users():
    """
    Get a list of all users
    :return:
        - Response object containing a list of users
        - Bad request error message
    """
    users = data_manager.get_all_users()

    if users is None:
        return not_found_error('Users')

    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
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
    user_movies = data_manager.get_user_movies(user_id)

    if user_movies is None:
        return not_found_error(f'User with id {user_id}')

    return render_template('user_movies.html',
                           user_id=user_id,
                           user_movies=user_movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Render add_user form
    for adding a new user
    :return:
        POST:
            Redirect to home page |
            Bad request error message
        GET:
            Render add_user.html page
    """
    if request.method == 'POST':
        new_user = request.get_json()

        if data_manager.add_user(new_user):
            return redirect(url_for('home'))
        else:
            return bad_request_error('')

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id: int):
    """
    Render add_movie form
    to add movie
    for a given user id
    :param user_id: int
    :return:
    """
    if request.method == 'POST':
        movie_info = {'name': request.form.get('name'),
                      'director': request.form.get('director'),
                      'year': int(request.form.get('year')),
                      'rating': float(request.form.get('rating'))
                      }
        data_manager.add_user_movie(user_id, movie_info)
        return redirect(url_for('get_user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>')
def update_movie(user_id, movie_id):
    """
    Render update_movie form
    to update a movie
    for a given user id
    :param user_id: int
    :param movie_id: int
    :return:
    """
    return render_template('update_movie.html')


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id: int, movie_id: int):
    """
    Delete a specific movie from a given user id
    :param user_id: int
    :param movie_id: int
    :return:
    """
    if data_manager.delete_user_movie(user_id, movie_id) is None:
        return not_found_error('Movie')

    return redirect(url_for('get_user_movies', user_id=user_id))


@app.errorhandler(400)
def bad_request_error(_error):
    return jsonify({"error": "Invalid user data."}), 400


@app.errorhandler(404)
def not_found_error(error) -> Tuple[Response, int]:
    """
    Handle 404, Not Found Error
    returns:
        User Not Found error message, 404 (Tuple[Response, int])
    """
    return jsonify({"error": f"{error} Not Found"}), 404


if __name__ == "__main__":
    app.run(port=5002)
