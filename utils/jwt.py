from datetime import datetime

from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

# from apps.user.serializers import UserSimpleSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def jwt_response_payload_handler(token, user=None, request=None):
    """
      jwt 荷载处理
    :param token:
    :param user:
    :param request:
    :return:
    """
    # 这里会发送一个登录的信号
    user_logged_in.send(sender='', user=user, request=request)
    return {
        'token': token,
        # 'user': UserSimpleSerializer(user, context={'request': request}).data
    }


def generate_token(user):
    """
    生成token
    :param user:
    :return:
    """
    return jwt_encode_handler(jwt_payload_handler(user))


def generate_response(token, user, request):
    """
    生成response
    :param token:
    :param user:
    :param request:
    :return:
    """
    response_data = jwt_response_payload_handler(token, user, request)

    if request.session.get('current') is not None:
        response = HttpResponseRedirect(request.session.pop('current'))
    else:
        response = Response(response_data)

    expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
    response.set_cookie(api_settings.JWT_AUTH_HEADER_PREFIX.upper(), token, expires=expiration, httponly=True)

    return response


