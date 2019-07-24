import os
from flask import Flask
ABS_PATH = os.getcwd() + '/{}'
DB_NAME = 'database_of_rp'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VERY_SECRET_KEY'
app.config['MONGODB_SETTINGS'] = {
	'db': DB_NAME
}
app.config['SECURITY_PASSWORD_SALT'] = 'salt'

