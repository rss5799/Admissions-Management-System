from app import create_app
import pandas as pd

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
