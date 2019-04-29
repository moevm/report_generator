from app import app
from main import main as create_word
from flask import render_template
from flask import request


@app.route('/', methods=["GET", 'POST'])
@app.route('/home', methods=["GET", 'POST'])
def index():
    if request.method == 'POST':
        for i in request.form:
            print(i)
        wiki = request.form['wiki']
        branch = request.form['branch']
        repo = request.form['repo']
        return render_template("home.html", link=create_word([repo, wiki, branch]))

    return render_template("home.html")
