import os
from flask import Flask


TWITTER_BASE_URL = 'https://twitter.com/'
STATIC = 'static'
UPLOADED_FILES_PATH = os.path.join(os.getcwd(), STATIC)


def create_app():
    flask_app = Flask(__name__)
    flask_app.debug = True
    flask_app.secret_key = 'development'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = None
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    if not os.path.exists(UPLOADED_FILES_PATH):
        os.makedirs(UPLOADED_FILES_PATH)
    return flask_app
