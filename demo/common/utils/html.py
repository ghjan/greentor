#coding:utf8
'''
@author: Glen
@date: 2015-9-15
'''

import re

from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup

from django.template.defaultfilters import striptags
from common.utils import string as common_string

def article_clear(html):
    ''' 去除 '''
    
    #html = html.replace('&nbsp;', ' ')
    soup = BeautifulSoup(html)
    
    # 清除字体，行间距，字体大小
    r_clear_style = re.compile('(\s?color: rgb\(0, 0, 0\)[^;]*;?|\s?font-family[^;]*;?|\s?line-height[^;]*;?|\s?font-size[^;]*(medium|small|large);?|\s?white-space[^;]*;?)')
    ss = soup.findAll(attrs={'style':r_clear_style})
    for s in ss:
        s['style'] = r_clear_style.sub("", s['style'])
    
    # 去除所有class
    ss = soup.findAll()
    for s in ss:
        if s.string is not None:
            s.string = s.text.strip()
        del s['class']

    return soup.__unicode__()


def html_unescape(html):
    """html转义字符 逆转"""
    if type(html) == str:
        html = html.decode('utf-8')
    
    html_parser = HTMLParser()
    html = html_parser.unescape(html)
    
    return html


def strip_html_tags(html):
    u'''移除html标签'''
    
    html = striptags(html).strip().replace('&nbsp;','').replace('\r','').replace('\n','').replace(u'\u3000','')
    return html


def parse_content_summary(content, length, ext=''):
    u'''解析出文章摘要'''
    
    if type(content) == str:
        content = content.decode('utf8')
    
    simple_content = common_string.wrap_word(strip_html_tags(content), length, ext)
    
    summary_content = simple_content
    str_index = len(simple_content) -1
    while str_index > 1:
        # 截取字符串
        string = simple_content[str_index]
        
        # 命中最后一个结束标点，退出
        if string in [u'。', u'！', u'？', u'?', u'!', u'.']:
            summary_content = simple_content[0:(str_index+1)]
            break
        
        # 从后往前查询
        str_index -= 1
    
    return summary_content

def lazy(html, src_field='data-lazyload', class_name='lazy'):
    u'''
    '''
    placeholder_src = 'http://static.fuwo.com/static/images/new/common/placeholder.jpg'
    
    soup = BeautifulSoup(html)
    img_tags = soup.findAll('img')
    
    if img_tags:
        for tag in img_tags:
            if tag.has_key('src'):
                tag['class'] = class_name
                tag[src_field] = tag['src']
                tag['src'] = placeholder_src
        lazy_html = unicode(soup)
    else:
        lazy_html = html
    
    soup.clear()
    del soup
    return lazy_html

def get_image_urls(html):
    """
    function: 读取html中的img src值。
    """
    rg_image = re.compile(r'src="([^\"]+)"')
    matches = rg_image.findall(html)
    return matches
