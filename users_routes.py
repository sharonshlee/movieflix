"""
Users Blueprint routes page:
Implementing
list users
add user
routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort

from movieflix.data_manager.json_data_manager import JSONDataManager
from movieflix.data_manager.users import Users

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


def validate_user_input(user_info: dict) -> list:
    """
    Validates user inputs and
    return specific error messages
    based on user input error
    :param user_info: dict
    :return:
        error messages (list)
    """
    user_name = user_info['name']
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

        error_messages = validate_user_input({'name': user_name})
        if len(error_messages) != 0:
            abort(400, error_messages)

        new_user = {"name": user_name,
                    "movies": []}

        if users_data_manager.add_user(new_user) is None:
            abort(400, ['Invalid user data'])
        return redirect(url_for('users.list_users'))

    return render_template('add_user.html')


def get_user_info(user_id: int) -> dict:
    """
    Get updated user details
    from update_user.html form
    :param: user_id: int
    :return:
        updated user details (dict)
    """
    return {'user_id': user_id,
            'name': request.form.get('name', '')}


def get_updated_user_info(user_id: int) -> dict:
    """
    Get updated user info
    from user form
    :return:
        Updated user info (dict)
    """
    updated_user = get_user_info(user_id)
    error_messages = validate_user_input(updated_user)

    if len(error_messages) != 0:
        abort(400, error_messages)

    return updated_user


@users_bp.route('/users/<int:user_id>/update_user', methods=['GET', 'POST'])
def update_user(user_id: int):
    """
    Update a specific user info
    :param user_id: int
    :return:
        GET: Render update_user.html | User not found error message
        POST: Redirect to list users page | bad request error message
    """
    if request.method == 'POST':
        if users_data_manager.update_user(get_updated_user_info(user_id)) is None:
            abort(400, ['User not found'])
        return redirect(url_for('users.list_users'))

    user = users_data_manager.get_user(user_id)

    if user is None:
        abort(404)

    return render_template('update_user.html', user=user)


@users_bp.route('/users/<int:user_id>/delete_user')
def delete_user(user_id: int):
    """
    Delete a specific user given user_id
    :param user_id: int
    :return:
        redirect to list users page |
        user not found error message
    """
    if users_data_manager.delete_user(user_id) is None:
        abort(404)

    return redirect(url_for('users.list_users'))
