from rest_framework import serializers


class ThirdAuthSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
