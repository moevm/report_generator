#!../venv/bin/python3.6
from app import app
from flask_dance.contrib.github import make_github_blueprint
import view

CLIENT_ID = '6bfefa93bab199af589e'
CLIENT_SECRET = '49c1cf2398a705a235a9411a2a8fa7f3d7c5e974'

github_blueprint = make_github_blueprint(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
app.register_blueprint(github_blueprint, url_prefix='/login')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
