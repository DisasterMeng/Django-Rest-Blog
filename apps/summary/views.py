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
        if 'sum_tag' in request.session:
            sum_tag = request.session.get('sum_tag')
        summary = Summary.objects.order_by('?')
        img = summary.first()
        cur_md5 = md5(img.image.read())
        if sum_tag and sum_tag == cur_md5:
            img = summary.last()
            cur_md5 = md5(img.image.read())
        request.session['sum_tag'] = cur_md5
        return HttpResponse(img.image, content_type='image/png')
