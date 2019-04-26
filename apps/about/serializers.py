import markdown
from markdown.inlinepatterns import SimpleTagPattern
from rest_framework import serializers

from .models import About

INS_RE = r"(\+\+)(.+?)(\+\+)"


class AboutSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = About
        fields = '__all__'

    def get_content(self, obj):
        md = markdown.Markdown(extensions=['utils.markdown_extension:ChangeCodeExtension',
                                           'pymdownx.extra', 'pymdownx.critic', 'pymdownx.tilde'])
        md.inlinePatterns.add('ins', SimpleTagPattern(INS_RE, 'ins'), '<not_strong')
        return md.convert(obj.content)
