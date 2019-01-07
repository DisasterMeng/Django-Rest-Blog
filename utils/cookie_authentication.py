from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


#  http://getblimp.github.io/django-rest-framework-jwt/#extending-jsonwebtokenauthentication


class CookieAuthentication(BaseJSONWebTokenAuthentication):

    def get_jwt_value(self, request):
        return request.COOKIES.get(api_settings.JWT_AUTH_HEADER_PREFIX.upper(), '')
