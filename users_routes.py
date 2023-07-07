from flask import Blueprint, render_template, request, redirect, url_for

from data_manager.json_data_manager import JSONDataManager

users_bp = Blueprint('users', __name__)

FILEPATH = 'data_manager/movies.json'
data_manager = JSONDataManager(FILEPATH)


@users_bp.route('/users', methods=['GET'])
def list_users():
    """
    Get a list of all users
    :return:
        - Response object containing a list of users
        - Bad request error message
    """
    users = data_manager.get_all_users()

    if users is None:
        return users_bp.page_not_found('')

    return render_template('users.html', users=users)


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
        new_user = {"name": request.form.get('user_name'),
                    "movies": []}

        if data_manager.add_user(new_user) is None:
            return users_bp.bad_request_error('')
        return redirect(url_for('users.list_users'))

    return render_template('add_user.html')


@users_bp.errorhandler(400)
def bad_request_error(_error):
    """
    Handle 400, Bad Request Error
    returns:
        Bad request page, 400
    """
    return render_template('400.html'), 400


@users_bp.errorhandler(404)
def page_not_found(_error):
    """
    Handle 404, Not Found Error
    returns:
        Page Not Found page, 404
    """
    return render_template('404.html'), 404
