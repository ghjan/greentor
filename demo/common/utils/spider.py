#coding:utf-8
'''
Created on 2015-1-23

@author: butter
'''

import os
import re
import time
import Image
import random
import urllib2

from BeautifulSoup import BeautifulSoup
from common.utils.tool import create_browser_headers, gzip_read, create_uuid
from common.utils import storage_new as storage
from common import settings

def get_response_data_by_url(url, headers={}, proxy_url=None, timeout=20, mobile=False, data=None):
    """
    function: 获取指定url的请求内容(url也可以是图片地址）
    params:
        url - 请求的网络地址（图片地址）
        headers - 请求的http headers
        proxy - 指定请求使用的代理ip
        timeout - 请求超时时间
        mobile - 是否以移动客户端形式访问
    return: {'code':200, 'msg':'succ', 'data':'请求返回的html代码或者图片内容'}
    """
    if not headers:
        headers = create_browser_headers(mobile)
    # 构建代理请求
    if proxy_url:
        proxy_type = 'http' if proxy_url.startswith('http') else 'https'
        opener = urllib2.build_opener( urllib2.ProxyHandler({proxy_type:proxy_url}) )
        opener.addheaders = [(k,v) for k,v in headers.items()]
        try:
            resp = opener.open(url, data=data, timeout=timeout)
            rsp_data = resp.read()
        except Exception, e:
            code = e.code if hasattr(e, 'code') else 500
            return {'code':code, 'msg':str(e)}
    # 直接请求
    else:
        if settings.DEBUG and (image_extname(url) is None):
            print '\nrequest is direct:', url
        try:
            request = urllib2.Request(url, headers=headers)
            resp = urllib2.urlopen(request, data=data, timeout=timeout)
            rsp_data = resp.read()
        except Exception, e:
            code = e.code if hasattr(e, 'code') else 500
            return {'code':code, 'msg':str(e)}
    
    resp.close()
    if resp.getcode() != 200:
        return {'code':resp.getcode(), 'msg':str(resp.info)}
    
    # 判断返回的数据是否经过了gzip压缩
    gzipped = resp.info().get('Content-Encoding')
    if gzipped:
        rsp_data = gzip_read(rsp_data)
    # redirect 判断请求是否跳转
    return {
            'code':resp.getcode(), 'msg':'succ',
            'data':rsp_data,
            'redirect':False if (url == resp.url) else True, # 判断请求是否跳转
            'resp_info':resp.info() # 请求的返回信息
            }

def get_response(url, proxy_list=[], headers={}, timeout=20, mobile=False, data=None):
    """
    function: 获取指定url的请求内容(url也可以是图片地址）
    params:
        url - 请求的网络地址（图片地址）
        headers - 请求的http headers
        proxy_list - 指定请求使用的代理ip列表
        timeout - 请求超时时间
        mobile - 是否以移动客户端形式访问
    return: {'code':200, 'msg':'succ', 'data':'请求返回的html代码或者图片内容'}
    """
    if proxy_list:
        # 从ip列表中抽取2个作为尝试
        if len(proxy_list) > 2:
            proxys = [random.choice(proxy_list), random.choice(proxy_list)]
        else:
            proxys = proxy_list
        
        for proxy_url in proxys:
            resp_data = get_response_data_by_url(url, headers=headers, proxy_url=proxy_url, timeout=timeout, mobile=mobile, data=data)
            if resp_data['code'] in (200, 404):
                return resp_data
            time.sleep(2)
        time.sleep(1)
    # 如果没有proxy_list, 直接访问。所有代理都失败，也直接访问。
    resp_data = get_response_data_by_url(url, headers=headers, timeout=timeout, mobile=mobile, data=data)
    return resp_data


def request_image(img_url, try_count=3):
    
    for _ in range(try_count):
        rsp_data = get_response(img_url)
        if rsp_data['code'] == 200:
            break
        time.sleep(1)
    return rsp_data


