# encoding: utf-8
'''
Created on 2015-2-2
@author: leo.liu
'''

import Image
from common import settings as common_settings

def photo_crop(photo_name, custom_name, size, im_ext='JPEG', quality=95, cut=False):
    """
    function: 等比缩放或者裁剪图片（缩放的时候如果图片保持图片尺寸不变，多余部分留白）
    # 例如 原图 1000x800 新图 500x500 那么先缩放为500x300, 再扩充200的空白。
    """
    # 文件保存格式jpg==jpeg
    if im_ext.lower() == 'jpg':
        im_ext = 'JPEG'
    
    im = Image.open(photo_name)
    if (im.mode).upper() != 'RGB':
        im = im.convert("RGB")

    x1, y1 = im.size
    x2, y2 = size
    # 原始尺寸及新尺寸的xy比例
    scale_x = float(x2)/x1
    scale_y = float(y2)/y1
    # 原始图片压缩
    if cut == False:
        newsize = (x2, int(y1*scale_x)) if scale_x < scale_y else (int(x1*scale_y), y2)
    else:
        newsize = (x2, int(y1*scale_x)) if scale_x > scale_y else (int(x1*scale_y), y2)
    
    if cut == False:
        resize = im.resize(newsize, Image.ANTIALIAS)
    else:
        im = im.resize(newsize, Image.ANTIALIAS)
        # 裁剪 坐标
        x = (newsize[0] - x2)/2
        y = (newsize[1] - y2)/2
        box = (x, y, (x + x2), (y + y2))
        resize = im.crop(box)
    
    resize.save(custom_name, im_ext, quality=quality)
    del im, resize
    
def create_common_thumbnail(img_path):
    """裁剪图片的3种通用缩略图"""
    file_type = img_path.split('.')[-1]
    
    for key_name, val_size in dict(common_settings.IMAGE_THUMBNAIL_SIZE_CHOICES).items():
        
        thumbnail_path = '%s.%s.%s' % (img_path, key_name, file_type)
        photo_crop(img_path, thumbnail_path, val_size, cut=True)
    
def square_thumbnail_extname(img):
    file_type = img.split('.')[-1]
    return '%s.%s' % (common_settings.IMAGE_SQUARE_THUMBNAIL_NAME, file_type)

def get_square_thumbnail(img):
    return '%s.%s' % (img, square_thumbnail_extname(img))

def small_thumbnail_extname(img):
    file_type = img.split('.')[-1]
    return '%s.%s' % (common_settings.IMAGE_SMALL_THUMBNAIL_NAME, file_type)

def get_small_thumbnail(img):
    return '%s.%s' % (img, small_thumbnail_extname(img))

def big_thumbnail_extname(img):
    file_type = img.split('.')[-1]
    return '%s.%s' % (common_settings.IMAGE_BIG_THUMBNAIL_NAME, file_type)

def get_big_thumbnail(img):
    return '%s.%s' % (img, big_thumbnail_extname(img))
