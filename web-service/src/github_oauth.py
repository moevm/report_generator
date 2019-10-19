from flask import redirect, request
import requests

client_id = '6bfefa93bab199af589e'
client_secret = '49c1cf2398a705a235a9411a2a8fa7f3d7c5e974'


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
            print('VALID RESPONSE')
            print(response)
            print(self.code)
            if 'error' not in response:
                print('NOT ERROR')
                self.access_token = response['access_token']
                return response['access_token']

    def get(self, path):
        if not self.access_token:
            self.access_token = self.get_access_token()

        print('GET!!!!!!!!!!!!!!')
        #self.access_token = self.get_access_token()
        print(self.access_token)
        params = {'access_token': self.access_token,
                  'client_secret': client_secret,
                  'scope': "user,repo",
                  'code': self.code}

        info = requests.get("https://api.github.com/{}".format(path),
                                 headers=self.headers,
                                 params=params)

        if self.is_valid_response(info):
            return info.json()
