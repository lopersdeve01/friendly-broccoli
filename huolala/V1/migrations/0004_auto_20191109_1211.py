# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-09 04:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('V1', '0003_auto_20191109_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='imgs',
        ),
        migrations.RemoveField(
            model_name='img',
            name='articles',
        ),
        migrations.AddField(
            model_name='img',
            name='articles',
            field=models.ManyToManyField(to='V1.Article', verbose_name='所属文章'),
        ),
    ]