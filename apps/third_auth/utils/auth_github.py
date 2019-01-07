import json
import urllib

from .auth_base import AuthBase


class AuthGithub(AuthBase):
    def get_auth_url(self):
        params = {
            'client_id': self.id,
            'response_type': 'code',
            'redirect_uri': self.redirect,
            'scope': 'user:email',
            'state': 1
        }
        url = 'https://github.com/login/oauth/authorize?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self, code):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.id,
            'client_secret': self.key,
            'code': code,
            'redirect_url': self.redirect
        }
        response = self.post('https://github.com/login/oauth/access_token', params)
        result = urllib.parse.parse_qs(response.text, True)
        self.access_token = result['access_token'][0]
        return self.access_token

        # github不需要获取openid，因此不需要get_open_id()方法

    def get_user_info(self):
        params = {'access_token': self.access_token}
        response = self.get('https://api.github.com/user', params)
        result = json.loads(response.text)
        self.openid = result.get('id', '')
        return result

    def get_email(self):
        params = {'access_token': self.access_token}
        response = self.get('https://api.github.com/user/emails', params)
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']
