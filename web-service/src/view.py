from app import app
from main import main as create_word
from json_api import JsonApi as update_settings
from flask import render_template, redirect, url_for, session
from flask import request
import google.google_api


@app.route('/', methods=["GET", 'POST'])
@app.route('/home', methods=["GET", 'POST'])
def index():
    if request.method == 'POST':
        update_settings(dict(request.form))
        repo = request.form['repo_name']
        wiki = request.form['wiki_name']
        branch = request.form['branch_name']
        session['link'] = create_word([repo, wiki, branch])
        return redirect(url_for("index"))

    return render_template("home.html", link=session.get('link'), google=google.google_api.get_list())


@app.route('/send', methods=['GET'])
def send():
    return redirect(url_for('post_file_api_request'))

