import uuid

from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from rest_framework import viewsets, status

from user.models import User
from third_auth.models import ThirdAuth
from third_auth.serializers import ThirdAuthSerializer
from third_auth.utils.auth_github import AuthGithub
from utils.jwt import generate_token, generate_response


class ThirdAuthViewSet(viewsets.GenericViewSet):
    serializer_class = ThirdAuthSerializer

    @action(methods=['get'], detail=False, url_path='github-third-url')
    def github_third_url(self, request, pk=None):
        """
        跳转github认证url
        :param request:
        :param pk:
        :return:
        """
        if 'current' in request.query_params:
            request.session['current'] = request.query_params.get('current')
        auth = AuthGithub(settings.GITHUB_APP_ID, settings.GITHUB_KEY, settings.GITHUB_CALLBACK_URL)
        url = auth.get_auth_url()
        return HttpResponseRedirect(url)

    @action(methods=['get'], detail=False, url_path='github-auth')
    def github_auth(self, request, pk=None):
        oauth, nickname, image_url, signature, sex, open_id, email, github_url = self.get_user_info()
        if oauth:
            user = oauth.user
            return self.custom_response(user)
        else:
            super_user = User.objects.filter(is_superuser=True).first()
            is_super = True if super_user.email == email else False
            user = User.objects.create(username=nickname, desc=signature,
                                       password=uuid.uuid1(), sex=sex,
                                       github=github_url, email=email, is_superuser=is_super)
            user.img_download(image_url, nickname)
            user.save()
            instance = ThirdAuth.objects.create(user=user, openid=open_id, type='1')
            instance.save()
            return self.custom_response(user)

    def get_user_info(self):
        """
        获取github信息
        """
        code = self.request.query_params['code']
        auth = AuthGithub(settings.GITHUB_APP_ID, settings.GITHUB_KEY, settings.GITHUB_CALLBACK_URL)
        auth.get_access_token(code)
        user_info = auth.get_user_info()
        email = user_info.get('email', '')
        github_url = user_info.get('html_url', '')
        nickname = user_info.get('login', '')
        image_url = user_info.get('avatar_url', '')
        open_id = str(auth.openid)
        signature = user_info.get('bio', '')
        if not signature:
            signature = "无个性签名"
        sex = '3'
        try:
            oauth = ThirdAuth.objects.get(openid=open_id, type='1')
        except BaseException as e:
            print(e)
            oauth = None
        return oauth, nickname, image_url, signature, sex, open_id, email, github_url

    def custom_response(self, user):
        if user is not None and user.is_active:
            token = generate_token(user)
            response = generate_response(token, user, self.request)
            return response




