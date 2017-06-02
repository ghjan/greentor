#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author magic
"""

import time
import copy
from common import settings
from common.utils import crypto
import functools
import logging
import ujson as json
from django.http import HttpResponse
django_log = logging.getLogger('django')


def verify_request(func):
    """
    Client post request params and sign verify.
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        crypto.Init()
        rsp_data = copy.copy(settings.ERROR['SUCC'])
        if request.method == 'POST':
            params = copy.deepcopy(request.POST)
        elif request.method == 'GET':
            params = copy.deepcopy(request.GET)
        elif request.method == "FILES":
            params = copy.deepcopy(request.FILES)
        else:
            params = copy.deepcopy(request.REQUEST)

        try:
            sign = str(params.get('sign'))
            timestamp = params.get('timestamp')
            params.pop('sign')
        except AttributeError:
            rsp_data = copy.copy(settings.ERROR['ERROR'])
            return HttpResponse(json.dumps(rsp_data), content_type='application/json')

        if crypto.SignDict(settings.REAL_CRYPTO_KEY, params) != sign:
            rsp_data = copy.copy(settings.ERROR['SIGN_ERROR'])
            return HttpResponse(json.dumps(rsp_data), content_type='application/json')
        try:
            if verify_timestamp(timestamp) and crypto.SignDict(settings.REAL_CRYPTO_KEY, params) == sign:
                valid = True
            else:
                valid = False
                rsp_data = copy.copy(settings.ERROR['TIME_ERROR'])
        except Exception as e:
            logging.error(e)
            valid = False
            rsp_data = copy.copy(settings.ERROR['ERROR'])

        if valid:
            return func(request, *args, **kwargs)
        else:
            return HttpResponse(json.dumps(rsp_data), content_type='application/json')

    return wrapper


def verify_timestamp(timestamp, term=180, deviation=180):
    """
    verify current time and deviation
    :param timestamp: client timestamp
    :param term:
    :param deviation: time diff
    :return:
    """
    cur_timestamp = int(time.time())
    timestamp = int(timestamp)

    if abs(cur_timestamp - timestamp) <= (term + deviation):
        return True

    else:
        return False

