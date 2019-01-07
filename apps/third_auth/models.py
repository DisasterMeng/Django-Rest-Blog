from django.db import models
from model_utils.models import TimeStampedModel

from user.models import User

types = (
    ('1', 'github'),
    ('2', 'qq'),
    ('3', 'weibo'),)


class ThirdAuth(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    openid = models.CharField("openid", max_length=100, default='')
    type = models.CharField(max_length=1, choices=types)
