# coding: utf-8

from __future__ import unicode_literals

from django.db.models import *

import random
import uuid
from datetime import datetime
from django.contrib.auth.models import User

# import myfarm.settings as myfarm_settings  # STATE_CHOICES, ITEM_TAG_SETS, ITEM_CATEGORY_SET, item_sample, noes
from myfarm.settings import *

def get_absolute_url(path, empty_fpath=EMPTY_IMG_FPATH):
    u'''
    function: 根据本地相对稳健路径获取url路径

    path - 本地相对路径
    '''
    if not path:
        path = empty_fpath
    return '%s%s' % (MEDIA_URL, path)

def generate_uuid():
    uuid_str = str(uuid.uuid4())
    return uuid_str.replace('-', '')


class UnrealEnum(object):
    UNCOOKED = 100
    COOKED = 200
    IOS = 300
    ANDROID = 400


UNREAL_TYPE_CHOICES = (
    (UnrealEnum.UNCOOKED, 'uncooked'),
    (UnrealEnum.COOKED, 'cooked'),
    (UnrealEnum.IOS, 'ios'),
    (UnrealEnum.ANDROID, 'android')
)


class UnrealStatusEnum(object):
    INITIAL = 0  # not convert
    PENDING_CONVERT = 10  # converting
    CONVERTING = 20  # convert failed
    CONVERT_FAILED = 30  # converted


UNREAL_STATUS_CHOICES = (
    (UnrealStatusEnum.INITIAL, "not convert"),
    (UnrealStatusEnum.PENDING_CONVERT, "converting"),
    (UnrealStatusEnum.CONVERTING, "convert failed"),
    (UnrealStatusEnum.CONVERT_FAILED, "converted"),
)


class BoolNumberEnum(object):
    NO = 0
    YES = 1


BOOL_NUMBER_CHOICES = (
    (BoolNumberEnum.NO, 'No'),
    (BoolNumberEnum.YES, 'Yes'),
)


class Merchant(Model):
    no = CharField(max_length=32)
    name = CharField(max_length=64)
    url = URLField()
    app_no = IntegerField(default=0)
    domain = CharField(max_length=128)
    farm_domain = CharField(max_length=128)
    spec = CharField(max_length=256)


class Unreal(Model):
    no = CharField(max_length=32)
    platform = CharField(max_length=128)
    status = IntegerField(choices=UNREAL_STATUS_CHOICES, default=UnrealStatusEnum.INITIAL)
    real_type = IntegerField(choices=UNREAL_TYPE_CHOICES)
    filename = CharField(max_length=128)
    is_exist = IntegerField(choices=BOOL_NUMBER_CHOICES, default=BoolNumberEnum.NO)


