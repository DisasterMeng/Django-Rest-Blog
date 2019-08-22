from rest_framework import viewsets
from rest_framework.response import Response

from .models import About
from .serializers import AboutSerializer


class AboutViewSet(viewsets.GenericViewSet):
    queryset = About.objects.all()

    @staticmethod
    def list(request, *args, **kwargs):
        about = About.objects.last()
        serializer = AboutSerializer(about)
        return Response(serializer.data)
