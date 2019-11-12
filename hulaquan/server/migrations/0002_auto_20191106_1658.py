# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-06 08:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='summary',
        ),
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.AddField(
            model_name='article',
            name='categorys',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='server.Category', to_field='cid', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='category',
            name='cid',
            field=models.IntegerField(default=0, unique=True, verbose_name='分类值'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='articles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='server.Article', verbose_name='所属文章'),
        ),
        migrations.RemoveField(
            model_name='img',
            name='articles',
        ),
        migrations.AddField(
            model_name='img',
            name='articles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='server.Article', verbose_name='所属文章'),
        ),
        migrations.AlterField(
            model_name='img',
            name='url',
            field=models.ImageField(max_length=255, upload_to='', verbose_name='图片路径'),
        ),
    ]
