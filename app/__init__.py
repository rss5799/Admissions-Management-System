from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    secret_key = os.urandom(2500)
    app.secret_key = secret_key
    app.config['SECRET_KEY'] = secret_key

    #import and register routes
    from . import routes
    app.register_blueprint(routes.bp)

    # if we wanted to get students from firebase we would use this but we'll load from csv
    # from .models.student import load_students_from_firebase_into_array
    # load_students_from_firebase_into_array()

    return app