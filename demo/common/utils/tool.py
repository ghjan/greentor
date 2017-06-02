# coding:utf-8
'''
Created on 2015-1-23

@author: butter
'''

import os
import uuid
import datetime, time
import random
import commands
import re
import gzip
import StringIO
import HTMLParser

from django.utils import html
from django.core.cache import cache

from common import settings

html_parser = HTMLParser.HTMLParser()


def create_uuid():
    return str(uuid.uuid1()).replace('-', '')


def create_verifycode(digits=6):
    '''
    生成随机数字验证码字符串
    digits - 位数
    '''
    return ''.join([str(random.randint(0, 9)) for i in range(digits)])


def create_random_string(digits=10):
    chars = random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], digits)
    return ''.join(chars)


def generate_deal_serial_no(uid):
    """产生订单号"""

    return str(datetime.datetime.now()).replace('.', '').replace(':', '').replace('-', '').replace(' ', '') + str(
        uid).zfill(10) + str(random.randint(0, 99)).zfill(2)


def get_local_ips():
    '''
    返回本机ip地址列表
    '''
    s = commands.getoutput('hostname -I').strip(' ')
    return s.split(' ')


def is_mobile(s, regex=settings.RegexEnum.MOBILE):
    '''
    判断s是否是合法的手机号
    '''
    if re.match(regex, s):
        return True
    else:
        return False


def is_email(s, regex=settings.RegexEnum.EMAIL):
    '''
    判断s是否是合法的email
    '''
    if re.match(regex, s):
        return True
    else:
        return False


def mobile_safe(mobile):
    u'''
    function: 将显示的手机安全隐藏掉中间四位数字，如 13948594859显示成139****4859
    
    mobile - 手机号码
    
    return: 例如 139****4859
    '''

    if is_mobile(mobile):
        return mobile[:3] + '****' + mobile[7:]
    else:
        return mobile


def truncate(s, n=30, suffix=u'...'):
    u'''
    function: 对字符串截取生成字符串最大长度n
    
    s - 原字符串
    n - 截取最大长度
    suffix - 后缀
    
    return: 新字符串
    '''

    if len(s) <= n:
        return s
    else:
        return s[:n] + suffix


def get_date_path(t=None):
    u'''
    function: 生成按日期开始的文件路径 如当前日期是 2015-10-13  则返回的字符串为 1510/13/
    
    t - datetime类型，（非必填）
    
    return: 1510/13/ 这样的目录字符串
    '''
    if not t:
        t = datetime.datetime.now()
    return t.strftime('%Y%m/%d/')[2:]


def get_no_path(no):
    '''
    function: 根据uuid编号生成文件目录路径
    no - uuid编号
    '''
    valid_name = ''.join(a for a in no if ((a.isdigit()) or (a.isalpha())))
    if len(valid_name) < 4:
        valid_name = '0001'
    pre_dir_path = str(int(valid_name[0:4], 16))

    return '%s/%s/' % (pre_dir_path, no)


def get_total_page(total_count, count):
    '''
    计算总页数
    total_count - 总记录数
    count - 每页记录数
    '''
    total_page = total_count / count
    vod = total_count % count
    if vod:
        total_page += 1

    return total_page


def get_page(start_index, count):
    '''
    计算当前页
    start_index - 起数记录
    count - 每页记录数
    '''

    return start_index / count + 1


def image_suffix(fname):
    u'''
    function: 根据图片文件名获取真实的图片后缀
    
    fname - 文件名
    
    return: jpg,png,gif,tmp等
    '''

    suffix = fname.split('.')[-1].lower()

    if suffix in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
        if suffix == 'jpeg':
            return 'jpg'
        return suffix
    else:
        return 'jpg'


def is_flash_request(request):
    u'''
    function: 判断request是否由flashplayer发起的请求
    
    request - django request
    
    return: True/False
    '''
    
    if not request.META.has_key('HTTP_X_REQUESTED_WITH'):
        return False
    if request.META['HTTP_X_REQUESTED_WITH'].startswith('ShockwaveFlash'):
        return True
    else:
        return False

def create_browser_ua(mobile=False):
    '''
    生成随机浏览器User-Agent header
    mobile - 是否手机端浏览器
    return - user_agent字符串
    '''

    # 模拟的pc浏览器user agent
    PC_BROWSER_UAS = [
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
        'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
        'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
        'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    ]

    # 模拟的手机浏览器user agent
    MOBILE_BROWSER_UAS = [
        'User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'User-Agent: Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'User-Agent: Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149',
        'User-Agent: Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
        'User-Agent: Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
        'Mozilla/5.0 (Linux; Android 4.2.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36',
    ]

    if not mobile:
        return PC_BROWSER_UAS[random.randint(0, len(PC_BROWSER_UAS) - 1)]
    else:
        return MOBILE_BROWSER_UAS[random.randint(0, len(MOBILE_BROWSER_UAS) - 1)]


def create_browser_headers(mobile=False):
    '''
    生成随机浏览器headers
    mobile - 是否手机端浏览器
    return - headers dict
    '''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': create_browser_ua(mobile)
    }
    return headers


