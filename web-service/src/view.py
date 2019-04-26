from app import app
from main import main as create_word
from flask import render_template, redirect, url_for
from flask import request

link = ""
@app.route('/', methods=["GET", 'POST'])
@app.route('/home', methods=["GET", 'POST'])
def index():
    global link
    if request.method == 'POST':
        wiki = request.form['wiki']
        branch = request.form['branch']
        repo = request.form['repo']
        link = create_word([repo, wiki, branch])
        return redirect(url_for("index"))

    return render_template("home.html", link=link)