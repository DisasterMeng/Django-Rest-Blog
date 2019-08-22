from django.db import models
from model_utils.models import TimeStampedModel


class About(TimeStampedModel):
    content = models.TextField('内容')

    class Meta:
        verbose_name = '关于'
        verbose_name_plural = verbose_name
