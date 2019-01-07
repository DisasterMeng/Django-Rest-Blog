from rest_framework import viewsets, permissions

from utils.pagination import StandardResultsSetPagination
from .models import Summary
from .serializers import SummarySerializer


class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
