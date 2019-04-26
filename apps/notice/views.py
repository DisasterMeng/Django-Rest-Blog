from rest_framework import viewsets
from rest_framework.response import Response

from .models import Notice
from .serializers import NoticeSerializer
# Create your views here.


class NoticeViewSet(viewsets.GenericViewSet):
    queryset = Notice.objects.all()

    def list(self, request, *args, **kwargs):
        notice = Notice.objects.last()
        serializer = NoticeSerializer(notice)
        return Response(serializer.data)
