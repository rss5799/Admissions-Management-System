from flask import Flask, session, render_template, request, redirect
import os
import pyrebase

def create_app():
    app = Flask(__name__)
    config = {
    'apiKey': "AIzaSyDObAkxu03wa769hSlSaYkGb27Z1SJ95Fg",
    'authDomain': "admissionsmanagementsystem.firebaseapp.com",
    'projectId': "admissionsmanagementsystem",
    'storageBucket': "admissionsmanagementsystem.firebasestorage.app",
    'messagingSenderId': "178704031743",
    'appId': "1:178704031743:web:f0773e4dfa6702049711ca",
    'databaseURL' : '' 
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    
    
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