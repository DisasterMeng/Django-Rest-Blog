from django.db import models

from model_utils.models import TimeStampedModel
# Create your models here.


class Notice(TimeStampedModel):
    notice = models.CharField('通知', max_length=200)

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.notice
