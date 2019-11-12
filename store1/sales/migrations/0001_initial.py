# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-22 08:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='校区')),
                ('address', models.CharField(blank=True, max_length=512, null=True, verbose_name='详细地址')),
            ],
            options={
                'verbose_name': '校区表',
                'verbose_name_plural': '校区表',
            },
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('LinuxL', 'Linux中高级'), ('PythonFullStack', 'Python高级全栈开发')], max_length=64, verbose_name='课程名称')),
                ('semester', models.IntegerField(verbose_name='学期')),
                ('price', models.IntegerField(default=10000, verbose_name='学费')),
                ('memo', models.CharField(blank=True, max_length=100, null=True, verbose_name='说明')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('graduate_date', models.DateField(blank=True, null=True, verbose_name='结业日期')),
                ('class_type', models.CharField(blank=True, choices=[('fulltime', '脱产班'), ('online', '网络班'), ('weekend', '周末班')], max_length=64, null=True, verbose_name='班级类型')),
                ('campuses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Campuses', verbose_name='校区')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qq', models.CharField(help_text='QQ号必须唯一', max_length=64, unique=True, verbose_name='QQ')),
                ('qq_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='QQ昵称')),
                ('name', models.CharField(blank=True, help_text='学员报名后，请改为真实姓名', max_length=32, null=True, verbose_name='姓名')),
                ('sex', models.CharField(blank=True, choices=[('male', '男性'), ('female', '女性')], default='male', max_length=16, null=True, verbose_name='性别')),
                ('birthday', models.DateField(blank=True, default=None, help_text='格式yyyy-mm-dd', null=True, verbose_name='出生日期')),
                ('phone', models.BigIntegerField(blank=True, null=True, verbose_name='手机号')),
                ('source', models.CharField(choices=[('qq', 'qq群'), ('referral', '内部转介绍'), ('website', '官方网站'), ('baidu_ads', '百度推广'), ('office_direct', '直接上门'), ('WoM', '口碑'), ('public_class', '公开课'), ('website_luffy', '路飞官网'), ('others', '其它')], default='qq', max_length=64, verbose_name='客户来源')),
                ('course', multiselectfield.db.fields.MultiSelectField(choices=[('LinuxL', 'Linux中高级'), ('PythonFullStack', 'Python高级全栈开发')], max_length=22, verbose_name='咨询课程')),
                ('class_type', models.CharField(choices=[('fulltime', '脱产班'), ('online', '网络班'), ('weekend', '周末班')], default='fulltime', max_length=64, verbose_name='班级类型')),
                ('customer_note', models.TextField(blank=True, null=True, verbose_name='客户备注')),
                ('status', models.CharField(choices=[('signed', '已报名'), ('unregistered', '未报名'), ('studying', '学习中'), ('paid_in_full', '学费已交齐')], default='unregistered', help_text='选择客户此时的状态', max_length=64, verbose_name='状态')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='咨询日期')),
                ('last_consult_date', models.DateField(auto_now_add=True, verbose_name='最后跟进日期')),
                ('next_date', models.DateField(blank=True, null=True, verbose_name='预计再次跟进时间')),
                ('deal_date', models.DateField(blank=True, null=True)),
                ('class_list', models.ManyToManyField(blank=True, to='sales.ClassList', verbose_name='已报班级')),
            ],
            options={
                'verbose_name': '客户信息表',
                'verbose_name_plural': '客户信息表',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=32)),
                ('telephone', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('depart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.Department')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='sales.UserInfo', verbose_name='销售'),
        ),
        migrations.AddField(
            model_name='customer',
            name='introduce_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.Customer', verbose_name='转介绍自学员'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to='sales.UserInfo', verbose_name='老师'),
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=set([('course', 'semester', 'campuses')]),
        ),
    ]