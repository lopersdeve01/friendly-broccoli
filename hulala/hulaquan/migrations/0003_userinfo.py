# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-08 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hulaquan', '0002_auto_20191106_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('token', models.CharField(blank=True, max_length=64, null=True, verbose_name='token')),
            ],
        ),
    ]
