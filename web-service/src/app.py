import os
from flask import Flask
DB_NAME = 'new_data_15'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VERY_SECRET_KEY'
app.config['MONGODB_SETTINGS'] = {
	'db': DB_NAME
}
app.secret_key = 'very_secret'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
