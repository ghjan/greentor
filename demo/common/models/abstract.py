#!/usr/bin/env python
# coding: utf-8

from django.db import models
from common import settings


class TimeModel(models.Model):
    """
    class: include create time and modify time
    """
    
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=u'创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name=u'修改时间')
    
    class Meta:
        abstract = True


class StateModel(models.Model):
    """
    class: base class including status code
    """
    state = models.IntegerField(choices=settings.STATE_CHOICES, default=settings.StateEnum.VALID,
                                db_index=True, verbose_name=u'状态码')

    class Meta:
        abstract = True


class NoModel(models.Model):
    '''
    class: 包含唯一编号的基础类
    '''
    no = models.CharField(max_length=128, unique=True, verbose_name=u'编号')

    class Meta:
        abstract = True


class NewNoModel(models.Model):
    '''
    class: 包含唯一编号的基础类
    '''
    no = models.CharField(max_length=32, unique=True, verbose_name=u'编号')

    class Meta:
        abstract = True