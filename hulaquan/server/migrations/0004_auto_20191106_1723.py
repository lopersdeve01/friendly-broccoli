# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-06 09:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20191106_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='categorys',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='articles',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='users',
        ),
        migrations.RemoveField(
            model_name='img',
            name='articles',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Img',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
