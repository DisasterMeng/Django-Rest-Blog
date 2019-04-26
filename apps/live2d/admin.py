from django.contrib import admin

from .models import Live2d, Live2dTextures, Live2dAction
# Register your models here.

admin.site.register(Live2d)
admin.site.register(Live2dAction)
admin.site.register(Live2dTextures)