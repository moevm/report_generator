from app import app
from main import main as create_word
from json_api import JsonApi as update_settings
from flask import render_template, redirect, url_for, request
from flask_github import GitHub
from flask_security import current_user, login_required
from flask_bcrypt import Bcrypt
from admin_security import user_datastore

CLIENT_ID = '6bfefa93bab199af589e'
CLIENT_SECRET = '49c1cf2398a705a235a9411a2a8fa7f3d7c5e974'

app.config['GITHUB_CLIENT_ID'] = CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = CLIENT_SECRET
github = GitHub(app)
bcrypt = Bcrypt(app)


link = ""
@app.route('/', methods=["GET", 'POST'])
@app.route('/home', methods=["GET", 'POST'])
def index():
    global link
    if request.method == 'POST':
        update_settings(dict(request.form))
        repo = request.form['repo_name']
        wiki = request.form['wiki_name']
        branch = request.form['branch_name']
        link = create_word([repo, wiki, branch])
        return redirect(url_for("index"))

    return render_template("home.html", link=link)


@app.route('/me/')
@login_required
def me():
    return "You are logged in as :{} {}".format(current_user.username, current_user.github_access_token)


@app.before_first_request
def create_admin():
    user_datastore.find_or_create_role(name='admin')
    user_datastore.find_or_create_role(name='test_user')
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(username='admin', email='admin@example.com', password='password')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    if not user_datastore.get_user('test@example.com'):
        user_datastore.create_user(username='test_user', email='test@example.com', password='testpass')
    user_datastore.add_role_to_user('test@example.com', 'test_user')

