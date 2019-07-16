from app import app
from main import main as create_word
from json_api import JsonApi as update_settings
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_security import current_user, login_required, login_user, logout_user
from admin_security import user_datastore
from models import User
from services.github_service import getGithub

app.config['was_new_user'] = True

FIRST_ADMIN = 'light5551'
FIRST_EMAIL_ADMIN = 'example@mail.ru'

link = ""
@app.route('/', methods=["GET", 'POST'])
@app.route('/home', methods=["GET", 'POST'])
def index():
    github = getGithub()
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
        repos = create_list_of_repo(github_data)

    return render_template("home.html", link=link, github=github_data, repositories=repos)


@app.route('/github_login')
def github_login():
    return getGithub().authorize()


@app.route('/log_out')
def logout():
    if current_user.is_authenticated:
        flash('You were successfully logged out', 'success')
        logout_user()
    return redirect(url_for('index'))


@app.route('/info')
def info():
    return jsonify(User.objects)


@app.before_first_request
def create_admin():
    user_datastore.find_or_create_role(name='admin')
    user_datastore.find_or_create_role(name='test_user')
    if not user_datastore.get_user(FIRST_EMAIL_ADMIN):
        app.config['was_new_user'] = False
        user_datastore.create_user(username=FIRST_ADMIN, email=FIRST_EMAIL_ADMIN)
        app.config['was_new_user'] = False
    user_datastore.add_role_to_user(FIRST_EMAIL_ADMIN, 'admin')


@app.route('/login/github/authorized')
def authorized():
    github = getGithub()
    github.set_code(request.args.get('code', None))
    github.is_active = True
    github_account = github.get('user')
    user = user_datastore.find_user(username=github_account['login'])
    if user:
        flash('You were successfully logged in, {}'.format(github_account['login']), 'success')
        if not user.avatar:
            user.avatar = github_account['avatar_url']
            app.config['was_new_user'] = False
            user.save()
        login_user(user)
    else:
        flash('Sorry, but you don\'t have access right', 'danger')
    return redirect(url_for('index'))


def create_list_of_repo(repo_data):
    if repo_data:
        repos = getGithub().get('users/{}/repos'.format(repo_data['login']))
        list_of_repo = []
        for repo in repos:
            list_of_repo.append({'url': repo['html_url'], 'name': repo['full_name']})
        return list_of_repo
    return []
