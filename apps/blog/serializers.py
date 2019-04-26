import markdown
from markdown.inlinepatterns import SimpleTagPattern

from django.utils.html import strip_tags
from rest_framework import serializers

from .models import Blog, Category, Tag

INS_RE = r"(\+\+)(.+?)(\+\+)"


class CategorySerializer(serializers.ModelSerializer):
    blogs = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_blogs(self, obj):
        serializer = BlogSimpleSerializer(obj.blog_set.all(), many=True)
        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    blogs = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'blogs')

    def get_blogs(self, obj):
        serializer = BlogSimpleSerializer(obj.blog_set.all(), many=True)
        return serializer.data


class TagSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class BlogSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title')


class BlogDetailSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    next_blog = serializers.SerializerMethodField()
    pre_blog = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = "__all__"

    def get_content(self, obj):
        md = markdown.Markdown(extensions=['utils.markdown_extension:ChangeCodeExtension',
                                           'pymdownx.extra', 'pymdownx.critic', 'pymdownx.tilde'])
        md.inlinePatterns.add('ins', SimpleTagPattern(INS_RE, 'ins'), '<not_strong')
        return md.convert(obj.content)

    def get_created(self, obj):
        return obj.created.strftime('%Y-%m-%d')

    def get_category(self, obj):
        return obj.category.name

    def get_tags(self, obj):
        serializer = TagSimpleSerializer(obj.tags, many=True)
        return serializer.data

    def get_pre_blog(self, obj):
        blogs = Blog.objects.order_by('-id')
        pre_blog = blogs.filter(id__lt=obj.id)
        if pre_blog.count() > 0:
            return {
                'title': pre_blog[0].title,
                'id': pre_blog[0].id
            }
        else:
            return None

    def get_next_blog(self, obj):
        blogs = Blog.objects.order_by('-id')
        next_blog = blogs.filter(id__gt=obj.id).order_by('id')
        if next_blog.count() > 0:
            return {
                'title': next_blog[0].title,
                'id': next_blog[0].id
            }
        else:
            return None


class BlogListSerializer(serializers.ModelSerializer):
    desc = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ('id', 'created', 'desc', 'title', 'category', 'page_view', 'summary_img', 'tags')

    def get_desc(self, obj):
        md = markdown.Markdown(extensions=['utils.markdown_extension:ChangeCodeExtension',
                                           'pymdownx.extra', 'pymdownx.critic', 'pymdownx.tilde'])
        md.inlinePatterns.add('ins', SimpleTagPattern(INS_RE, 'ins'), '<not_strong')
        desc = strip_tags(md.convert(obj.content))[:54]
        return '{}...'.format(desc)

    def get_created(self, obj):
        return obj.created.strftime('%Y-%m-%d')

    def get_category(self, obj):
        return obj.category.name

    def get_tags(self, obj):
        serializer = TagSimpleSerializer(obj.tags, many=True)
        return serializer.data
