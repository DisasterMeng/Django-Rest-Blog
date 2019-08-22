import os
from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel
# Create your models here.


def upload_music_path(instance, filename):
    return os.path.join(settings.UPLOAD_MUSIC_DIR, instance.name, filename)


class Music(TimeStampedModel):
    name = models.CharField('名称', max_length=100)
    artist = models.CharField('作者', max_length=100)
    url = models.FileField('music', upload_to=upload_music_path)
    cover = models.ImageField('300*300图片', upload_to=upload_music_path)
    lrc = models.FileField('lrc 歌词', upload_to=upload_music_path, null=True, blank=True)

    class Meta:
        verbose_name = 'music'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