def image_download(img_url, dir_path, proxy_list=[], crop=False, **kwargs):
    """
    function: 图片下载
    params:
        img_url - 需要下载的图片的url
        dir_path - 基于MEDIA_ROOT为跟路径的相对目录路径
        proxy - 下载图片使用的代理
    return: {'code':200, 'msg':'succ', 'data':'保存的图片相对路径'}
    """
    
    rsp_data = request_image(img_url)
    if rsp_data['code'] == 200:
        # 验证图片下载的完整性。
        image_real_size = int(rsp_data['resp_info'].get('Content-Length') or rsp_data['resp_info'].get('Cotnent-Length') or -1)
        image_resp_size = len(rsp_data['data'])
        # 太小的图片直接放弃
        if image_resp_size < 2000:
            return {'code':500, 'data':None}
        
        if image_resp_size < image_real_size:
            print 'image down failed, waitting for reload.'
            rsp_data = request_image(img_url, 1)
            if rsp_data['code'] != 200:
                return rsp_data
    
        suffix = img_url.split('.')[-1]
        suffix = suffix.lower()
        if not suffix in ['jpg', 'png', 'gif', 'bmp', 'jpeg']:
            suffix = 'jpg'
        
        # 裁剪有水印的图片
        offset_xy = kwargs.get('offset_xy')
        if crop and offset_xy:
            
            # 创建临时图片文件存储
            tmp_root = '/tmp/spider/'
            if not os.path.isdir(tmp_root):
                os.mkdir(tmp_root)
            tmp_fpath = os.path.join(tmp_root, '%s.%s' % (create_uuid(), suffix))
            fp = open(tmp_fpath, 'wb')
            fp.write(rsp_data['data'])
            fp.close()
            
            crop_mode = kwargs.get('crop_mode', 1)
            position = kwargs.get('position', 3)
            try:
                photo_watermark_crop(tmp_fpath, tmp_fpath, offset_xy, position, crop_mode)
                crop_fp = open(tmp_fpath, 'rb')
                rsp_data['data'] = crop_fp.read()
                crop_fp.close()
            except IOError:
                # 图片有问题，相当于放弃该图片
                rsp_data = {'code':500, 'data':None}
                if settings.DEBUG:
                    print 'image crop failed, will be removed.'
            os.remove(tmp_fpath)
        
        if rsp_data['data']:
            fpath = storage.save(rsp_data['data'], dir_path, suffix)
            rsp_data['data'] = fpath
        
    return rsp_data
    

def photo_watermark_crop(origin_image, save_path, offset_xy, position=3, crop_mode=1):
    """
    function: 根据图片水印的位置，宽度和高度对比，把带有水印的部分裁剪掉（一整边）
    params:
        origin_image - 原始图片地址
        save_path - 保存地址
        offset_xy - 裁剪水印偏离顶角的x或y位移坐标（都是正数）。
        position - 水印所处的位置（顺时针方向） :1 (左上/顶部)；2 (右上/右边)；3 (右下/底部)；4 (左下/左边)；
        crop_mode - 裁剪模式：1、根据水印的位置及原图的长宽比例裁剪某一边；2、根据水印的位置裁剪固定的边（例如：position为1，裁剪顶部。）。
    """
    def _create_crop_box(im_size, offset_xy, position, crop_mode):
        """生成裁剪的box"""
        x,y = im_size
        crop_x, crop_y = offset_xy
        if crop_mode == 1:
            # 裁剪规则：如果图片x，y的比例大于4/3则裁剪图片的左边或者右边，否则裁剪图片的顶部或者底部
            if (float(x)/float(y)) > (4.0/3.0):
                if position in (1, 4):
                    box = (crop_x, 0, x, y)
                else:
                    box = (0, 0, (x-crop_x), y)
            else:
                if position in (1, 2):
                    box = (0, crop_y, x, y)
                else:
                    box = (0, 0, x, (y-crop_y))
        elif crop_mode == 2:
            # 裁剪规则： 根据position值，裁剪固定的一边，顶部和底部裁剪高度为crop_y；左右裁剪宽度为crop_x；
            if position == 1:
                box = (0, crop_y, x, y)
            elif position == 2:
                box = (0, 0, (x-crop_x), y)
            elif position == 3:
                box = (0, 0, x, (y-crop_y))
            else:
                box = (crop_x, 0, x, y)
        else:
            # 维持原图不变
            box = (0, 0, x, y)
        
        return box
    # 裁剪图片
    im = Image.open(origin_image)
    if (im.mode).upper() != 'RGB':
        im = im.convert("RGB")
    box = _create_crop_box(im.size, offset_xy, position, crop_mode)
    new_im = im.crop(box)
    
    new_im.save(save_path, quality=95)
    del im, new_im
    

def count_html_alink(html, exclude_img=False):
    """ 统计A标签数量 """
    if (type(html) == str) or (type(html) == unicode):
        html = BeautifulSoup(html)
    alinks = html.findAll("a")
    # 排除图片上的A链接（图片链接有时候是给搜索引擎用的，实际点击时不会打开链接）
    if exclude_img:
        count = 0
        for alink in alinks:
            if not alink.find("img"):
                count += 1
    else:
        count = len(alinks)
    return count

