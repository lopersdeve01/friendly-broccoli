# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-28 03:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_auto_20191028_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='weight',
            field=models.IntegerField(default=100),
        ),
    ]
