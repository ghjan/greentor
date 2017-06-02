#coding:utf8
'''
Created on 2013-4-18

@author: Administrator
'''
import base64
import copy
import urllib
import urllib2
import random
from common.utils.tool import build_request_headers, gzip_read
from common.utils.proxy_ip import get_proxy_ips

def urldecode(query):
    if not query:
        return {}
    d = {}
    a = urllib.unquote(query).split('&')
    for s in a:
        if s.find('='):
            k,v = map(urllib.unquote, s.split('='))
            d[k] = v

    return d

def urlencode(params):
    str_params = ''
    for key, val in params.items():
        if val:
            if str_params:
                str_params += '&%s=%s' % (key,val)
            else:
                str_params = '%s=%s' % (key,val)

    return str_params


def b64encode_url(string):
    u'''中文链接编码'''
    string = base64.b64encode(string.encode('utf8'))
    return string.replace('+', '-').replace('/', '_').replace('=', '')


def b64decode_url(string):
    u'''中文链接解码'''
    try:
        string = string.replace('-', '+').replace('_', '/')
        return base64.b64decode(string + (4 - len(string) % 4) * '=').decode('utf8')
    except:
        raise NameError('url format error')

def short_url_parse(string, arguments_format):
    u'''链接解析'''
    arguments = string.split('-')
    arguments_dict = {}
    for s in arguments:
        arguments_dict[s[0:2]] = s[2:]
    obj = copy.copy(arguments_format)
    for k, v in obj.items():
        if type(v) is dict:
            if arguments_dict.has_key(k):
                try:
                    obj[k] = obj[k][arguments_dict[k]]
                except:
                    obj[k] = obj[k]['default']
            else:
                obj[k] = obj[k]['default']
        else:
            if arguments_dict.has_key(k):
                obj[k] = arguments_dict[k]
    if arguments_dict.has_key('pg'):
        del(arguments_dict['pg'])
    return obj, arguments_dict


def filter_url_concat(query_dict):
    obj = {}
    keys = query_dict.keys()
    a = []
    for key in keys:
        a.append(key+query_dict[key])
        uri = []
        for k, v in query_dict.items():
            if key != k:
                uri.append(k+v)
        obj[key] = uri
    obj['all'] = sorted(a)
    return obj
    

if __name__=='__main__':

    x =  urldecode("""user_id%3D7%26url%3D%252Fconsumer%252Fshow%252F7%252F%26true_name%3D%25E9%2599%2588%25E7%258E%25B2%26message_count%3D0%26avatar%3D%252Fupload%252Fphoto%252F2013%252F06%252F13%252FQQ20120518-1.200x200_1.30x30.png%26user_name%3D%25E9%2599%2588%25E7%258E%25B2""")
    print x['user_id']
    print x['url']
    print x['true_name']
    print x['message_count']
    print x['user_name']
    print x['avatar']
