import markdown
from markdown.inlinepatterns import SimpleTagPattern
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from comment.serializers import TreeCommentSerializer
from utils.pagination import StandardResultsSetPagination
from .models import Category, Blog, Tag
from .serializers import CategorySerializer, BlogSerializer, BlogListSerializer, BlogDetailSerializer, TagSerializer

INS_RE = r"(\+\+)(.+?)(\+\+)"


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.order_by('-id').all()
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogListSerializer
        elif self.action == 'retrieve':
            return BlogDetailSerializer
        else:
            return BlogSerializer

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.increase_views()
        return obj

    @action(methods=['get'], detail=True, serializer_class=TreeCommentSerializer, permission_classes=[])
    def comments(self, request, pk=None):
        """
        对应blog的评论
        """

        query = TreeCommentSerializer.setup_eager_loading(Blog.objects.all(),
                                                          prefetch_related=TreeCommentSerializer.PREFETCH_RELATED_FIELDS)
        blog = query.get(id=pk)
        comments = blog.comment.filter(parent=None)
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = TreeCommentSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = TreeCommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='md-to-html')
    def md_to_html(self, request, pk=None):
        content = request.query_params.get('content', '')
        md = markdown.Markdown(extensions=['utils.markdown_extension:ChangeCodeExtension',
                                           'pymdownx.extra', 'pymdownx.critic', 'pymdownx.tilde'])
        md.inlinePatterns.add('ins', SimpleTagPattern(INS_RE, 'ins'), '<not_strong')
        return Response(md.convert(content), status=status.HTTP_200_OK)
