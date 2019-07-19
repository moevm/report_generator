import os
from app import app
import flask
from flask import url_for, redirect

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.http import MediaFileUpload
import googleapiclient.discovery
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CREDENTIALS = 'credentials'
CLIENT_SECRETS_FILE = "client_secrets.json"
TITLE = 'title'
NAME_OF_FILE = 'report.pdf'
TYPE = 'mimeType'
PDF = 'application/pdf'
MEDIA_TYPE = 'text/pdf'
ID = 'id'
OFFLINE = 'offline'
STATE = 'state'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'


@app.route('/post_report_pdf')
def post_file_api_request():
    if CREDENTIALS not in flask.session:
        return flask.redirect(url_for('google_authorize'))
    credentials = google.oauth2.credentials.Credentials(
        **flask.session[CREDENTIALS])
    drive = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    file_metadata = {TITLE: NAME_OF_FILE, TYPE: PDF}
    media = MediaFileUpload('report.pdf',
                            mimetype=MEDIA_TYPE)
    file = drive.files().insert(body=file_metadata,
                                media_body=media,
                                fields=ID).execute()

    flask.session[CREDENTIALS] = credentials_to_dict(credentials)

    return redirect(url_for('index'))


@app.route('/googleauthorize')
def google_authorize():
    if CREDENTIALS in flask.session:
        return flask.redirect(url_for('post_file_api_request'))
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)
    flow.code_verifier = os.urandom(50)
    authorization_url, state = flow.authorization_url(
        access_type=OFFLINE,
        include_granted_scopes='true')

    flask.session[STATE] = state

    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session[STATE]

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=None, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    flow.code_verifier = os.urandom(50)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    flask.session[CREDENTIALS] = credentials_to_dict(credentials)

    return flask.redirect(url_for('post_file_api_request'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
