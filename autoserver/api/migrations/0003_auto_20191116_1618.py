# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-16 08:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191116_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memory',
            old_name='host',
            new_name='server',
        ),
    ]
