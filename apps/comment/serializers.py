from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db.models import Prefetch
from rest_framework import serializers

from blog.models import Blog
from user.models import User
from user.serializers import SimpleUserSerializer
from utils.mixins import EagerLoaderMixin
from .models import Comment


class FlatCommentSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    parent_user = serializers.SerializerMethodField()
    submit_date = serializers.SerializerMethodField()

    def get_submit_date(self, obj):
        return obj.submit_date.strftime('%Y-%m-%d')

    def get_review(self, obj):
        review = obj.content_object
        return {
            'id': review.id,
            'title': review.title,
        }

    def get_user(self, obj):
        user = User.objects.get(pk=obj.user.id)
        serializer = SimpleUserSerializer(user, many=False, context={'request': self.context['request']})
        return serializer.data

    def get_parent_user(self, obj):
        parent = obj.parent
        if not parent:
            return None
        parent_user = User.objects.get(pk=parent.user.id)
        serializer = SimpleUserSerializer(parent_user, many=False, context={'request': self.context['request']})
        return serializer.data

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'parent_user',
            'review',
            'submit_date',
            'comment',
        )


class TreeCommentSerializer(serializers.ModelSerializer, EagerLoaderMixin):
    descendants = FlatCommentSerializer(many=True)
    user = SimpleUserSerializer()
    submit_date = serializers.SerializerMethodField()
    # 前端使用
    is_add = serializers.SerializerMethodField()
    sub_content = serializers.SerializerMethodField()

    def get_submit_date(self, obj):
        return obj.submit_date.strftime('%Y-%m-%d')

    def get_is_add(self, obj):
        return False

    def get_sub_content(self, obj):
        return ''

    PREFETCH_RELATED_FIELDS = [
        Prefetch('comment', queryset=Comment.objects.order_by('-submit_date'))
    ]

    class Meta:
        model = Comment
        fields = (
            'id',
            'content_type',
            'object_pk',
            'comment',
            'submit_date',
            'user',
            'descendants',
            'descendants_count',
            'is_add',
            'sub_content',
            'user_agent',
            'ip_position'
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    """
       仅用于 reply 的创建
       """
    parent_user = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_parent_user(self, obj):
        parent = obj.parent
        if not parent:
            return None
        parent_user = User.objects.get(pk=parent.user.id)
        serializer = SimpleUserSerializer(parent_user, many=False, context={'request': self.context['request']})
        return serializer.data

    def get_user(self, obj):
        user = User.objects.get(pk=obj.user.id)
        serializer = SimpleUserSerializer(user, many=False, context={'request': self.context['request']})
        return serializer.data

    def create(self, validated_data):
        reivew_id = validated_data.get('object_pk')

        review_ctype = ContentType.objects.get_for_model(
            Blog.objects.get(id=int(reivew_id))
        )
        site = Site.objects.get_current()
        validated_data['site'] = site
        validated_data['content_type'] = review_ctype
        return super(CommentCreateSerializer, self).create(validated_data)

    class Meta:
        model = Comment
        fields = (
            'id',
            'object_pk',
            'comment',
            'parent',
            'submit_date',
            'ip_address',
            'is_public',
            'is_removed',
            'user',
            'parent_user',
            'user_agent',
            'ip_position'
        )
        read_only_fields = (
            'id',
            'submit_date',
            'ip_address',
            'is_public',
            'is_removed',
            'user_agent',
            'ip_position'
        )
