from django.http import HttpResponse

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from .models import Live2d, Live2dTextures
from .serializers import Live2dSerializer

from utils.uuid import md5
# Create your views here.


class Live2dViewSet(viewsets.ModelViewSet):
    queryset = Live2d.objects.all()
    serializer_class = Live2dSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    @action(methods=['get'], detail=False, url_path='textures')
    def live2d_img(self, request, pk=None):
        live_tag = None
        if 'live_tag' in request.session:
            live_tag = request.session.get('live_tag')
        live2d = Live2dTextures.objects.order_by('?')
        img = live2d.first()
        cur_md5 = md5(img.textures.read())
        if live_tag and live_tag == cur_md5:
            img = live2d.last()
            cur_md5 = md5(img.textures.read())
        request.session['live_tag'] = cur_md5
        return HttpResponse(img.textures, content_type='image/png')

    @action(methods=['get'], detail=False, url_path='name')
    def live2d_name(self, request, pk=None):
        name = request.query_params.get('name')
        live2d = Live2d.objects.get(name=name)
        serialize = Live2dSerializer(live2d, many=False, context={'request': request})
        return Response(serialize.data)
