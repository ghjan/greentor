#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author magic
"""
from django.conf import settings

STATIC_URL = settings.STATIC_URL
MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
# STATIC_GRUNT_ROOT = settings.STATIC_GRUNT_ROOT
DJANGO_USER = settings.DJANGO_USER
# SPHINX_SERVER = settings.SPHINX_SERVER
# SPHINX_PORT = settings.SPHINX_PORT
DEBUG = settings.DEBUG
# GRUNT_ON = settings.GRUNT_ON
# DOMAIN_NAME = settings.DOMAIN_NAME
# ERROR_TEMPLATE = settings.ERROR_TEMPLATE
# SCM_BIN = settings.SCM_BIN

# ERROR = {
# }
# ERROR.update(settings.ERROR)

REAL_CRYPTO_KEY = '3XngWHHT12Rr0ecSKULWJnTcvrOGfPoO'


class StateEnum:
    VALID = 0
    TEMPORARY = 1
    DELETED = 9
STATE_CHOICES = (
    (StateEnum.VALID, u'有效' ),
    (StateEnum.TEMPORARY, u'临时记录'),
    (StateEnum.DELETED, u'删除' ),
)

# class StateEnum(object):
#     VALID = 0
#     TEMPORARY = 1
#     INVALID = 9
#
# STATE_CHOICES = (
#     (StateEnum.VALID, '有效'),
#     (StateEnum.TEMPORARY, '临时有效'),
#     (StateEnum.INVALID, '无效的'),
# )

# 页面缓存key
COMMON_PAGE_CACHE_KEY = '%s.views.decorators.page_cache.%s'

CACHE_PAGE_KEY_PREFIX = 'common.cache_page'


class RegexEnum:
    # 手机
    MOBILE = r'^1[34578]\d{9}$'
    # email
    EMAIL = r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    # 合法的手机或email账号
    USERNAME = r'(^1[34578]\d{9}$)|(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)'
    # 密码
    PASSWORD = r'^[^\s]{6,16}$'
    # 用户类型
    USER_TYPE = r'^[012]$'
    # 32位UUID编号
    UUID_NO = r'^[0-9a-fA-F]{32}$'
    # 32位UUID编号
    UUID_NOS = r'^([0-9a-fA-F]{32},)*([0-9a-fA-F]{32})$'
    # 32位MD5
    SIGN = r'^[0-9a-fA-F]{32}$'
    # 验证码
    VERIFYCODE = r'^[0-9a-zA-Z]{1,8}$'
    # 性别
    USER_SEX = r'^[NMF]$'
    # ID
    ID = r'^\d{1,32}$'
    # ID列表字符串，已都好分隔
    IDS = r'^(\d+,)*(\d+)$'
    # BOOL(0-False,1-True)
    BOOLEAN = r'^[01]$'
    # 整数或小数
    NUMBER = r'^(-?\d*)(\.\d+)?$'
    # state状态
    STATE = r'^[019]$'
    # data
    DATA = r'.*'


################################
##公共正则表达式
##日期
# DATE_REGULAR_EXPRESSION = '^((?:19|20)\d\d)-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$'

COMMON_PROXY_IP_CACHE_KEY = 'common.proxy.ip'
COMMON_PROXY_IP_CACHE_TIME = 7*24*60*60
COMMON_PROXY_IPS = [
    '103.27.24.117:80',
    '111.13.109.52:80', # 高匿
    '163.177.159.149:80', # 透明
    '218.200.66.196:8080', # 高匿
    '120.198.236.10:80', # 高匿
    '220.248.224.242:8089', # 高匿
    '183.207.228.122:80', # 透明
    '101.26.38.162:80', # 透明
    '116.228.80.186:8080', # 高匿
    '120.197.234.164:80', # 高匿
    '218.200.66.196:8080', # 高匿
    '220.248.224.242:8089', # 高匿
]

################################
# 虚拟动态数字生成的缓存设置
# VIRTUAL_COUNT_TODAY_CACHE_KEY = 'common.virtual.count.today'
# VIRTUAL_COUNT_30DAY_CACHE_KEY = 'common.virtual.count.30day'

CRYPTO_KEY = 'f056380ed970b169'
CRYPTO_IV = '912467427a354o9x'
# 搜索引擎标识
# SPIDER_UA_KEYWORDS = ['baiduspider', 'googlebot', '360spider', 'sogou web spider', 'yisouspider', 'msnbot-media']

class BoolNumberEnum:
    NO = 0
    YES = 1
BOOL_NUMBER_CHOICES = (
    (BoolNumberEnum.NO, u'否'),
    (BoolNumberEnum.YES, u'是'),
)


class DecorationTypeEnum:
    CEILING = 0
    FLOOR = 1
    WALL_FORONT = 2
    WALL_BACK = 3
DECORATION_TYPE_CHOICES = (
    (DecorationTypeEnum.CEILING, u'吊顶' ),
    (DecorationTypeEnum.FLOOR, u'地板'),
    (DecorationTypeEnum.WALL_FORONT, u'墙正面' ),
    (DecorationTypeEnum.WALL_BACK, u'墙背面' ),
)

# 阿里云配置
ALIYUN_ACCESS_KEY_ID = 'VO2qxqlHDYFZkzPv'
ALIYUN_ACCESS_KEY_SECRET = 'N4Xpn9rnMvkbVydzgecwD3S5dMiYIH'
if hasattr(settings, 'ALIYUN_ACCESS_KEY_ID'):
    ALIYUN_ACCESS_KEY_ID = settings.ALIYUN_ACCESS_KEY_ID

if hasattr(settings, 'ALIYUN_ACCESS_KEY_SECRET'):
    ALIYUN_ACCESS_KEY_SECRET = settings.ALIYUN_ACCESS_KEY_SECRET

IMAGE_SMALL_THUMBNAIL_NAME = 'small'
IMAGE_BIG_THUMBNAIL_NAME = 'big'
IMAGE_SQUARE_THUMBNAIL_NAME = 'square'

IMAGE_THUMBNAIL_SIZE_CHOICES = (
    (IMAGE_SMALL_THUMBNAIL_NAME,  (180,100)),
    (IMAGE_BIG_THUMBNAIL_NAME,    (480,300)),
    (IMAGE_SQUARE_THUMBNAIL_NAME, (300,300))
)

EMPTY_IMG_FPATH = 'common/empty.jpg'

# 设计风格(用于单选风格）
class DesignStyleEnum:
    DEFAULT = 0
    JY = 1
    XD = 2
    ZS = 3
    OS = 4
    MS = 5
    TY = 6
    XGD = 7
    HD = 8
    DZH = 9
    DNY = 10
    RS = 11
    YJ = 12
    BO = 13
    JO = 14
DESIGN_STYLE_CHOICES = (
    (DesignStyleEnum.DEFAULT, u'未知'),
    (DesignStyleEnum.JY, u'简约'),
    (DesignStyleEnum.XD, u'现代'),
    (DesignStyleEnum.ZS, u'中式'),
    (DesignStyleEnum.OS, u'欧式'),
    (DesignStyleEnum.MS, u'美式'),
    (DesignStyleEnum.TY, u'田园'),
    (DesignStyleEnum.XGD, u'新古典'),
    (DesignStyleEnum.HD, u'混搭'),
    (DesignStyleEnum.DZH, u'地中海'),
    (DesignStyleEnum.DNY, u'东南亚'),
    (DesignStyleEnum.RS, u'日式'),
    (DesignStyleEnum.YJ, u'宜家'),
    (DesignStyleEnum.BO, u'北欧'),
    (DesignStyleEnum.JO, u'简欧'),
)

# 设计风格(用于多选风格）
class DesignStyleMultipleEnum:
    DEFAULT = 0
    JY = 1
    XD = 2
    ZS = 4
    OS = 8
    MS = 16
    TY = 32
    XGD = 64
    HD = 128
    DZH = 256
    DNY = 512
    RS = 1024
    YJ = 2048
    BO = 4096
    JO = 8192
DESIGN_STYLE_Multiple_CHOICES = (
    (DesignStyleMultipleEnum.DEFAULT, u'未知'),
    (DesignStyleMultipleEnum.JY, u'简约'),
    (DesignStyleMultipleEnum.XD, u'现代'),
    (DesignStyleMultipleEnum.ZS, u'中式'),
    (DesignStyleMultipleEnum.OS, u'欧式'),
    (DesignStyleMultipleEnum.MS, u'美式'),
    (DesignStyleMultipleEnum.TY, u'田园'),
    (DesignStyleMultipleEnum.XGD, u'新古典'),
    (DesignStyleMultipleEnum.HD, u'混搭'),
    (DesignStyleMultipleEnum.DZH, u'地中海'),
    (DesignStyleMultipleEnum.DNY, u'东南亚'),
    (DesignStyleMultipleEnum.RS, u'日式'),
    (DesignStyleMultipleEnum.YJ, u'宜家'),
    (DesignStyleMultipleEnum.BO, u'北欧'),
    (DesignStyleMultipleEnum.JO, u'简欧'),
)

