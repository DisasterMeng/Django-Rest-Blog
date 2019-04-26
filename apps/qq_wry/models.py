from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

from model_utils.models import TimeStampedModel
# Create your models here.


class QqWry(TimeStampedModel):
    qqwry_file = models.FileField('QqWry', upload_to=settings.UPLOAD_QQWRY_DIR, null=True, blank=True)

    def file_save(self, binary):
        self.qqwry_file.save('qqwry.dat', ContentFile(binary), save=True)

    class Meta:
        verbose_name = 'QqWry'
        verbose_name_plural = verbose_name
