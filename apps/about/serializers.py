import markdown
from rest_framework import serializers

from .models import About


class AboutSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = About
        fields = '__all__'

    def get_content(self, obj):
        md = markdown.Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
        return md.convert(obj.content)
