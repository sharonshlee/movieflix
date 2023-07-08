"""
API routes for users movies app using Flask
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


if __name__ == "__main__":
    app.run(port=5002)
