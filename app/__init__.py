from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager


db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
   
    secret_key = os.urandom(24)
    app.secret_key = os.environ.get("SECRET_KEY", secret_key)
    
    
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'index'
    login_manager.init_app(app)

    from .models.User import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #import and register routes

    from . import routes
    app.register_blueprint(routes.bp)

    return app