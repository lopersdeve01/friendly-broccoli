# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-03 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_remove_permission_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
