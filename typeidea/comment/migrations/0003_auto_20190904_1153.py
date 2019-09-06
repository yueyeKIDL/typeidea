# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-04 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20190903_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, default='163@qq.com', max_length=254, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='website',
            field=models.URLField(default='www.baidu.com', verbose_name='网站'),
        ),
    ]