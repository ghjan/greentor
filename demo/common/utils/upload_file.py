#!/usr/bin/env python
#coding: utf-8
#created on 2011-5-25
#authur:  butter

import os
from datetime import date

from django.core.files.storage import FileSystemStorage
from django.conf import settings

PHOTO_STORAGE = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photo/'), 
                                               base_url=os.path.join(settings.MEDIA_URL, 'photo/'))


ROOMMAP_PHOTO_STORAGE = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photo/roommap/'), 
                                               base_url=os.path.join(settings.MEDIA_URL, 'photo/roommap/'))
COMPOUND_PHOTO_STORAGE = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photo/compound/'), 
                                               base_url=os.path.join(settings.MEDIA_URL, 'photo/compound/'))

FILE_STORAGE = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'file/'), 
                                               base_url=os.path.join(settings.MEDIA_URL, 'file/'))

# iFuwo object 存储
IFUWO_OBJECT_STORAGE = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'ifuwo/model/'), 
                                               base_url=os.path.join(settings.MEDIA_URL, 'ifuwo/model/'))

# iFuwo的户型存储
IFUWO_HOUSELAYOUT_STORAGE = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'ifuwo/houselayout/'), 
                                               base_url=os.path.join(settings.MEDIA_URL, 'ifuwo/houselayout/'))

# 3d模型品牌logo
BRAND_LOGO_STORAGE = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photo/brand/'),
    base_url=os.path.join(settings.MEDIA_URL, 'photo/brand/'))

def upload_to(instance, filename):
    '''
    function: 头像的上传路径
    '''
    
    return os.path.join(date.today().strftime('%Y/%m/%d/'), filename)
