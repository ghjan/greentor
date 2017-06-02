#!/usr/bin/env python
# coding: utf-8
'''
Created on 2016年3月4日

@author: butter.huang
'''

from aliyunsdkcore import client
from aliyunsdkcdn.request.v20141111 import RefreshObjectCachesRequest

from common import settings

client = client.AcsClient(settings.ALIYUN_ACCESS_KEY_ID, settings.ALIYUN_ACCESS_KEY_SECRET, 'cn-hangzhou')

def refresh_object_caches(object_path, object_type='File'):
    u'''
    function: 刷新指定路径的url路径(可为目录或者文件路径)的cdn缓存。url刷新日限额2000个，目录刷新日限额100个
    
    object_path - 刷新的url路径，如abc.com/image/1.png 或 abc.com/image/
    object_type - 可选， 刷新的类型， 其值可以为File | Directory，默认是File。
    
    return: {"RefreshTaskId":"704222904","RequestId":"D61E4801-EAFF-4A63-AAE1-FBF6CE1CFD1C"}
    '''
    
    assert(object_type in ['File', 'Directory'])
    
    request = RefreshObjectCachesRequest.RefreshObjectCachesRequest()
    request.set_accept_format('json')
    request.set_ObjectPath(object_path)
    request.set_ObjectType(object_type)
    
    return client.do_action(request)
