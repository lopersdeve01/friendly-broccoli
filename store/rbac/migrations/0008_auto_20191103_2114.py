# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-03 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0007_permission_url_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='roles',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
