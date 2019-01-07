
from rest_framework import serializers


class ThirdAuthSerializer(serializers.Serializer):

    token = serializers.CharField()