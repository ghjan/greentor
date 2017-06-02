# __author__ = 'Administrator'
# coding: utf-8

import os
import shutil

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings as django_settings

_file_root = os.path.dirname(__file__)

_fontsize  = 16
_fonttype  = os.path.join(_file_root, 'msyh.ttf')
_water_1   = os.path.join(_file_root, 'water_1.png')
_water_2   = os.path.join(_file_root, 'water_2.png')

_watermark_font_color = (200, 200, 200)


def watermark(filepath, string='', bak=True):
    '''在文件同级目录创建图片的水印图片，灰字白底'''
    if bak:
        f1, ff = os.path.splitext(filepath)
        newfilepath = u'%s%s%s' % (f1, u'.filecopy', ff)
        shutil.copy(filepath, newfilepath)
        
    ima = Image.open(filepath)
    x, y = ima.size
    font = ImageFont.truetype(_fonttype, _fontsize)
    
    if string:
        string   = u'@%s' % string
        image_wm = Image.open(_water_1)
        ImageDraw.Draw(image_wm).text((57, 25), string, _watermark_font_color, font)
    else:
        image_wm = Image.open(_water_2)

    x_wm, y_wm = image_wm.size
    mark = image_wm.convert('RGBA')
    ima.paste(image_wm, (x-x_wm-20, y-y_wm-15), mark)
    ima.save(filepath)