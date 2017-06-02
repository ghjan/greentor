# __author__ = 'Administrator'
# coding: utf-8

import os

from PIL import Image, ImageDraw, ImageFont


fontsize = 23
fonttype = u'msyh.ttf'
color = (255, 240, 241)


def watermark(filepath, string):
    '''在文件同级目录创建图片的水印图片'''
    ima = Image.open(filepath)
    x, y = ima.size
    font = ImageFont.truetype(fonttype, fontsize)
    draw = ImageDraw.Draw(ima)
    xr, yr = draw.textsize(string, font=font)
    if xr >= x or yr >= y:
        rate = xr / x + 1 if xr / x > 0 else yr / y + 1
        font = ImageFont.truetype(fonttype, fontsize / rate)
        xr, yr = draw.textsize(string, font=font)
    draw.text((x - xr, y - yr), string, font=font, fill=color)
    ##draw.bitmap(xy, bitmap, options)
    f1, ff = os.path.splitext(filepath)
    newfilepath = u'%s%s%s' % (f1, u'_watermark', ff)
    ima.save(newfilepath)