# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-29 09:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_permission_icon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permission',
            old_name='url_title',
            new_name='reverse_name',
        ),
    ]