def build_request_user_agent(pc_only=False):
    """构建随机的模拟用户浏览器user agent"""
    usage = random.randint(0, 2) if pc_only else random.randint(0, 4)
    if usage == 0:
        # Chrome
        agent = 'Mozilla/%s.0 (Windows NT %s.0; WOW%s) AppleWebKit/%s.36 (KHTML, like Gecko) Chrome/%s.0.2357.65 Safari/%s.36' \
                % (random.randint(4, 5), random.randint(8, 10), random.choice([32, 64]),
                   random.randint(521, 537), random.randint(31, 43), random.randint(521, 537))
    elif usage == 1:
        # FF
        vs = random.randint(29, 36)
        agent = 'Mozilla/%s.0 (Windows NT %s.0; WOW%s; rv:%s.0) Gecko/20100101 Firefox/%s.0' \
                % (random.randint(4, 5), random.randint(8, 10), random.choice([32, 64]), vs, vs)
    elif usage == 2:
        # IE
        agent = 'Mozilla/%s.0 (compatible; MSIE %s.0; Windows NT %s.1; WOW%s; Trident/%s.0)' \
                % (random.randint(4, 5), random.randint(8, 10), random.randint(8, 10), random.choice([32, 64]),
                   random.randint(4, 5))
    elif usage == 3:
        # Android
        agent = 'Mozilla/%s.0(Linux;U;Android4.%s.%s;zh-cn;%s)AppleWebKit/534.30(KHTML, likeGecko)Version/%s.0MobileSafari/534.30' \
                % (random.randint(4, 5), random.randint(0, 3), random.randint(0, 3), \
                   random.choice(
                       ["nokia", "sony", "ericsson", "mot", "samsung", "sgh", "lg", "sie", "philips", "panasonic",
                        "alcatel", "lenovo", "cldc", "midp", "wap", "mobile"]), \
                   random.randint(3, 5))
    else:
        # iPhone
        agent = 'Mozilla/%s.0(iPhone;CPUiPhoneOS%s_%s_%slikeMacOSX)AppleWebKit/%s00.1.%s(KHTML, likeGecko)Mobile/12H321' \
                % (random.randint(4, 5), random.randint(6, 8), random.randint(0, 1), random.randint(0, 4),
                   random.randint(4, 6), random.randint(1, 4))

    return agent


def build_request_headers(pc_only=False):
    """构建request headers"""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': build_request_user_agent(pc_only=pc_only)
    }
    return headers


def gzip_read(content):
    """读取gzip压缩的数据"""
    content = StringIO.StringIO(content)
    gz = gzip.GzipFile(fileobj=content)
    raw_data = gz.read()
    gz.close()
    return raw_data


def html2text(html_content):
    u'''
    function: 将html内容转换为纯文本内容
    
    html_content - html内容
    
    return text_content
    '''

    # strip_tags清理标签， unescape负责将&lt;&gt;等html文档字符转意
    text_content = html_parser.unescape(html.strip_tags(html_content))

    return text_content


def imagemagick_convert(png_fpath, jpg_fpath, quality=90):
    u'''
    function: 调用ImageMagick的convert命令行将 png格式图转换为jpg格式图（因为PIL做这种处理会有质量损失，需要安装yum install ImageMagick)
    
    png_fpath - png图绝对路径
    jgp_fpath - jpg图绝对路径
    quality - jpg图片质量
    
    return None
    '''

    exit_status = os.system('convert %s -quality %s %s' % (png_fpath, quality, jpg_fpath))
    assert (exit_status == 0)


def make_timestamp(t=None):
    u'''
    function: 根据datetime(t)生成时间戳，如果t==None，则返回当前时间戳
    
    t - datetime，可为空
    
    return: 时间戳(int)
    '''

    if not t:
        t = datetime.datetime.now()

    return int(time.mktime(t.timetuple()))

def create_virtual_count_today():
    """
    function: 根据当天的时间 hour，依次随机递增当天的 需求总数。
    """
    today_demand = cache.get(settings.VIRTUAL_COUNT_TODAY_CACHE_KEY)
    
    datetime_now = datetime.datetime.now()
    seconds = datetime_now.hour * 60*60 + datetime_now.minute * 60 + datetime_now.second
    cache_timeout = 24*60*60 - seconds
    
    if not today_demand:
        count = 0
        for _ in range(1, datetime_now.hour):
            count += random.randint(30, 50)
        today_demand = {"count":count, "hour":datetime_now.hour}
        
        cache.set(settings.VIRTUAL_COUNT_TODAY_CACHE_KEY, today_demand, timeout=cache_timeout)
    else:
        if today_demand['hour'] < datetime_now.hour:
            
            for _ in range(datetime_now.hour - today_demand['hour']):
                today_demand['count'] += random.randint(30, 50)
            today_demand['hour'] = datetime_now.hour
            cache.set(settings.VIRTUAL_COUNT_TODAY_CACHE_KEY, today_demand, timeout=cache_timeout)
    
    return today_demand['count']

def create_virtual_count_30day():
    """
    function: 随机生成一个数字，作为30天内的需求总数，并每天更新一次。
    """
    count = cache.get(settings.VIRTUAL_COUNT_30DAY_CACHE_KEY)
    
    if not count:
        count = random.randint(50000, 70000)
        
        datetime_now = datetime.datetime.now()
        seconds = datetime_now.hour * 60*60 + datetime_now.minute * 60 + datetime_now.second
        cache_timeout = 24*60*60 - seconds
        
        cache.set(settings.VIRTUAL_COUNT_30DAY_CACHE_KEY, count, timeout=cache_timeout)
    
    return count
