# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-29 09:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_permission_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='icon',
        ),
    ]