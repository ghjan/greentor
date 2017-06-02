#!/usr/bin/env python
#coding: utf-8

'''
Created on 2013-11-21

@author: butter
'''
import os

from django.conf import settings
from django.core.files.storage import Storage

def filename2sid(file_name):
    valid_name = ''.join(a for a in file_name if ((a.isdigit()) or (a.isalpha())))
    if len(valid_name) < 4:
        valid_name = '0001'
    return int(valid_name[0:4], 16)

def id2sid(object_id):
    str_id = str(object_id)
    if len(str_id) < 4:
        str_id = '0' * (4-len(str_id)) + str_id
    return str_id


class LFSStorage(Storage):
    '''
    Local file system storage
    '''
    
    def __init__(self, media_url=None, media_root=None, **kwargs):
        '''
        构造函数
        @param media_url: 
        @param media_root: 
        '''
        
        if media_root is None:
            media_root = settings.MEDIA_ROOT
        self.media_root = media_root
        
        if media_url is None:
            media_url = settings.MEDIA_URL
        self.media_url = media_url
    
    def delete(self, name):
        if self.exists(name):
            os.remove(self.path(name))
    
    def exists(self, name):
        return os.path.exists(self.path(name))
    
    def get_available_name(self, name):
        return name
    
    def path(self, name):
        if os.path.isabs(name):
            return name
        else:
            return os.path.join(self.media_root, self.sid(name), name)
    
    def relative_path(self, name):
        return os.path.join(self.sid(name), name)
    
    def listdir(self, path):
        l = os.listdir(self.path(path))
        ds = []
        fs = []
        for n in l:
            if os.path.isfile(os.path.join(self.path(path), n)):
                fs.append(n)
            else:
                ds.append(n)
        return ds,fs
    
    def open(self, name, mode='rb'):
        if ('w' in mode) and ('+' in mode):
            if self.exists(name):
                self.delete(name)
            dir_path = os.path.dirname(self.path(name))
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                except OSError, e:
                    # 如果目录已经存在的异常，进行忽略
                    if e.errno != 17:
                        raise e
        
        return file(self.path(name), mode)
    
    def save(self, name, content):
        f = self.open(self.get_available_name(name), 'wb+')
        f.write(content)
        f.close()
    
    def size(self, name):
        return os.path.getsize(self.path(name))
    
    def url(self, name):
        if name.startswith('/'):
            name = name[1:]
        return '%s%s/%s' %(self.media_url, self.sid(name), name)
    
    def sid(self, name):
        return str(filename2sid(name))
    