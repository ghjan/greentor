# coding: utf-8
#__author__ = 'butter'
#__create__ = '14-5-23'
import random
import hashlib

def is_chinese_string(s):
    '''
    判断字符串s是否是中文
    '''
    if type(s) == str:
        s = s.decode('utf-8')
    elif type(s) == unicode:
        pass
    else:
        raise TypeError("suport type are unicode or utf8 str.")
    
    for ch in s:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    
    return False

def pure_chinese_string(s):
    '''
    function:判断字符串s是否纯中文
    '''
    if type(s) == str:
        s = s.decode('utf-8')
    elif type(s) == unicode:
        pass
    else:
        raise TypeError("suport type are unicode or utf8 str.")
    
    for ch in s:
        if (ch < u'\u4e00') or (ch > u'\u9fff'):
            return False
    
    return True


def wrap_word(string, length=15, ext='...'):
    u'''截取字符串'''
    
    if len(string) > length:
        return '%s%s' % (string[0:length],ext)
    return string

def get_random_str(length):
    u'''生成随机字符串'''
    seeds = u'''0123456789ZXCVBNMQWERTYUIOOPASDFGHJKLqwertyuioopasdfghjklzxcvbnm'''
    return u''.join([random.choice(seeds) for i in range(length)])

def string_md5(string):
    """字符串MD5加密"""
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()


def obfuscator(string, cut_char=True, add_spaces=True):
    """
    function: 简单的字符串混淆器(长度小于20的不做处理）
    params:
        cut_char - 是否随机删除一些字符。
        add_spaces - 是否随机添加一些空格
    return 处理过后的字符串
    """
    if not string:
        return string
    elif type(string) == str:
        string = string.decode('utf8')
    
    # 字符总数统计
    count = string.__len__()
    if count < 20:
        return string
    
    step = 20
    contents = []
    last_index = 0
    for i in xrange(step, count, step):
        contents.append(string[i-step : i])
        last_index = i
    else:
        overplus = string[last_index:]

    # 随机删除一些字符
    if cut_char:
        for i, content in enumerate(contents):
            random_index = random.randint(0, step-1)
            contents[i] = content[:random_index] + content[random_index+1:]
        step -= 1
    
    # 随机添加一些空格
    if add_spaces:
        # 空格符 “&nbsp;” -> u'\xa0'
        for i, content in enumerate(contents):
            random_index = random.randint(0, step-1)
            contents[i] = content[:random_index] + u'\xa0' + content[random_index:]
        step += 1
    
    contents.append(overplus)
    
    return ''.join(contents)
