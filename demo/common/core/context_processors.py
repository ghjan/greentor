#coding:utf8
'''
Created on 2015-11-3

@author: butter
'''

from django.conf import settings


def static(request):
    """
    Adds static-related context variables to the context.

    """
    context_extras = {}
    context_extras['STATIC_URL'] = settings.STATIC_URL
    context_extras['PROJECT_VERSION'] = settings.PROJECT_VERSION
    return context_extras
