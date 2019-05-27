import os
from flask import Flask
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VERY_SECRET_KEY'
