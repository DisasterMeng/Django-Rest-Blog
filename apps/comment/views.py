import markdown
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.cookie_authentication import CookieAuthentication
from .models import Comment
from .serializers import CommentCreateSerializer
from utils.markdown_extension import DelInsExtension


class CommentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()
    authentication_classes = (CookieAuthentication,)

    def perform_create(self, serializer):
        parent_review = serializer.validated_data.get('parent')
        serializer.save(user=self.request.user, parent=parent_review)

    @action(methods=['get'],detail=False,url_path='md-to-html')
    def md_to_html(self,request,pk=None):
        content = request.query_params.get('content',"")
        md = markdown.Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite',DelInsExtension()])

        return Response(md.convert(content),status=status.HTTP_200_OK)

