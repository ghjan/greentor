# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-25 11:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myfarm', '0002_auto_20170525_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='no',
        ),
    ]
