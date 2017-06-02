# coding: utf-8
'''
Created on 2016年3月14日

@author: butter.huang
'''

from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType

def fetch_content_type_id(app_label, model):
    u'''
    function: 根据app_label和model获取django content type的id, 实现过程中会使用缓存
    
    app_label - 应用label, 比如auth app的label为 "auth"
    model - Model名，比如auth.User的name为 "user", 必须小写
    
    return: content_type id
    '''
    
    cache_key = 'common.content_type.%s_%s'%(app_label, model)
    
    content_type_id = cache.get(cache_key)
    if content_type_id != None:
        return content_type_id
    
    content_type = ContentType.objects.only('id').get(app_label=app_label, model=model)
    
    cache.set(cache_key, content_type.id, timeout=7*24*60*60)
    
    return content_type.id
