"""
API routes for users movies web app using Flask
Using
Users Blueprint
Movies Blueprint
"""
from flask import Flask, render_template
from flask_cors import CORS

from users_routes import users_bp
from movies_routes import movies_bp

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(movies_bp)

CORS(app)


@app.route('/')
def home():
    """
    Home page
    :return:
        render index.html page.
    """
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(_error):
    """
    Handle 404, Not Found Error
    returns:
        Page Not Found page, 404
    """
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request_error(error):
    """
    Handle 400, Bad Request Error
    returns:
        Bad request page, 400
    """
    return render_template('400.html', errors=error.description), 400


@app.errorhandler(500)
def internal_server_error(_error):
    """
    Handle 500, Internal Server Error
    returns:
        Internal Server page, 500
    """
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(port=5002)
