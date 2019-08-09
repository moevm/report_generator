from flask import Flask
import os
#  local deploy
#ABS_PATH = os.getcwd() + '/{}'
# docker deploy
ABS_PATH = "/var/www/report_generator/{}"

app = Flask(__name__)
app.secret_key = os.urandom(24)
