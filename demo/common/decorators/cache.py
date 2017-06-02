#!/usr/bin/env python
# coding: utf-8
'''
Created on 2011-4-20

@author: butter
'''
from functools import wraps
import hashlib

from django.core.cache import cache
from django.http import HttpResponse
from django.utils.decorators import available_attrs

from common import settings

def cache_page_enhanced(timeout=24*60*60, **gkwargs):
    '''
    增强版本
    timeount - 页面缓存超时时间,单位秒
    only_paths - 一个 url path的list，如果存在这个参数，则仅当request.path在其中时，缓存。
    '''
    def wrapper(view_func):
        def wrapped_view(request, *args, **kwargs):
            
            # 如果debug模式下，不做cache
            if settings.DEBUG:
                return view_func(request, *args, **kwargs)
            
            # POST请求不做cache
            if request.method =='POST':
                return view_func(request, *args, **kwargs)
            
            # 如果带有get参数，也不做cache
            if len(request.GET) > 0:
                return view_func(request, *args, **kwargs)
            
            if gkwargs.has_key('only_paths') and (request.path not in gkwargs['only_paths']):
                return view_func(request, *args, **kwargs)
            
            request_path = request.path
            if request.path == '/':
                request_path = ''
            cache_key = '%s.%s%s'%(settings.CACHE_PAGE_KEY_PREFIX, request.META['HTTP_HOST'], request_path)
            
            view_cache = cache.get(cache_key)
            # 默认有缓存,不再进行html压缩
            request._hit_htmlmin = False
            if view_cache is None:
                # 无缓存,进行html压缩
                request._hit_htmlmin = True
                template_response = view_func(request, *args, **kwargs)
                
                # 对status_code不等于200的response直接返回
                if template_response.status_code != 200:
                    return template_response
                
                view_cache = template_response.render()
                cache.set(cache_key, view_cache, timeout=timeout)
            
            rsp = HttpResponse(view_cache)
            
            return rsp
        return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
    return wrapper

def delete_cache_page_enhanced(urls):
    u'''
    function - 删除cache_page
    
    urls - 删除的page 缓存 url,是个列表
    '''
    if not urls:
        return 0
    
    cache_keys = []
    for url in urls:
        cache_key = '%s.%s'%(settings.CACHE_PAGE_KEY_PREFIX, url)
        cache_keys.append(cache_key)
    
    return cache.delete_many(cache_keys)

def page_cache(timeout, keyprefix=None, only_path=None, ignore_get=False):
    def wrapper(view_func):
        def wrapped_view(request, *args, **kwargs):
            
            #===================================================================
            # # 如果debug模式下，不做page_cache
            # if settings.DEBUG:
            #    return view_func(request, *args, **kwargs)
            #===================================================================
            
            path = request.path
            if only_path and only_path != path:
                return view_func(request, *args, **kwargs)
            
            if len(request.GET) > 0 and ignore_get == False:
                return view_func(request, *args, **kwargs)
            
            # 生成缓存的key
            key_prefix = keyprefix or getattr(settings, 'CACHE_MIDDLEWARE_KEY_PREFIX', None)
            key_prefix = key_prefix or 'default'
            cache_key = settings.COMMON_PAGE_CACHE_KEY % (key_prefix, (hashlib.md5(path)).hexdigest())
            # 获取缓存的html
            view_cache = cache.get(cache_key)
            # 默认有缓存,不再进行html压缩
            request._hit_htmlmin = False
            if view_cache is None:
                # 无缓存,进行html压缩
                request._hit_htmlmin = True
                # 取view的response
                template_response = view_func(request, *args, **kwargs)
                view_cache = template_response.render()
                cache.set(cache_key, view_cache, timeout=timeout)
            
            response = HttpResponse(view_cache)
            #===================================================================
            # # 这里不能做页面缓存（用户访问会有可能不经过服务器之间读取浏览器缓存）
            # response['Cache-Control'] = 'max-age=%s' % timeout
            #===================================================================
            return response
        return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
    return wrapper

    