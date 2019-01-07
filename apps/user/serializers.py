from rest_framework import serializers

from .models import User


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('icon', 'id', 'username',)