def has_badword(content, extra=u''):
    """
    function:检查html中是否含有关键字。
    params:
        content - 要检测的内容
        extra - 附加检查的内容
    return: True or False
    """
    keywords = [u'土巴兔', u'小兔', u'酷家乐', u'小酷', u'小乐', u'乐乐', u'kujiale', 'to8to', u'优居客', u'小优', u'youjuke', u'x团', u'X团']
    if (type(content) == str) or (type(content) == unicode):
        content = BeautifulSoup(content)
    html_text = content.getText()
    text = u'%s,%s' % (html_text, extra)
    for kw in keywords:
        if text.find(kw) > -1:
            return True
        
    return False

def html_dispose_before_use(html):
    """
    function:在内容处理（所有的内容操作）之前清理完全不需要的html(包括图片，div，p等标签)
    params:
        html - 需要预处理的html或者BeautifulSoup对象
    return 处理过后的BeautifulSoup对象
    """
    if (type(html) == str) or (type(html) == unicode):
        html = BeautifulSoup(html)
    # remove img-owner
    img_owners = html.findAll("div", attrs={"class":"img-owner"})
    for img_own in img_owners:
        img_own.decompose()
    # remove face image
    face_images = html.findAll("img", attrs={"data-type":"emoji"})
    for img_face in face_images:
        img_face.decompose()
    # remove error image
    rg_img = re.compile(r'data:image/png[^\"]+')
    error_images = html.findAll("img", attrs={'data-url':rg_img})
    for img_error in error_images:
        img_error.decompose()
    # remove file image
    rg_file = re.compile(r'file:/[^\"]+')
    file_images = html.findAll("img", attrs={'data-url':rg_file})
    for img_file in file_images:
        img_file.decompose()
    # remove previous next（to8to PC端访问的时候有前一篇，后一篇。）
    prenext = html.find("div", attrs={"class":"yezhu-zxcs-page-up"})
    if prenext:
        prenext.decompose()
    
    # 删除 推荐内容 及   删除“注：...”的内容，带有关键字的内容段落
    p_contents = html.findAll("p")
    for p_content in p_contents:
        pcontent = str(p_content).decode("utf8")
        if (pcontent.find(u"装修网") > -1):
            p_content.decompose()
            continue
        if (pcontent.find(u'土巴兔') > -1) or (pcontent.find(u'小兔') > -1) or (pcontent.find(u'注：') > -1):
            p_content.decompose()
            continue
        if (p_content.getText() == u'相关阅读：'):
            p_content.decompose()
            continue
        if (str(p_content) == '<p>%s</p>' % str(p_content.find("a"))):
            p_content.decompose()
            continue
        
    # 删除X团网底部推荐
    xtuan_filter_words = [u'相关推荐']
    P_index = 0
    break_index = 0
    for p_dom in html.findAll("p"):
        p_text = p_dom.text.strip()
        for filter_word in xtuan_filter_words:
            if p_text.startswith(filter_word):
                break_index = P_index
        P_index += 1
    if break_index != 0:
        for del_p_dom in html.findAll("p")[break_index:]:
            del_p_dom.decompose()
            
    # 删除X团网底部标签    
    xtuan_tag = html.find("p", attrs={"class":"tag"})
    if xtuan_tag:
        xtuan_tag.decompose()
        
    return html

def replace_img_alt(html, alt=""):
    """
    function: 替换html中所有img的alt内容
    params:
        html - 原始html内容
        alt - 要替换的alt内容
    return 替换过后的html(unicode)
    """
    if (type(html) == str) or (type(html) == unicode):
        html = BeautifulSoup(html)
    images = html.findAll("img")
    for im in images:
        im['alt'] = alt
        
    return html.__unicode__()

