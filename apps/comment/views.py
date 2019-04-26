import markdown
from markdown.inlinepatterns import SimpleTagPattern
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks.qq_wry import Wry
from utils.cookie_authentication import CookieAuthentication
from .models import Comment
from .serializers import CommentCreateSerializer

INS_RE = r"(\+\+)(.+?)(\+\+)"
QQ_WRY = Wry()


class CommentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()
    authentication_classes = (CookieAuthentication,)

    def perform_create(self, serializer):
        if 'HTTP_X_FORWARDED_FOR' in self.request.META:
            ip_address = self.request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip_address = self.request.META['REMOTE_ADDR']
        parent_review = serializer.validated_data.get('parent')
        serializer.save(user=self.request.user, parent=parent_review,
                        user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                        ip_address=ip_address,
                        ip_position=QQ_WRY.ip_search(ip_address))

    @action(methods=['get'], detail=False, url_path='md-to-html')
    def md_to_html(self, request, pk=None):
        content = request.query_params.get('content', '')
        md = markdown.Markdown(extensions=['utils.markdown_extension:ChangeCodeExtension',
                                           'pymdownx.extra', 'pymdownx.critic', 'pymdownx.tilde'])
        md.inlinePatterns.add('ins', SimpleTagPattern(INS_RE, 'ins'), '<not_strong')
        return Response(md.convert(content), status=status.HTTP_200_OK)

