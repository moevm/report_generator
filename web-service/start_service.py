#!../venv/bin/python3.6
from app import app
import view

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
