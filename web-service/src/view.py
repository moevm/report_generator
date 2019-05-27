from app import app
from main import main as create_word
from json_api import JsonApi as update_settings
from flask import render_template, redirect, url_for, request
from flask_dance.contrib.github import github

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

    current_github = ''
    if github.authorized:
        current_github = github.get('/user').json()
    return render_template("home.html", link=link, github=current_github)

@app.route('/github', methods=["GET", 'POST'])
def github_login():
    if not github.authorized and request.method == 'GET':
        return redirect(url_for('github.login'))

    if github.authorized:
        account_info = github.get('/user')

        if account_info.ok:
            account_info_json = account_info.json()
            return 'Your github name is {login}'.format(login=account_info_json['login'])
            #return render_template('sign.html', github_nick=account_info_json['login'],
			#image=account_info_json['avatar_url'])
    #return render_template('sign.html')
    return 'OOPS'



