from rest_framework import serializers

from .models import Live2d


class Live2dSerialize(serializers.ModelSerializer):

    class Meta:
        model = Live2d
        fields = ('name', 'file_model')
