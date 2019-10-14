import os
from flask import Flask
DB_NAME = 'database_of_rp'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#  local deploy
#ABS_PATH = os.getcwd() + '/{}'
# docker deploy
ABS_PATH = "/var/www/report_generator/{}"

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MONGODB_SETTINGS'] = {
	'db': DB_NAME
}
app.config['SECURITY_PASSWORD_SALT'] = 'salt'

