from rest_framework import viewsets, permissions

from .models import Music
from .serializers import MusicSerializer
# Create your views here.


class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

