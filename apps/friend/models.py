from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings


class Friend(TimeStampedModel):
    name = models.CharField('友人帐', max_length=50)
    desc = models.CharField('描述', max_length=200)
    image = models.ImageField('图片', upload_to=settings.UPLOAD_FRIEND_DIR, default=0)
    link = models.URLField('连接')

    class Meta:
        verbose_name = '友人帐'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}--{}'.format(self.id, self.name)
