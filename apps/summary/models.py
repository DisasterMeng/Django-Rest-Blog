from django.db import models

from django.conf import settings

from model_utils.models import TimeStampedModel


class Summary(TimeStampedModel):
    image = models.ImageField('图片', upload_to=settings.UPLOAD_SUMMARY_DIR)

    class Meta:
        verbose_name = '摘要图片'
        verbose_name_plural = verbose_name
