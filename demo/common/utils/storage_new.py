#coding:utf-8
'''
Created on 2015-10-18

@author: butter
'''
import os
import oss2
import urllib2
import Image
import StringIO

from common import settings
from common.files.oss import oss_media_bucket, oss_farm_bucket


from . import tool

def get_absolute_url(path, empty_fpath=settings.EMPTY_IMG_FPATH):
    u'''
    function: 根据本地相对稳健路径获取url路径
    
    path - 本地相对路径
    '''
    if not path:
        path = empty_fpath
    return '%s%s' %(settings.MEDIA_URL, path)

def get_absolute_path(path):
    return path

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
        
        tmp_file = StringIO.StringIO()
        im.save(tmp_file, 'jpeg', quality=quality)
        del im
        tmp_file.seek(0)
        buff = tmp_file.read()
        tmp_file.close()
        oss_media_bucket.put_object(fpath, buff)
        del buff
    else:
        oss_media_bucket.put_object(fpath, file_content)
    
    t2 = time.time()
    django_log.info('[storage_new.save - %s - %s - %s]'%(fpath, file_size, t2-t1))

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
        
        fpath = save(rsp.read(), dir_path)
        rsp.close()
        return fpath
    
    return None

def read(fpath):
    u'''
    function: 读取文件内容
    
    fpath - 文件路径
    
    return - file content文件内容
    '''
    f = oss_media_bucket.get_object(fpath)
    
    file_content = f.read()
    return file_content

def remove(fpath):
    u'''
    function: 删除文件
    
    fpath - 文件路径
    '''
    oss_media_bucket.delete_object(fpath)

def exists(path):
    u'''
    function: 判断相对路径path是否存在
    
    path - 相对路径
    
    return: True/False
    '''
    try:
        oss_media_bucket.get_object(path)
    except oss2.exceptions.NoSuchKey, e:
        return False
    return True

def getsize(fpath):
    u'''
    function: 获取文件大小
    
    fpath - 文件路劲
    
    return: 
    '''
    
    file_object = oss_media_bucket.get_object(fpath)
    return file_object.content_length

def listdir(dir_path, prefix='', max_count=1000):
    u'''
    function: 列出目录下的所有文件
    
    dir_path - 目录路径
    prefix - 文件名前缀
    max_count - 最大数量
    
    return - 文件名列表
    '''
    oss_prefix = os.path.join(dir_path, prefix)
    
    result = oss_media_bucket.list_objects(oss_prefix, max_keys = max_count)
    keys = [obj.key for obj in result.object_list]
    return [os.path.basename(key) for key in keys]

def copy_from_local(local_fpath, fpath):
    u'''
    function: 将本地文件复制到oss中
    
    local_fpath - 本地文件路径
    fpath - oss文件路径
    '''
    oss_media_bucket.put_object_from_file(fpath, local_fpath)

def copy_to_local(fpath, local_fpath):
    u'''
    function: 将oss文件复制到本地
    
    fpath - oss文件路径
    local_fpath - 本地文件路径
    '''
    oss_media_bucket.get_object_to_file(fpath, local_fpath)


def delete_file_by_key_on_oss(fpath):
    u'''
    function: 根据指定的key删除OSS上的文件

    fpath - oss文件路径
    '''
    oss_media_bucket.delete_object(fpath)


def migrate_file_between_buckets(src_path, dest_path):
    file_content = oss_farm_bucket.get_object(src_path).read()
    return save(file_content, dest_path)
