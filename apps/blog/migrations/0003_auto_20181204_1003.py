# Generated by Django 2.1.3 on 2018-12-04 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20181201_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='summary_img',
            field=models.ImageField(blank=True, default='', null=True, upload_to='static/images/summary', verbose_name='摘要图片'),
        ),
    ]
