#coding:utf-8
'''
Created on 2015-10-18

@author: butter
'''
import os
import urllib2
import Image
import StringIO

from common import settings

from . import tool,storage_new

def get_absolute_url(path):
    u'''
    function: 根据本地相对稳健路径获取url路径
    
    path - 本地相对路径
    '''
    return '%s%s' %(settings.MEDIA_URL, path)

def get_absolute_path(path):
    return os.path.join(settings.MEDIA_ROOT, path)

def get_path_by_media_url(media_url):
    fpath = media_url.replace(settings.MEDIA_URL, '')
    return fpath

import logging
import time
django_log = logging.getLogger('django')

def save_path(file_content, fpath, optimize=False):
    u'''
    function: 保存文件内容file_content到指定的路径fpath
    
    file_content - 文件内容
    fpath - 基于MEDIA_ROOT为跟路径的相对文件路径
    optimize - 是否对文件的大小进行优化，默认为False
    '''
    t1 = time.time()
    assert(len(file_content)>0)
    
    absolute_fpath = get_absolute_path(fpath)
    
    # 判断目录是否存在，不存在则创建
    absolute_dir_path = os.path.dirname(absolute_fpath)
    if not os.path.exists(absolute_dir_path):
        os.makedirs(absolute_dir_path)
    
    file_size = len(file_content)
    if (optimize == True) and (file_size>500*1024):
        # 优化的点为，如果size>3M, 则quality设为80%， 如果大于500K,则quality设为90%
        # 如果图片宽度超过1200px， 则等比压缩为1200px
        im = Image.open(StringIO.StringIO(file_content))
        if im.size[0] > 1200:
            new_width = 1200
            new_height = int(1.0*new_width*im.size[1]/im.size[0])
            im = im.resize((new_width, new_height), Image.ANTIALIAS)
        quality = 90
        if file_size >= 3*1024*1024:
            quality = 80
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im.save(absolute_fpath, quality=quality)
        del im
    else:
        f = file(absolute_fpath, 'wb+')
        f.write(file_content)
        f.close()
    
    t2 = time.time()
    django_log.info('[storage.save - %s - %s - %s]'%(absolute_fpath, file_size, t2-t1))


def save(file_content, dir_path='', suffix='jpg', optimize=False):
    u'''
    
    file_content - 文件内容
    dir_path - 基于MEDIA_ROOT为跟路径的相对目录路径
    suffix - 文件名后缀, 默认为jpg
    optimize - 是否对文件的大小进行优化，默认为False
    
    return: 返回相对路径
    '''
    
    dir_path = os.path.join(dir_path, tool.get_date_path())
    fname = '%s.%s' %(tool.create_uuid(), suffix)
    fpath = os.path.join(dir_path, fname)
    
    save_path(file_content, fpath, optimize)
    storage_new.save_path(file_content, fpath, optimize)
    
    return fpath

def save_url(url, dir_path='', try_count=2):
    u'''
    url: 文件的外部url
    dir_path: 基于MEDIA_ROOT为跟路径的相对目录路径
    return: 返回相对路径
    '''
    
    while try_count > 0:
        try_count -= 1
        
        try:
            rsp = urllib2.urlopen(url)
        except:
            continue
        
        if rsp.code != 200:
            rsp.close()
            continue
        file_content = rsp.read()
        fpath = save(file_content, dir_path)
        del file_content
        rsp.close()
        return fpath
    
    return None

def exists(path):
    u'''
    function: 判断相对路径path是否存在
    
    path - 相对路径
    
    return: True/False
    '''
    return os.path.exists(get_absolute_path(path))
