from flask import Flask
from app import create_app
import pandas as pd
import webbrowser
import threading

app = create_app()

if __name__ == "__main__":
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=False)
