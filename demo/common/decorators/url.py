#!/usr/bin/env python
# coding: utf-8
'''
Created on 2011-4-20

@author: butter
'''
from functools import wraps

from django.utils.decorators import available_attrs

from common.utils.url import short_url_parse


def short_url_parse_wrap(arguments_setting):
     
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def wrapped_view(request, *args, **kwargs):
            if kwargs.has_key('arguments') and kwargs['arguments']:
                kwargs['arguments'], kwargs['query_dict'] = short_url_parse(kwargs['arguments'], arguments_setting)
            #===================================================================
            # else:
            #     kwargs['arguments'] = None
            #     kwargs['query_dict'] = {}
            #===================================================================
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
