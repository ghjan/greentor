# encoding: utf-8
'''
Created on 2017-4-1
@author: leo.liu
'''
import copy
import ujson as json

from functools import wraps

from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import available_attrs


def require_fuwo_server(view_func):
    '''
    function : 服务器判断
               要求服务器必须是指定的内网服务器访问
    @param view_func:
    @return:
    '''
    def wrapped_view(request,*args, **kwargs):
        # 开发环境跳过检查
        if settings.DEBUG:
            return view_func(request,*args,**kwargs)
        
        request_ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
        fuwo_servers = getattr(settings, 'FUWO_SERVER_IPS') if hasattr(settings, 'FUWO_SERVER_IPS') else ()
        
        if request_ip and (request_ip in fuwo_servers):
            return view_func(request,*args,**kwargs)
        else:
            rsp_data = copy.copy(settings.ERROR['FORBIDDEN'])
            return HttpResponse(json.dumps(rsp_data), mimetype="application/json")
    
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