class Item(Model):
    no = CharField(max_length=32)
    state = IntegerField(default=0, choices=STATE_CHOICES)
    create_time = DateTimeField(auto_now_add=True, db_index=True, verbose_name=u'创建时间')
    modify_time = DateTimeField(auto_now=True, db_index=True, verbose_name=u'修改时间')

    # 状态
    status = IntegerField(choices=ITEM_STATUS_CHOICES, default=ItemStatusEnum.INITIAL, db_index=True, verbose_name=u'模型状态')
    render_state = IntegerField(default=RenderStateEnum.WAITING, choices=RENDER_STATE_CHOICES, verbose_name=u'渲染状态')
    photo_degree = SmallIntegerField(default=PhotoDegreeGapEnum.GAP_NONE, choices=PHOTO_DEGREE_CHOICES, verbose_name=u'模型环绕照片渲染的角度间隔，每隔45度,每隔1度，0为默认')
    # 属性
    inner_type = PositiveIntegerField(default=ItemInnerTypeEnum.MODEL, choices=ITEM_INNER_TYPE_CHOICES, verbose_name=u'内部分类')
    sub_type = PositiveIntegerField(default=ItemSubTypeEnum.DEFAULT_MODEL, choices=ITEM_SUB_TYPE_CHOICES, verbose_name=u'子分类')
    system_type = SmallIntegerField(default=ItemSystemTypeEnum.DEFAULT, choices=ITEM_SYSTEM_TYPE_CHOICES, verbose_name=u'子系统分类')
    is_public = SmallIntegerField(default=BoolNumberEnum.YES, choices=BOOL_NUMBER_CHOICES, verbose_name=u'是否公开')
    lightable = SmallIntegerField(default=LightTypeEnum.NO, choices=LIGHT_TYPE_CHOICES, verbose_name=u'携带光源类型')
    scalable = SmallIntegerField(default=BoolNumberEnum.YES, choices=BOOL_NUMBER_CHOICES, verbose_name=u'是否可缩放')
    direct_scalable = SmallIntegerField(default=BoolNumberEnum.NO, choices=BOOL_NUMBER_CHOICES, verbose_name=u'是否可以单向缩放')
    # family_head = SmallIntegerField(default=BoolNumberEnum.YES, choices=BOOL_NUMBER_CHOICES, verbose_name=u'是否族主，用于确定定制关系')
    salable = SmallIntegerField(default=BoolNumberEnum.NO, choices=BOOL_NUMBER_CHOICES, verbose_name=u'是否销售')

    # 尺寸
    product_width = FloatField(default=0, verbose_name=u'物品模型宽度，单位cm')
    product_length = FloatField(default=0, verbose_name=u'物品模型长度，单位cm')
    product_height = FloatField(default=0, verbose_name=u'物品模型高度，单位cm')
    flat_height = FloatField(default=0, verbose_name=u'物品模型平台高度，单位cm')

    # 产品信息
    product_name = CharField(max_length=64, verbose_name=u'产品名称')
    product_id = CharField(default='', blank=True, max_length=32, db_index=True, verbose_name=u'商品id')
    sku_id = CharField(default='', blank=True, max_length=32, db_index=True, verbose_name=u'skuid')
    product_link = CharField(default=u'', blank=True, max_length=512, verbose_name=u'产品链接')
    product_brand = CharField(default=u'', blank=True, max_length=64, verbose_name=u'产品品牌')
    product_price = FloatField(default=0, verbose_name=u'产品价格')
    width = FloatField(default=0, verbose_name=u'产品真实宽度，单位cm')
    length = FloatField(default=0, verbose_name=u'产品真实长度，单位cm')
    height = FloatField(default=0, verbose_name=u'产品真实高度，单位cm')
    sale_count = IntegerField(default=0, verbose_name=u'销量')
    group_id = CharField(default='', blank=True, db_index=True, max_length=64, verbose_name=u'所属商家')
    material = CharField(default=u'', max_length=32, blank=True, null=True, verbose_name=u'材质')
    describe = CharField(default=u'', max_length=128, blank=True, null=True, verbose_name=u'描述')

    # 货号
    cargo_no = CharField(default=u'', blank=True, max_length=64, verbose_name=u'产品货号')
    unit = PositiveIntegerField(default=ItemUnitTypeEnum.PIECE, choices=ITEM_UNIT_TYPE_CHOICES,verbose_name=u'产品单位')
    discount_price = IntegerField(default=0, verbose_name=u'折扣价格(单位-分)')

    # 用户
    user = ForeignKey(User, verbose_name=u'所有者')
    author = ForeignKey(User, null=True, blank=True, related_name=u'author', verbose_name=u'模型管理员')
    # 模型相关
    photo_scale = FloatField(default=ITEM_DEFAULT_PHOTO_SCALE, verbose_name=u'模型渲染缩放比例')


    preview_fpath = CharField(default=u'', max_length=128, blank=True, verbose_name=u'预览图路径')

    merchant  = CharField(default=u'', max_length=128, blank=True, verbose_name=u'所属商家id')

    @property
    def preview_url(self):
        return get_absolute_url(self.preview_fpath)

    @property
    def customizable(self):
        '''
        判断物品是否可定制
        '''
        return 0
        # if ItemFamily.objects.filter(item_no=self.no)[0:1]:
        #     return 1
        # else:
        #     return 0

    class Meta:
        app_label = 'myfarm'
        verbose_name = u'物品'
        verbose_name_plural = u'物品'

    def __unicode__(self):
        return self.product_name


class Category(Model):
    # no = CharField(max_length=32)
    state = IntegerField(default=0, choices=STATE_CHOICES)
    name = CharField(max_length=32, verbose_name=u'名称')
    alias_name = CharField(max_length=32, verbose_name=u'类目别名', default='')
    parent = ForeignKey('self', null=True, blank=True, verbose_name=u'父级类目,该字段为空时表示根类目', related_name='parent_key')
    depth = PositiveSmallIntegerField(default=0, verbose_name=u'深度')

    order_id = PositiveIntegerField(default=0, verbose_name=u'顺序id')

    remark = CharField(default=u'', max_length=128, blank=True, verbose_name=u'备注')
    # 为解决冗余数据的问题，增加link_id字段，表示当前节点与目标节点有相同的子节点，故不再重复建树了
    link = ForeignKey('self', null=True, blank=True, verbose_name=u'链接id', related_name='link_key')

    def get_real_depth(self):
        u'''
        function: 根据父类目关联，计算真实的depth, 可将这个值存入depth字段方便查询使用
        '''
        p = self.parent
        d = 0
        while (p):
            d += 1
            p = p.parent
        return d

    @property
    def is_root(self):
        if not self.parent:
            return True
        else:
            return False

    @property
    def root(self):
        u'''
        function: 查询当前类目的根类目
        '''
        p = self
        while (p):
            if not p.parent:
                return p
            p = p.parent

    class Meta:
        app_label = 'myfarm'
        verbose_name = u'类目'
        verbose_name_plural = u'类目'

        unique_together = (('parent', 'name'),)

    def __unicode__(self):
        return self.name


class ItemCategory(Model):
    item_no = CharField(max_length=64, db_index=True, verbose_name=u'物品编号')
    category = ForeignKey(Category, db_index=True, verbose_name=u'类目')

    class Meta:
        app_label = 'myfarm'
        verbose_name = u'物品类目关联'
        verbose_name_plural = u'物品类目关联'

        unique_together = (('item_no', 'category'),)

    def __unicode__(self):
        return u'%s-%s' % (self.item_no, self.category.name)


if __name__ == '__main__':
    pass

# for i in range(5000000):
#     item = item_sample
#     item['no'] = generate_uuid()
#     item['category'] = random.sample(noes, 5)
#
#     print(item['no'], item['category'][0])
#     Item(**item).save()
