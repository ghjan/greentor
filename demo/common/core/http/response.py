#!/usr/bin/env python
#coding: utf-8
'''
Created on 2016年10月11日

@author: butter
'''

import ujson as json

from common.utils import crypto

from django.http import HttpResponse
from django.conf import settings

class JSONResponse(HttpResponse):
    """
    """
    
    def __init__(self, data=None, encrypt=False, error=None, *args, **kwargs):
        
        rsp = {'encrypt': int(encrypt),}
        
        if not error:
            rsp.update(settings.ERROR['SUCC'])
        else:
            rsp.update(error)
        
        if data != None:
            if encrypt:
                rsp['data'] = crypto.encrypto(json.dumps(data))
            else:
                rsp['data'] = data
        
        content = json.dumps(rsp)
        super(JSONResponse, self).__init__(content, content_type='application/json', *args, **kwargs)
