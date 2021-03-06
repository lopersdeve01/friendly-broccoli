# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-05 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标签')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.IntegerField(choices=[(1, '发布'), (2, '删除')], default=1, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='web.Tag', verbose_name='标签'),
        ),
    ]
