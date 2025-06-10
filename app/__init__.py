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

    return app