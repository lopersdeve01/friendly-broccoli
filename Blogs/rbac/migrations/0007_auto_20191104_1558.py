# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-04 07:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_auto_20191104_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admini',
            name='roles',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to='rbac.Role', verbose_name='职位'),
        ),
    ]