def html_dispose(html, remove_a=False):
    """
    function:处理html内容（包括删除各自不需要的样式，id，name。。。，替换某些关键字，图片属性等操作）
    params:
        html - 需要处理的html
        remove_a - 是否删除非图片链接及内容
    return 处理后的html（unicode）
    """
    # <[^>]*?>
    # 重要：后面所有的字符串操作都是基于unicode的，所以这里必须保留
    if (type(html) == str):
        html = html.decode('utf8')
        
    # 删除  src="/static/images/common/pixel.gif"（酷家乐的图片是懒加载方式）
    html = html.replace('src="/static/images/common/pixel.gif"', '')
    
    rg_pattern_tuple = (
        (u'<a[^>]+>点击[^<\/a>]*<\/a>', ""), # 删除“点击进入...”的链接
        ('<a[^>]+>[^<img]*(<img[^>]+>)[^<\/a>]*<\/a>', r'\1'), # 删除图片的链接
        (r'<a[^>]+>[^<]*</a>' if remove_a else '', ''), # 删除非图片链接及内容
        ('<a\s[^>]*>', ''), # 删除多余的A（有些A标签可能不完整）
        ('<\/a>', ''), # 删除多余的A（有些A标签可能不完整）
        # 删除html标签的某些指定属性（id,name,style...）,移除 href="*"（有非A标签也可能会带有href="*"）
        ('\s(href|onclick|style|class|name|id|width|height|title)=\"[^\"]*\"', ""),
        # 酷家乐图片是懒加载方式，所以需要转换data-url=>src
        (r'data-url="([^\"]+)"', r'src="\1"'),
        # 去除非段落标题部分的加粗显示（strong标签）
        (r'([^>\n|\s?])<strong>(.*?)</strong>', r'\1\2'),
        # 土巴兔内容在移动端都是<article>...</article>形式
        (r"<article>([\w\W]+?)</article>", r"<div>\1</div>"),
        (u"(以上就是.{0,4}?小编|以上就是本文).*?(\.|。|\?|？|\!|！)", ""), # 删除某些文章最后的编辑内容的第一句：以上就是小编...
    )
    for rg, pattern in rg_pattern_tuple:
        action_re = re.compile(rg)
        html = action_re.sub(pattern, html)
    
    # 查找所有的p标签
    p_re = re.compile("<p\s*>[\w\W]+?</p>")
    p_all = p_re.findall(html)
    # 相关广告语
    advertisements = [u'<span>马上发布&gt;&gt;',u'<span>看看&gt;&gt;</span>',u">>>更多"]
    # 匹配中文
    zh_char_re = re.compile(u'[\u4e00-\u9fa5]')
    for item_out in p_all:
        # 如果html中带有图片标签的前缀<img 就认为该p标签中有图片，直接跳过.
        if item_out.find("<img") > -1:
            continue
        # 清除空白的p标签
        if not (zh_char_re.search(item_out)):
            html = html.replace(item_out,"")
        # 清除广告
        new_item_out = item_out.replace(" ","")
        # 如果html中带有相关广告语则删除
        for ad in advertisements:
            if new_item_out.find(ad) > -1:
                html = html.replace(item_out,"")   
                break      
        
    # 替换或过滤敏感关键词
    sensitive_words = (
        (u"X团", u"福窝"),
        (u"x团", u"福窝"),
        (u"www.xtuan.com/导语：", ""),
    )
    for src,desc in sensitive_words:
        html = html.replace(src,desc)
        
    return html

def img_url_dispose(img_url, domain=None):
    """
    function: 图片url处理（下载之前有些图片的url需要先行处理）
    params:
        img_url - 图片url
        domain - 因为有的网站内容中图片url不完整，所以需要提供该网站的domain来补全图片url以便下载。
    return: 处理过后的img url
    """
    if domain and (not img_url.startswith("http")):
        img_url = '%s%s' % (domain, img_url)
    
    # webp格式url处理
    if img_url.find('tp=webp') > 0:
        img_url = img_url.replace('tp=webp', 'tp=jpg')
    
    suffix = img_url.split('.')[-1]
    # xtuan的图片需要去掉最后的部分url
    img_url = img_url.replace("_w_w200.%s" % suffix, ".%s" % suffix).replace("_w200.%s" % suffix,".%s" % suffix)
    
    return img_url

def get_html_images(html):
    """查找html中的图片url"""
    rg_image = re.compile(r'src="([^\"]+)"')
    matches = rg_image.findall(html)
    #===========================================================================
    # if domain:
    #    matches_copy = []
    #    for match in matches:
    #        if not match.startswith("http"):
    #            match = '%s%s' % (domain,match)
    #        matches_copy.append(match)
    #    matches = matches_copy
    #===========================================================================
    return matches

def image_extname(img_url):
    """
    function: 获取图片的扩展名（网络常见图片url），如果不是图片链接或非常见图片链接形式，返回None。
    params:
        img_url - 网络常见图片url
    return 'jpg'
    """
    base_url = img_url.split('?')[0]
    last_split = base_url.split('.')[-1].lower()
    
    extname = last_split if last_split in ('jpg', 'jpeg', 'png', 'gif', 'bmp') else None
    
    return extname