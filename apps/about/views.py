from rest_framework import viewsets
from rest_framework.response import Response

from .models import About
from .serializers import AboutSerializer


class AboutViewSet(viewsets.GenericViewSet):
    queryset = About.objects.all()

    def list(self, request, *args, **kwargs):
        about = About.objects.all().first()
        serializer = AboutSerializer(about)
        return Response(serializer.data)
