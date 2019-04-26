import os
from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel
# Create your models here.


def upload_motions_path(instance, filename):
    return os.path.join(settings.UPLOAD_LIVE2D_DIR, instance.name, 'motions', filename)


def upload_textures_path(instance, filename):
    return os.path.join(settings.UPLOAD_LIVE2D_DIR, instance.name, 'textures', filename)


def upload_path(instance, filename):
    return os.path.join(settings.UPLOAD_LIVE2D_DIR, instance.name, filename)


class Live2dAction(TimeStampedModel):
    name = models.CharField('Live2dAction Name', max_length=50, default='')
    motions = models.FileField('Live2dAction motions', upload_to=upload_motions_path)

    class Meta:
        verbose_name = 'live2dAction'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Live2dTextures(TimeStampedModel):
    name = models.CharField('Live2dTextures Name', max_length=50, default='')
    textures = models.ImageField('Live2dTextures  Clothes', upload_to=upload_textures_path)

    class Meta:
        verbose_name = 'live2dTextures'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Live2d(TimeStampedModel):
    name = models.CharField('Live2d Name', max_length=50, default='')
    file_model = models.FileField('Live2d model', upload_to=upload_path, blank=True, null=True)
    moc = models.FileField('Live2d moc', upload_to=upload_path)
    actions = models.ForeignKey(to=Live2dAction, on_delete=models.CASCADE)
    clothes = models.ForeignKey(to=Live2dTextures, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'live2d'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
