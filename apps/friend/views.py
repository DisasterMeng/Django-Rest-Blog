from rest_framework import viewsets, permissions

from .models import Friend
from .serializers import FriendSerializer


class FriendViewSet(viewsets.ModelViewSet):

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
