"""
API routes for users movies app using Flask
"""

import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS

from data_manager.json_data_manager import JSONDataManager
from users_routes import users_bp
from movies_routes import movies_bp

FILEPATH = 'data_manager/movies.json'


app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(movies_bp)
CORS(app)

data_manager = JSONDataManager(FILEPATH)


@app.route('/')
def home():
    """
    Home page
    :return:
        render index.html page.
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5002)
