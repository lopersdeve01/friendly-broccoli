# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-04 07:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admini',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('email', models.EmailField(max_length=64, verbose_name='邮箱')),
                ('telephone', models.IntegerField(max_length=11, verbose_name='电话号码')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='一级菜单名称')),
                ('weight', models.IntegerField(verbose_name='权重')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='二级菜单名称')),
                ('url', models.CharField(max_length=64, unique=True, verbose_name='路径')),
                ('url_name', models.CharField(max_length=64, unique=True, verbose_name='别名')),
                ('menus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='一级菜单')),
                ('parents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='父级菜单')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True, verbose_name='职位名称')),
                ('permissions', models.ManyToManyField(to='rbac.Permission', verbose_name='权限')),
            ],
        ),
    ]
