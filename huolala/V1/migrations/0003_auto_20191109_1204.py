# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-09 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('V1', '0002_auto_20191109_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='url',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='', verbose_name='图片路径'),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='token'),
        ),
    ]
