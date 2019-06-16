from app import app
from main import main as create_word
from json_api import JsonApi as update_settings
from flask import render_template, redirect, url_for, request, jsonify, session
from flask_security import current_user, login_required
from flask_bcrypt import Bcrypt
from admin_security import user_datastore
from github_oauth import Github

CLIENT_ID = '6bfefa93bab199af589e'
CLIENT_SECRET = '49c1cf2398a705a235a9411a2a8fa7f3d7c5e974'

app.config['GITHUB_CLIENT_ID'] = CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = CLIENT_SECRET

github = Github()
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
    github_data = []
    repos = []

    if github.is_authorized:
        github_data = github.get('user')
        repos = create_list_of_repo()
    return render_template("home.html", link=link, github=github_data, repositories=repos)


@app.route('/me/')
@login_required
def me():
    return "You are logged in as :{} {}".format(current_user.username, current_user.github_access_token)


@app.route('/info')
@login_required
def info():
    return jsonify(github.get('user'))


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


@app.route('/github_login')
@login_required
def login():
    return github.authorize()


@app.route('/_logout')
@login_required
def logout():
    github.is_active = False
    return redirect('/logout')


@app.route('/login/github/authorized')
def authorized():
    github.set_code(request.args.get('code', None))
    github.is_active = True
    return redirect('/home')


def create_list_of_repo():
    repo_data = github.get('user')
    if repo_data:
        repo = github.get('users/{}/repos'.format(repo_data['login']))
        list_of_repo = []
        for i in repo:
            list_of_repo.append({'url': i['html_url'], 'name': i['full_name']})
        return list_of_repo
    return []
