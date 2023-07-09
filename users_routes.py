"""
Users Blueprint routes page:
Implementing
list users
add user
routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort

from moviweb_app.data_manager.json_data_manager import JSONDataManager
from moviweb_app.data_manager.users import Users

users_bp = Blueprint('users', __name__)

FILEPATH = 'data/movies.json'
users_data_manager = Users(JSONDataManager(FILEPATH, 'user_id'))


@users_bp.route('/users', methods=['GET'])
def list_users():
    """
    Get a list of all users
    :return:
        - Response object containing a list of users
        - Bad request error message
    """
    users = users_data_manager.get_all_users()
    if users is None:
        abort(404)
    return render_template('users.html', users=users)


def get_error_messages(user_name: str) -> list:
    """
    Validates user inputs and
    return specific error messages
    based on user input error
    :param user_name: str
    :return:
        error messages (list)
    """
    error_messages = []
    if len(user_name) == 0:
        error_messages.append('User name cannot be empty')
    else:
        # check first letter is digit or special chars
        if not user_name[0].isalpha():
            error_messages.append('User name must start with letter')
    return error_messages


@users_bp.route('/add_user', methods=['GET', 'POST'])
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
        user_name = request.form.get('user_name', '')

        error_messages = get_error_messages(user_name)
        if len(error_messages) != 0:
            abort(400, error_messages)

        new_user = {"name": user_name,
                    "movies": []}

        if users_data_manager.add_user(new_user) is None:
            abort(400, ['Invalid user data'])
        return redirect(url_for('users.list_users'))

    return render_template('add_user.html')
