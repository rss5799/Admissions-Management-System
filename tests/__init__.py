import os
import sys
from flask import Flask

def create_app():
    """Factory function to create and return a Flask app instance."""

    # detect if running from a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))

    template_folder = os.path.join(base_path, 'templates')
    static_folder = os.path.join(base_path, 'static')

    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder
    )

    # Import routes and register them with app
    from app import routes

    return app
