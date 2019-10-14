from app import app
from main import main as create_word
from json_api import JsonApi as update_settings
from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_security import current_user, login_required, login_user, logout_user
from admin_security import get_datastore, create_admin
from models import User, IS_NEW_USER
from services.github_service import getGithub
import google.google_api

app.config[IS_NEW_USER] = True
MAIN_PAGE = 'index'
SUCCESS = 'success'
DANGER = 'danger'
WARNING = 'warning'
NO_ACCESS = 'Sorry, but you don\'t have access right'
SUCCESS_LOG_IN = 'You were successfully logged in, {}'
SUCCESS_LOG_OUT = 'You were successfully logged out'
ADMIN = 'admin'
NORMAL_USER = 'test_user'
LOGIN = 'login'
GET_REPOS = 'users/{}/repos'
USER = 'user'
CODE = 'code'
REPO_NAME = 'repo_name'
WIKI_NAME = 'wiki_name'
BRANCH_NAME = 'branch_name'
AVATAR = 'avatar_url'
URL = 'url'
HTML_URL = 'html_url'
NAME = 'name'
FULL_NAME = 'full_name'
POST = 'POST'
GET = 'GET'

FIRST_ADMIN = 'light5551'
FIRST_EMAIL_ADMIN = 'example@mail.ru'


@app.route('/', methods=["GET", 'POST'])
@app.route('/home', methods=["GET", 'POST'])
def index():
    github = getGithub()
    if request.method == POST:
        update_settings(dict(request.form))
        repo = request.form[REPO_NAME]
        wiki = request.form[WIKI_NAME]
        branch = request.form[BRANCH_NAME]
        session['link'] = create_word([repo, wiki, branch])
        return redirect(url_for(MAIN_PAGE))
    github_data = []
    repos = []

    if github.is_authorized:
        github_data = github.get(USER)
        repos = create_list_of_repo(github_data)

    return render_template("home.html", link=session.get('link'), google=google.google_api.get_list(),
                           github=github_data, repositories=repos)


@app.route('/github_login')
def github_login():
    return getGithub().authorize()


@app.route('/log_out')
def logout():
    if current_user.is_authenticated:
        flash(SUCCESS_LOG_OUT, SUCCESS)
        logout_user()
    return redirect(url_for(MAIN_PAGE))


@app.route('/info')
def info():
    return jsonify(User.objects)


@app.before_first_request
def first_request():
    create_admin()
    get_datastore().find_or_create_role(name=ADMIN)
    get_datastore().find_or_create_role(name=NORMAL_USER)
    if not get_datastore().get_user(FIRST_EMAIL_ADMIN):
        app.config[IS_NEW_USER] = False
        get_datastore().create_user(username=FIRST_ADMIN, email=FIRST_EMAIL_ADMIN)
        app.config[IS_NEW_USER] = False
    get_datastore().add_role_to_user(FIRST_EMAIL_ADMIN, ADMIN)


@app.route('/login/github/authorized')
def authorized():
    github = getGithub()
    github.set_code(request.args.get(CODE, None))
    github.is_active = True
    github_account = github.get(USER)
    user = get_datastore().find_user(username=github_account[LOGIN])
    if user:
        flash(SUCCESS_LOG_IN.format(github_account[LOGIN]), SUCCESS)
        if not user.avatar:
            user.avatar = github_account[AVATAR]
            app.config[IS_NEW_USER] = False
            user.save()
        login_user(user)
    else:
        flash(NO_ACCESS, DANGER)
    return redirect(url_for(MAIN_PAGE))


@app.route('/send', methods=['GET'])
def send():
    return redirect(url_for('post_file_api_request'))


def create_list_of_repo(repo_data):
    if repo_data:
        repos = getGithub().get(GET_REPOS.format(repo_data[LOGIN]))
        list_of_repo = []
        for repo in repos:
            list_of_repo.append({URL: repo[HTML_URL], NAME: repo[FULL_NAME]})
        return list_of_repo
    return []
