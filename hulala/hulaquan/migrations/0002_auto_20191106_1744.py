# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-06 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hulaquan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='check',
            field=models.IntegerField(default=0, verbose_name='浏览数量'),
        ),
        migrations.AlterField(
            model_name='article',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=None, verbose_name='文章图片'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='zan',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
    ]
