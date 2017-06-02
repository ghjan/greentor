# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-25 10:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myfarm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='link_key', to='myfarm.Category', verbose_name='\u94fe\u63a5id'),
        ),
        migrations.AddField(
            model_name='category',
            name='remark',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='\u5907\u6ce8'),
        ),
    ]
