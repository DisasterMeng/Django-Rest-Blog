from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel

from comment.models import Comment
from summary.models import Summary


class Category(TimeStampedModel):
    name = models.CharField('名字', max_length=20)

    class Meta:
        verbose_name = '博客类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}--{}'.format(self.id, self.name)


class Tag(TimeStampedModel):
    name = models.CharField('tag名', max_length=20)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}--{}'.format(self.id, self.name)


class Blog(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField('标题', max_length=150)
    content = models.TextField('内容')
    page_view = models.PositiveIntegerField('浏览量', default=0)
    summary_img = models.ImageField('摘要图片', upload_to=settings.UPLOAD_SUMMARY_DIR, default='', null=True, blank=True)
    comment = GenericRelation(Comment, object_id_field='object_pk', content_type_field='content_type', verbose_name='评论')

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}--{}'.format(self.id, self.title)

    def increase_views(self):
        """
        浏览量加1
        """
        self.page_view += 1
        self.save(update_fields=['page_view'])

    def save(self, *args, **kwargs):
        """
        覆写save方法，设置摘要   通过信号应该也可以
        """

        if not self.summary_img:
            if Summary.objects.count() > 0:
                self.summary_img = Summary.objects.order_by('?').first().image

        super(Blog, self).save(*args, **kwargs)
