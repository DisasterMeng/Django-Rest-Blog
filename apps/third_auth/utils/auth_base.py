import requests


class AuthBase(object):
    # 认证的基类
    def __init__(self, app_id, key, redirect):
        self.id = app_id
        self.key = key
        self.redirect = redirect

    @staticmethod
    def get(url, data):
        return requests.get(url, params=data)

    @staticmethod
    def post(url, data):
        return requests.post(url, json=data)

    def get_auth_code(self):
        pass

    def get_access_token(self, code):
        pass

    def get_open_id(self):
        pass

    def get_user_info(self):
        pass

    def get_email(self):
        pass
