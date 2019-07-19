import os
from app import app
import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.http import MediaFileUpload
import googleapiclient.discovery

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRETS_FILE = "client_secrets.json"

SCOPES = ['https://www.googleapis.com/auth/drive.file']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'

#app = flask.Flask(__name__)



@app.route('/test')
def test_api_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    drive = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    file_metadata = {'title': 'report.pdf', 'mimeType': 'application/pdf'}
    media = MediaFileUpload('report.pdf',
                            mimetype='text/pdf')
    file = drive.files().insert(body=file_metadata,
                                media_body=media,
                                fields='id').execute()

    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('index'))  # flask.jsonify(**files)


@app.route('/googleauthorize')
def google_authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    flow.code_verifier = 'fdskfhjdshjdhghajdhgjhdfjgjfdgjhfjghfjhgfhfdhjssgjfdgsdfhghfdgjdfnjgajfd'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=None,
        state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    flow.code_verifier = 'fdskfhjdshjdhghajdhgjhdfjgjfdgjhfjghfjhgfhfdhjssgjfdgsdfhghfdgjdfnjgajfd'

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('test_api_request'))


@app.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return ('Credentials successfully revoked.' + print_index_table())
    else:
        return ('An error occurred.' + print_index_table())


#@app.route('/clear')
#def clear_credentials():
#    if 'credentials' in flask.session:
#        del flask.session['credentials']
#    return 'clear'


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}



