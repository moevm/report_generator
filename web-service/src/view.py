from app import app
from main import main as create_word
from json_api import JsonApi as update_settings
from flask import render_template, redirect, url_for, request, jsonify, g
from flask_github import GitHub

CLIENT_ID = '6bfefa93bab199af589e'
CLIENT_SECRET = '49c1cf2398a705a235a9411a2a8fa7f3d7c5e974'

app.config['GITHUB_CLIENT_ID'] = CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = CLIENT_SECRET
github = GitHub(app)

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
    list_of_repo = []
    #if github.authorized:
        #current_github = github.get('/user').json()
        #list_of_repo = create_list_of_repo()
    return render_template("home.html", link=link, github=current_github, repositories=list_of_repo)

@app.route('/login')
def login():
    return github.authorize(scope="user,repo,repo:status")

@github.access_token_getter
def token_getter():
    return g.token

@app.route('/login/github/authorized')
@github.authorized_handler
def user(acc):
    print(acc)
    g.token = acc

    if acc:
        gu = github.get('/user')
        k = github.get('/users/light5551/repos')
        return jsonify(k)
        #print(github.get('/user').json())
    #if github.get('/user'):
    #    return (jsonify(github.get('/user')))
    return 'fail'
    #return jsonify(github.get('/user'))

@app.route('/login/github/authorized')
def check():
    return 'ok'
'''
@app.route('/github', methods=["GET", 'POST'])
def github_login():
    if not github.authorized and request.method == 'GET':
        return redirect(url_for('github.login'))

    if github.authorized:
        account_info = github.get('/user')

        if account_info.ok:
            account_info_json = account_info.json()
            return 'Information about you!\n{}'.format(account_info_json)
    return 'OOPS'


@app.route('/login/github/authorized')
def auth_login():
    return redirect(url_for('index'))


def create_list_of_repo():
    if github.authorized:
        repo_data = github.get('/user')
        if repo_data.ok:
            repo_url = repo_data.json()['repos_url']
            repo = requests.get(repo_url).json()
            list_of_repo = []
            for i in repo:
                list_of_repo.append({'url': i['html_url'], 'name': i['full_name'] })
            return list_of_repo
    return []

'''
