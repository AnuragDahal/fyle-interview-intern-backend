import os
from core.server import app  # Import your Flask app

if __name__ == "__main__":
    os.environ["FLASK_ENV"] = "development"  # Set the environment variable
    app.run(host="0.0.0.0")  # Run your Flask app