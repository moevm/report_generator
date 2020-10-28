from flask import render_template, redirect, url_for, request, jsonify, session, send_from_directory

import google.google_api
from app import app, ABS_PATH
from json_api import JsonApi as update_settings
from main import main as create_word

IS_NEW_USER = 'was_new_user'
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
    if request.method == POST:
        update_settings(dict(request.form))
        repo = request.form[REPO_NAME]
        wiki = request.form[WIKI_NAME]
        branch = request.form[BRANCH_NAME]
        session['link'] = create_word([repo, wiki, branch])
        return redirect(url_for(MAIN_PAGE))

    return render_template("home.html", link=session.get('link'), google=google.google_api.get_list())


@app.route('/send', methods=['GET'])
def send():
    return redirect(url_for('post_file_api_request'))


@app.route('/download', methods=[GET, POST])
def download_to_main_page():
    if request.method == POST:
        update_settings(dict(request.form))
        repo = request.form[REPO_NAME]
        wiki = request.form[WIKI_NAME]
        branch = request.form[BRANCH_NAME]
        try:
            path_report = create_word([repo, wiki, branch], need_push=False)
        except ValueError as e:
            return str(e), 402
        print(path_report)
    return ''


@app.route('/dw_report')
def dw_report():
    student = dict(request.args)['name'].replace(' ', '_')
    filename = app.config['filename_report']
    # if app.config['is_ok']:
    #     app.config['is_ok'] = False
    return send_from_directory(ABS_PATH[:-3], filename, as_attachment=True, cache_timeout=0, attachment_filename='{}.docx'.format(student))
    # return ''
