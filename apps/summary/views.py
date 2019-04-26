from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from utils.pagination import StandardResultsSetPagination
from .models import Summary
from .serializers import SummarySerializer

from utils.uuid import md5


class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    @action(methods=['get'], detail=False, url_path='random')
    def random_summary(self, request, pk=None):
        sum_tag = None
        if 'sum_tag' in request.COOKIES:
            sum_tag = request.COOKIES['sum_tag']
        summary = Summary.objects.order_by('?')
        img = summary.first()
        cur_md5 = md5(img.image.read())
        if sum_tag and sum_tag == cur_md5:
            img = summary.last()
            cur_md5 = md5(img.image.read())
        res = HttpResponse(img.image, content_type='image/png')
        res.set_cookie('sum_tag', cur_md5)
        return res
