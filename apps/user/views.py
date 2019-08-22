from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import SimpleUserSerializer
from utils.cookie_authentication import CookieAuthentication


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = SimpleUserSerializer
    authentication_classes = (CookieAuthentication,)

    @action(methods=['get'], detail=False, url_path='my-info')
    def get_my_info(self, request, pk=None):
        """
        获取自己的信息
        :param request:
        :param pk:
        :return:
        """
        if request.user.is_authenticated:
            serializer = SimpleUserSerializer(request.user, context={'request': request})
            return Response(serializer.data)
