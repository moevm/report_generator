from app import app
from main import main as create_word
from json_api import JsonApi as update_settings
from flask import render_template, redirect, url_for
from flask import request
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
