# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-25 04:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_auto_20191025_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='icon',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='permission',
            name='menu',
            field=models.BooleanField(default=False),
        ),
    ]
