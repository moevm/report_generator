from flask import redirect, request
import requests
import os

client_id = os.environ.get('github_ci')
client_secret = os.environ.get('github_cs')


class Github:

    def __init__(self):
        self.headers = {'Accept': 'application/json'}
        self.code = None
        self.access_token = None
        self.is_active = False

    def set_code(self, code):
        self.code = code

    @property
    def is_authorized(self):
        return self.is_active

    def authorize(self):
        self.is_active = True
        return redirect("https://github.com/login/oauth/authorize?client_id={}&scope=user%20repo".format(client_id),
                        code=302)

    def is_valid_response(self, response):
        return 200 <= response.status_code < 300

    def get_access_token(self):
        resp = requests.post("https://github.com/login/oauth/access_token",
                             headers=self.headers,
                             data={'client_id': client_id,
                                   'client_secret': client_secret,
                                   'code': self.code})

        if self.is_valid_response(resp):
            response = resp.json()
            if 'error' not in response:
                self.access_token = response['access_token']
                return response['access_token']

    def get(self, path):
        if not self.access_token:
            self.access_token = self.get_access_token()

        params = {'access_token': self.access_token,
                  'client_secret': client_secret,
                  'scope': "user,repo",
                  'code': self.code}

        info = requests.get("https://api.github.com/{}".format(path),
                                 headers=self.headers,
                                 params=params)

        if self.is_valid_response(info):
            return info.json()
