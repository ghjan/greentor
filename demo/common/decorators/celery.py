#!/usr/bin/env python
# coding: utf-8
'''
Created on 2011-4-20

@author: butter
'''
from functools import wraps
import sys

from django.utils.decorators import available_attrs
try:
    from django.utils.log import getLogger
    logger = getLogger('django.request')
except:
    import logging
    logger = logging.getLogger('django.request')

def task_exception_handler(view_func):
    """
    对celery task异常处理的decorator
    """
    def wrapped_view(*args, **kwargs):
        
        try:
            return view_func(*args, **kwargs)
        except Exception:
            logger.error('Celery task got exception.',
                    exc_info=sys.exc_info(),
                    extra={
                        'status_code': 400,
                    }
                )
    
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
