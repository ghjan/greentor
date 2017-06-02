# encoding: utf-8

import hashlib
from django.core.cache import cache
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.core.urlresolvers import reverse
from django.conf import settings as django_settings
from common.settings import COMMON_PAGE_CACHE_KEY, CACHE_PAGE_KEY_PREFIX

def expire_page_cache(view, args=None):
    """
    Removes cache created by cache_page functionality. 
    Parameters are used as they are in reverse()
    todo: 删除页面缓存
    """
 
    if args is None:
        path = reverse(view)
    else:
        path = reverse(view, args=args)
 
    request = HttpRequest()
    request.path = path
    setattr(request, 'LANGUAGE_CODE', django_settings.LANGUAGE_CODE)
    key = get_cache_key(request)
    if cache.has_key(key):
        cache.delete(key)
        

def get_page_count(total_count, page_num):
    """ 计算分页总数 """
    page_count = total_count / page_num
    vod = total_count % page_num
    if vod:
        page_count += 1
        
    return page_count
        
def delete_page_cache(view=None, path=None, args=None, key_prefix=None):
    """
    function:删除页面缓存
    """
    if view is None and path is None:
        raise KeyError('view and path is none')
    
    if path is None:
        if args is None:
            path = reverse(view)
        else:
            path = reverse(view, args=args)
    
    key_prefix = key_prefix or getattr(django_settings, 'CACHE_MIDDLEWARE_KEY_PREFIX', None)
    key_prefix = key_prefix or 'default'

    cache_key = COMMON_PAGE_CACHE_KEY % (key_prefix, (hashlib.md5(path)).hexdigest())
    cache.delete(cache_key)
    
def delete_enhanced_page_cache(http_host, req_path):
    """
    function: 删除增强的页面缓存
    """
    cache_key = '%s.%s%s'%(CACHE_PAGE_KEY_PREFIX, http_host, req_path)
    cache.delete(cache_key)
    
    
def delete_cache_page(url):
    '''
    删除cache_page页面缓存
    url - cache_page的url
    '''
    if url.startswith('http://'):
        url = url[7:]
    cache_key = '%s.%s'%(CACHE_PAGE_KEY_PREFIX, url)
    cache.delete(cache_key)

    
