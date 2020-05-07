#!./venv/bin/python3.6
import os
from app import app, ABS_PATH
import flask
from flask import url_for, redirect, jsonify

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.http import MediaFileUpload
import googleapiclient.discovery
from googleapiclient.discovery import build

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CREDENTIALS = 'credentials'
CLIENT_SECRETS_FILE = ABS_PATH.format("google/client_secrets.json")
TITLE = 'name'
NAME_OF_FILE = 'report.pdf'
TYPE = 'mimeType'
PDF = 'application/docx'
MEDIA_TYPE = 'text/pdf'
ID = 'id'
OFFLINE = 'offline'
STATE = 'state'
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'
PARENTS = 'parents'
GET_FOLDERS = "mimeType = 'application/vnd.google-apps.folder'"
FIELDS = "nextPageToken, files(id, name, parents, capabilities)"
FILES = 'files'


@app.route('/post_report_pdf/<id>')
def post_file_api_request(id=None):
    if CREDENTIALS not in flask.session:
        return flask.redirect(url_for('google_authorize'))
    credentials = google.oauth2.credentials.Credentials(
        **flask.session[CREDENTIALS])
    drive = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    if id is "0":
        file_metadata = {TITLE: app.config['filename_report'], TYPE: PDF}
    else:
        file_metadata = {TITLE: app.config['filename_report'], TYPE: PDF, PARENTS: [id]}
    print('GOOGLE DRIVE', app.config['filename_report'])
    media = MediaFileUpload(ABS_PATH.format(app.config['filename_report']), #ABS_PATH.format('report.pdf'),
                            mimetype=MEDIA_TYPE)
    file = drive.files().create(body=file_metadata,
                                media_body=media,
                                fields=ID).execute()

    flask.session[CREDENTIALS] = credentials_to_dict(credentials)

    return redirect(url_for('index'))


@app.route('/googleauthorize')
def google_authorize():
    if CREDENTIALS in flask.session:
        #return flask.redirect(url_for('post_file_api_request'))
        return redirect(url_for('index'))
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

    return redirect(url_for('index'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def get_list():
    if CREDENTIALS not in flask.session:
        return None
    credentials = google.oauth2.credentials.Credentials(
        **flask.session[CREDENTIALS])
    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    results = service.files().list(q=GET_FOLDERS,
                                   fields=FIELDS).execute()

    return results.get(FILES, [])
