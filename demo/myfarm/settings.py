#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author magic, create Date: 5/16/17
"""
import os
from tornado.options import define
import random


# DATABASE = dict(
#     db='model',
#     host='127.0.0.1',
#     port=27017
# )

# 产品模型状态
class ItemStatusEnum:
    INITIAL = 0  # 未审核
    PENDING_AUDIT = 10  # 待审核
    AUDITING = 20  # 管理员审核中
    AUDIT_FAILED = 30  # 管理员审核未通过
    AUDITED = 40  # 管理员审核通过
    WAREHOUSE = 50  # 已入库


ITEM_STATUS_CHOICES = (
    (ItemStatusEnum.INITIAL, u'未审核'),
    (ItemStatusEnum.PENDING_AUDIT, u'待审核'),
    (ItemStatusEnum.AUDITING, u'管理员审核中'),
    (ItemStatusEnum.AUDIT_FAILED, u'管理员审核未通过'),
    (ItemStatusEnum.AUDITED, u'管理员审核通过'),
    (ItemStatusEnum.WAREHOUSE, u'已入库'),
)


class StateEnum:
    VALID = 0
    TEMPORARY = 1
    DELETED = 9


STATE_CHOICES = (
    (StateEnum.VALID, u'有效'),
    (StateEnum.TEMPORARY, u'临时记录'),
    (StateEnum.DELETED, u'删除'),
)


# 模型渲染处理状态
class RenderStateEnum:
    WAITING = 0
    LINEUP = 1
    RENDERING = 2
    FINISH = 3
    FAILED = 4


RENDER_STATE_CHOICES = (

    (RenderStateEnum.WAITING, u'未渲染'),
    (RenderStateEnum.LINEUP, u'排队中(已发往渲染农场)'),
    (RenderStateEnum.RENDERING, u'渲染中'),
    (RenderStateEnum.FINISH, u'渲染完成'),
    (RenderStateEnum.FAILED, u'渲染失败'),
)

# 3d模型图片间隔度数
class PhotoDegreeGapEnum:
    GAP_NONE = 0
    GAP_1 = 1
    GAP_45 = 45
PHOTO_DEGREE_CHOICES = (
    (PhotoDegreeGapEnum.GAP_NONE, u'无'),
    (PhotoDegreeGapEnum.GAP_45, u'45度一张'),
    (PhotoDegreeGapEnum.GAP_1, u'1度一张'),
)

# 产品内部分类
class ItemInnerTypeEnum:
    MODEL = 1       # 家具
    DOOR = 2        # 门
    WINDOW = 3      # 窗
    MATERIAL = 4    # 材质
    CUPBOARD_LINE = 5  # 线条
    CUPBOARD_FRAME = 6  # 框架

ITEM_INNER_TYPE_CHOICES = (
    (ItemInnerTypeEnum.MODEL,       u'家具'),
    (ItemInnerTypeEnum.DOOR,        u'门'),
    (ItemInnerTypeEnum.WINDOW,      u'窗'),
    (ItemInnerTypeEnum.MATERIAL,    u'材质'),
    (ItemInnerTypeEnum.CUPBOARD_LINE, u'线条'),
    (ItemInnerTypeEnum.CUPBOARD_FRAME, u'框架'),
)


# 产品子分类
class ItemSubTypeEnum:
    DEFAULT_MODEL = 101
    TOP_MODEL = 102
    BOTTOM_MODEL = 103
    BACKEND_MODEL = 104
    FLOOR_MODEL = 105
    ROOF_DEFAULT_MODEL = 106
    ROOF_BOTTOM_MODEL = 107
    ROOF_TOP_MODEL = 108
    ROOF_TOP_PLUS_MODEL = 109

    ROOF_DEFAULT = 110
    ROOF_CEILING = 111

    SINGLE_DOOR = 201
    DOUBLE_DOOR = 202
    SLIDING_DOOR = 203
    POCKET_DOOR = 204

    GENERAL_WINDOW = 301
    FLOATING_WINDOW = 302
    FRENCH_WINDOW = 303

    FLOOR_MATERIAL = 401
    WALL_MATERIAL = 402
    SKIRTING_MATERIAL = 403
    CEILING_MATERIAL = 404

    CUPBOARD_FOOT_LINE = 501
    CUPBOARD_FRONT_WATER_PROOF_LINE = 502
    CUPBOARD_REAR_WATER_PROOF_LINE = 503
    CUPBOARD_WALL_TOP_LINE = 504

    CUPBOARD_DEFAULT_FRAME = 600
    CUPBOARD_GROUND_FRAME = 601
    CUPBOARD_MIDDLE_FRAME = 602
    CUPBOARD_HIGH_FRAME = 603
    CUPBOARD_TOP_FRAME = 604

    CABINET_UNIT_FRAME = 700


ITEM_SUB_TYPE_CHOICES = (
    (ItemSubTypeEnum.DEFAULT_MODEL, u'DEFAULT模型'),
    (ItemSubTypeEnum.TOP_MODEL, u'TOP模型'),
    (ItemSubTypeEnum.BOTTOM_MODEL, u'BOTTOM模型'),
    (ItemSubTypeEnum.BACKEND_MODEL, u'BACKEND模型'),
    (ItemSubTypeEnum.FLOOR_MODEL, u'FLOOR模型'),
    (ItemSubTypeEnum.ROOF_DEFAULT_MODEL, u'ROOF_DEFAULT模型'),
    (ItemSubTypeEnum.ROOF_BOTTOM_MODEL, u'ROOF_BOTTOM模型'),
    (ItemSubTypeEnum.ROOF_TOP_MODEL, u'ROOF_TOP模型'),
    (ItemSubTypeEnum.ROOF_TOP_PLUS_MODEL, u'ROOF_TOP_PLUS模型'),

    (ItemSubTypeEnum.ROOF_DEFAULT, u'默认顶部模型'),
    (ItemSubTypeEnum.ROOF_CEILING, u'吊顶'),

    (ItemSubTypeEnum.SINGLE_DOOR, u'单开门'),
    (ItemSubTypeEnum.DOUBLE_DOOR, u'双开门'),
    (ItemSubTypeEnum.SLIDING_DOOR, u'推拉门'),
    (ItemSubTypeEnum.POCKET_DOOR, u'门套'),

    (ItemSubTypeEnum.GENERAL_WINDOW, u'普通窗'),
    (ItemSubTypeEnum.FLOATING_WINDOW, u'飘窗'),
    (ItemSubTypeEnum.FRENCH_WINDOW, u'落地窗'),

    (ItemSubTypeEnum.FLOOR_MATERIAL, u'地面材质'),
    (ItemSubTypeEnum.WALL_MATERIAL, u'墙面材质'),
    (ItemSubTypeEnum.SKIRTING_MATERIAL, u'踢脚线材质'),
    (ItemSubTypeEnum.CEILING_MATERIAL, u'顶面材质'),

    (ItemSubTypeEnum.CUPBOARD_FOOT_LINE, u'橱柜脚线'),
    (ItemSubTypeEnum.CUPBOARD_FRONT_WATER_PROOF_LINE, u'橱柜台面前挡水线'),
    (ItemSubTypeEnum.CUPBOARD_REAR_WATER_PROOF_LINE, u'橱柜台面后挡水线'),
    (ItemSubTypeEnum.CUPBOARD_WALL_TOP_LINE, u'橱柜吊柜顶线'),

    (ItemSubTypeEnum.CUPBOARD_DEFAULT_FRAME, u'橱柜默认框架'),
    (ItemSubTypeEnum.CUPBOARD_GROUND_FRAME, u'橱柜地柜框架'),
    (ItemSubTypeEnum.CUPBOARD_MIDDLE_FRAME, u'橱柜中柜框架'),
    (ItemSubTypeEnum.CUPBOARD_HIGH_FRAME, u'橱柜高柜框架'),
    (ItemSubTypeEnum.CUPBOARD_TOP_FRAME, u'橱柜顶柜框架'),

    (ItemSubTypeEnum.CABINET_UNIT_FRAME, u'衣柜单元柜框架'),
)


# 物品系统分类，用于在各个子系统，如柜子，吊顶，橱柜顶子系统中类型的识别和区分
class ItemSystemTypeEnum:
    DEFAULT = 0

    CABINET_DEFAULT = 100  # 柜架定制系统默认类型
    CABINET_DOOR = 101  # 柜架定制-柜门
    CABINET_DRAWER = 102  # 柜架定制-抽屉
    CABINET_POLE = 103  # 柜架定制-挂杆

    CEILING_DEFAULT = 200  # 吊顶定制系统默认类型
    CEILING_JIAOXIAN = 201  # 吊顶定制-角线

    CUPBOARD = 400  # 橱柜定制
    CUPBOARD_CABINET = 401  # 橱柜定制-单元柜
    CUPBOARD_BOARD = 402  # 橱柜定制-板件
    CUPBOARD_JIAOXIAN = 403  # 橱柜定制-脚线
    CUPBOARD_DOOR = 404  # 橱柜定制-门板
    CUPBOARD_HANDLE = 405  # 橱柜定制-把手

    TILER = 500  # 区域铺贴
    TILER_CERAMIC = 501  # 瓷砖
    TILER_WOOD = 502  # 地板
    TILER_BOUNDARY = 505  # 波打线
    TILER_PATTERN = 510  # 样式

    HOUSEMADE_CABINET_DEFAULT = 600  # 全屋定制-衣柜

    PANEL = 700  # 护墙板定制
    PANEL_KEEL = 701  # 龙骨
    PANEL_WALLBOARD = 702  # 墙板
    PANEL_LINE = 703  # 线条


ITEM_SYSTEM_TYPE_CHOICES = (
    (ItemSystemTypeEnum.DEFAULT, u'默认'),

    (ItemSystemTypeEnum.CABINET_DOOR, u'柜架定制-柜门'),
    (ItemSystemTypeEnum.CABINET_DRAWER, u'柜架定制-抽屉'),
    (ItemSystemTypeEnum.CABINET_POLE, u'柜架定制-挂杆'),

    (ItemSystemTypeEnum.CEILING_DEFAULT, u'吊顶定制-默认'),
    (ItemSystemTypeEnum.CEILING_JIAOXIAN, u'吊顶定制-角线'),

    (ItemSystemTypeEnum.CUPBOARD, u'橱柜定制'),
    (ItemSystemTypeEnum.CUPBOARD_CABINET, u'橱柜定制-单元柜'),
    (ItemSystemTypeEnum.CUPBOARD_BOARD, u'橱柜定制-板件'),
    (ItemSystemTypeEnum.CUPBOARD_JIAOXIAN, u'橱柜定制-脚线'),
    (ItemSystemTypeEnum.CUPBOARD_DOOR, u'橱柜定制-门板'),
    (ItemSystemTypeEnum.CUPBOARD_HANDLE, u'橱柜定制-把手'),

    (ItemSystemTypeEnum.TILER, u'区域铺贴'),
    (ItemSystemTypeEnum.TILER_CERAMIC, u'区域铺贴-瓷砖'),
    (ItemSystemTypeEnum.TILER_WOOD, u'区域铺贴-地板'),
    (ItemSystemTypeEnum.TILER_BOUNDARY, u'区域铺贴-波打线'),
    (ItemSystemTypeEnum.TILER_PATTERN, u'区域铺贴-样式'),

    (ItemSystemTypeEnum.HOUSEMADE_CABINET_DEFAULT, u'衣柜定制'),

    (ItemSystemTypeEnum.PANEL, u'护墙板定制'),
    (ItemSystemTypeEnum.PANEL_KEEL, u'龙骨'),
    (ItemSystemTypeEnum.PANEL_WALLBOARD, u'墙板'),
    (ItemSystemTypeEnum.PANEL_LINE, u'线条'),
)

class BoolNumberEnum:
    NO = 0
    YES = 1
BOOL_NUMBER_CHOICES = (
    (BoolNumberEnum.NO, u'否'),
    (BoolNumberEnum.YES, u'是'),
)

class LightTypeEnum:
    NO = 0
    DEFAULT = 1
    FACET = 2
    SPHERE = 3
    IES = 4
LIGHT_TYPE_CHOICES = (
    (LightTypeEnum.NO, u'无灯光'),
    (LightTypeEnum.DEFAULT, u'默认光'),
    (LightTypeEnum.FACET, u'面灯光'),
    (LightTypeEnum.SPHERE, u'球灯光'),
    (LightTypeEnum.IES, u'IES光'),
)


# 产品单位
class ItemUnitTypeEnum:
    PIECE = 1  # 件
    SET = 2  # 套
    BLOCK = 3  # 块
    ZHAN = 4  # 盏
    ZHANG = 5  # 张
    GE = 6  # 个
    MI = 7  # 米
    PINGFANGMI = 8  # ㎡
    PEN = 9  # 盆
    TANG = 10  # 樘
    PIAN = 11  # 片
    ZU = 12  # 组
    TIAO = 13  # 条
    XIANG = 14  # 项
    JUAN = 15  # 卷
    TONG = 16  # 桶
    ZUO = 17  # 座
    BU = 18  # 步


ITEM_UNIT_TYPE_CHOICES = (
    (ItemUnitTypeEnum.PIECE, u'件'),
    (ItemUnitTypeEnum.SET, u'套'),
    (ItemUnitTypeEnum.BLOCK, u'块'),
    (ItemUnitTypeEnum.ZHAN, u'盏'),
    (ItemUnitTypeEnum.ZHANG, u'张'),
    (ItemUnitTypeEnum.GE, u'个'),
    (ItemUnitTypeEnum.MI, u'm'),
    (ItemUnitTypeEnum.PINGFANGMI, u'㎡'),
    (ItemUnitTypeEnum.PEN, u'盆'),
    (ItemUnitTypeEnum.TANG, u'樘'),
    (ItemUnitTypeEnum.PIAN, u'片'),
    (ItemUnitTypeEnum.ZU, u'组'),
    (ItemUnitTypeEnum.TIAO, u'条'),
    (ItemUnitTypeEnum.XIANG, u'项'),
    (ItemUnitTypeEnum.JUAN, u'卷'),
    (ItemUnitTypeEnum.TONG, u'桶'),
    (ItemUnitTypeEnum.ZUO, u'座'),
    (ItemUnitTypeEnum.BU, u'步'),
)
ITEM_DEFAULT_PHOTO_SCALE = 1.4 # flash端物品图片默认缩放比例值（图片像素/实际尺寸)
ITEM_MATERIAL_PHOTO_SCALE = 2 # flash端材质物品图片默认缩放比例值（图片像素/实际尺寸)
ITEM_LARGE_PHOTO_SCALE = 1    # 对尺寸较大的模型，其photo scale相对变小一点
ITEM_TAG_SETS = {
    'CATEGORY_TAGS': [
        {
            'name': u'硬装建材', 'id': 'yingzhuangjiancai', 'children': [
            {
                'name': u'门', 'id': 'men',
                'children': [
                    {'name': u'进户门', 'id': 'jinhumen', 'children': [], },
                    {'name': u'室内门', 'id': 'shineimen', 'children': [], },
                    {'name': u'移门', 'id': 'yimen', 'children': [], },
                    {'name': u'折叠门', 'id': 'zhediemen', 'children': [], },
                    {'name': u'门套', 'id': 'mentao', 'children': [], },
                ],
            },
            {
                'name': u'窗', 'id': 'chuanghu',
                'children': [
                    {'name': u'平开窗', 'id': 'pingkaichuang', 'children': [], },
                    {'name': u'推拉窗', 'id': 'tuilachuang', 'children': [], },
                    {'name': u'观景窗', 'id': 'guanjingchuang', 'children': [], },
                    {'name': u'飘窗', 'id': 'piaochuang', 'children': [], },
                    {'name': u'落地窗', 'id': 'luodichuang', 'children': [], },
                    {'name': u'装饰窗', 'id': 'zhuangshichuang', 'children': [], },
                ],
            },
            {
                'name': u'地面', 'id': 'dimian',
                'children': [
                    {'name': u'地板', 'id': 'diban', 'children': [], },
                    {'name': u'地砖', 'id': 'dizhuan', 'children': [], },
                    {'name': u'满铺地毯', 'id': 'manputitan', 'children': [], },
                    {'name': u'踢脚线', 'id': 'tijiaoxian', 'children': [], },
                ],
            },
            {
                'name': u'墙面', 'id': 'qiangmian',
                'children': [
                    {'name': u'墙纸', 'id': 'qiangzhi', 'children': [], },
                    {'name': u'墙砖', 'id': 'qiangzhuan', 'children': [], },
                    {'name': u'乳胶漆', 'id': 'rujaioqi', 'children': [], },
                    {'name': u'护墙板', 'id': 'huqiangban', 'children': [], },
                ],
            },
            {
                'name': u'天花板', 'id': 'dingmian',
                'children': [
                    {'name': u'吊顶', 'id': 'diaoding', 'children': [], },
                    {'name': u'顶角线', 'id': 'dingjiaoxian', 'children': [], },
                ],
            },
            {
                'name': u'背景墙类', 'id': 'beijingqianglei',
                'children': [
                    {'name': u'背景墙', 'id': 'beijingqiang', 'children': [], },
                    {'name': u'电视背景墙', 'id': 'dianshibeijingqiang', 'children': [], },
                    {'name': u'卧室背景墙', 'id': 'woshibeijingqiang', 'children': [], },
                ],
            },
            {
                'name': u'基本构造', 'id': 'jibengouzhao',
                'children': [
                    {'name': u'玄关', 'id': 'xuanguan', 'children': [], },
                    {'name': u'柱子', 'id': 'zhuzi', 'children': [], },
                    {'name': u'地台', 'id': 'ditai', 'children': [], },
                    {'name': u'栏杆', 'id': 'langan', 'children': [], },
                    {'name': u'楼梯', 'id': 'louti', 'children': [], },
                    {'name': u'壁炉', 'id': 'bilu', 'children': [], },
                ],
            },
            {
                'name': u'水电', 'id': 'shuidian',
                'children': [
                    {'name': u'开关', 'id': 'kaiguan', 'children': [], },
                    {'name': u'插座', 'id': 'chazuo', 'children': [], },
                    {'name': u'电箱', 'id': 'dianxiang', 'children': [], },
                    {'name': u'接线板', 'id': 'jiexianban', 'children': [], },
                ],
            },
        ],
        },
        {
            'name': u'家具', 'id': 'jiaju', 'children': [
            {
                'name': u'床类', 'id': 'chuanglei',
                'children': [
                    {'name': u'床', 'id': 'chuang', 'checked_for': ['woshi'], 'children': [], },
                    {'name': u'单人床', 'id': 'danrenchuang', 'checked_for': ['woshi'], 'children': [], },
                    {'name': u'双人床', 'id': 'shuangrenchuang', 'checked_for': ['woshi'], 'children': [], },
                    {'name': u'高低/子母床', 'id': 'gaodizimuchuang', 'children': [], },
                    {'name': u'儿童床', 'id': 'ertongchuang', 'children': [], },
                    {'name': u'婴儿床', 'id': 'yingerchuang', 'children': [], },
                    {'name': u'沙发床', 'id': 'shafachuang', 'children': [], },
                    {'name': u'榻榻米', 'id': 'tatami', 'children': [], },
                ],
            },
            {
                'name': u'沙发', 'id': 'shafalei',
                'children': [
                    {'name': u'单人沙发', 'id': 'danrenshafa', 'children': [], },
                    {'name': u'双人沙发', 'id': 'shuangrenshafa', 'children': [], },
                    {'name': u'多人沙发', 'id': 'duorenshafa', 'children': [], },
                    {'name': u'组合沙发', 'id': 'zuheshafa', 'children': [], },
                    {'name': u'儿童沙发', 'id': 'ertongshafa', 'children': [], },
                ],
            },
            {
                'name': u'柜', 'id': 'guilei', 'children': [
                {'name': u'电视柜', 'id': 'dianshigui', 'checked_for': ['keting', 'woshi'], 'children': [], },
                {'name': u'衣柜', 'id': 'yigui', 'checked_for': ['woshi', ], 'children': [], },
                {'name': u'儿童衣柜', 'id': 'ertongyigui', 'checked_for': ['ertongfang', ], 'children': [], },
                {'name': u'床头柜', 'id': 'chuangtougui', 'checked_for': ['woshi', ], 'children': [], },
                {'name': u'餐边柜', 'id': 'canbiangui', 'checked_for': ['canting', ], 'children': [], },
                {'name': u'书柜', 'id': 'shugui', 'children': [], },
                {'name': u'储物柜', 'id': 'chuwugui', 'children': [], },
                {'name': u'壁柜', 'id': 'bigui', 'children': [], },
                {'name': u'斗柜', 'id': 'dougui', 'children': [], },
                {'name': u'鞋柜', 'id': 'xiegui', 'children': [], },
                {'name': u'酒柜', 'id': 'jiugui', 'children': [], },
                {'name': u'门厅/玄关柜', 'id': 'mentingxuanguangui', 'children': [], },
                {'name': u'角柜', 'id': 'jiaogui', 'children': [], },
            ],
            },
            {
                'name': u'桌', 'id': 'zhuolei',
                'children': [
                    {'name': u'餐桌', 'id': 'canzhuo', 'children': [], },
                    {'name': u'餐桌椅组合', 'id': 'canzhuoyizuhe', 'children': [], },
                    {'name': u'梳妆台/桌', 'id': 'shuzhuangtaizhuo', 'children': [], },
                    {'name': u'书桌', 'id': 'shuzhuo', 'children': [], },
                    {'name': u'儿童书桌', 'id': 'ertongshuzhuo', 'children': [], },
                    {'name': u'书桌椅组合', 'id': 'shuzhuoyizuhe', 'children': [], },
                    {'name': u'电脑桌', 'id': 'diannaozhuo', 'children': [], },
                    {'name': u'吧台/吧椅', 'id': 'bataibayi', 'children': [], },
                    {'name': u'麻将桌', 'id': 'majiangzhuo', 'children': [], },
                ],
            },
            {
                'name': u'椅/凳/榻', 'id': 'yidengta',
                'children': [
                    {'name': u'餐椅', 'id': 'canyi', 'children': [], },
                    {'name': u'沙发椅', 'id': 'shafayi', 'children': [], },
                    {'name': u'写字椅', 'id': 'xieziyi', 'children': [], },
                    {'name': u'儿童椅', 'id': 'ertongyi', 'checked_for': ['ertongfang', ], 'children': [], },
                    {'name': u'贵妃椅', 'id': 'guifeiyi', 'children': [], },
                    {'name': u'休闲椅', 'id': 'xiuxianyi', 'children': [], },
                    {'name': u'沙发凳', 'id': 'shafadeng', 'children': [], },
                    {'name': u'梳妆凳', 'id': 'shuzhuangdeng', 'children': [], },
                    {'name': u'床尾凳', 'id': 'chuangweideng', 'children': [], },
                    {'name': u'矮凳', 'id': 'aideng', 'children': [], },
                ],
            },
            {
                'name': u'架', 'id': 'jiaxianglei',
                'children': [
                    {'name': u'衣帽架', 'id': 'yimaojia', 'children': [], },
                    {'name': u'鞋架', 'id': 'xiejia', 'children': [], },
                    {'name': u'书架', 'id': 'shujia', 'children': [], },
                    {'name': u'花架', 'id': 'haujia', 'children': [], },
                    {'name': u'博古架', 'id': 'bogujia', 'children': [], },
                    {'name': u'隔板/壁架', 'id': 'gebanbijia', 'children': [], },
                    {'name': u'杂志/报刊架', 'id': 'zazhibaokanjia', 'children': [], },
                ],
            },
            {
                'name': u'几', 'id': 'jilei',
                'children': [
                    {'name': u'茶几', 'id': 'chaji', 'children': [], },
                    {'name': u'角几/边几', 'id': 'jiaojibianji', 'children': [], },
                    {'name': u'套几', 'id': 'taoji', 'children': [], },
                ],
            },
        ],
        },
        {
            'name': u'厨/卫', 'id': 'chuwei',
            'children': [
                {
                    'name': u'厨房', 'id': 'chufang',
                    'children': [
                        {'name': u'橱柜', 'id': 'chugui', 'children': [], },
                        {'name': u'橱房配件/挂架', 'id': 'chufangpeijianguajia', 'children': [], },
                        {'name': u'厨具', 'id': 'chuju', 'children': [], },
                        {'name': u'餐具', 'id': 'canju', 'children': [], },
                    ],
                },
                {
                    'name': u'卫浴', 'id': 'weiyu',
                    'children': [
                        {'name': u'坐便器', 'id': 'zuobianqi', 'children': [], },
                        {'name': u'浴室柜', 'id': 'yushigui', 'children': [], },
                        {'name': u'洗脸台盆', 'id': 'xiliantaipen', 'children': [], },
                        {'name': u'花洒', 'id': 'huasa', 'children': [], },
                        {'name': u'淋浴房', 'id': 'linyufang', 'children': [], },
                        {'name': u'浴缸', 'id': 'yugang', 'children': [], },
                        {'name': u'小便斗', 'id': 'xiaobiandou', 'children': [], },
                        {'name': u'卫浴配件/挂架', 'id': 'weiyupeijianguajia', 'children': [], },
                        {'name': u'浴霸', 'id': 'yuba', 'children': [], },
                    ],
                },
            ],
        },
        {
            'name': u'家饰', 'id': 'jiashi',
            'children': [
                {
                    'name': u'家居饰品', 'id': 'jiajushipin',
                    'children': [
                        {'name': u'屏风/隔断', 'id': 'pingfenggeduan', 'children': [], },
                        {'name': u'装饰摆件', 'id': 'zhuangshibaijian', 'children': [], },
                        {'name': u'照片墙', 'id': 'zhaopianqiang', 'children': [], },
                        {'name': u'装饰画', 'id': 'zhuangshihua', 'children': [], },
                        {'name': u'油画', 'id': 'youhua', 'children': [], },
                        {'name': u'花瓶', 'id': 'huaping', 'children': [], },
                        {'name': u'鱼缸', 'id': 'yurgang', 'children': [], },
                    ],
                },
                {
                    'name': u'布艺软饰', 'id': 'buyiruanshi',
                    'children': [
                        {'name': u'窗帘', 'id': 'chuanglian', 'children': [], },
                        {'name': u'地毯', 'id': 'ditan', 'children': [], },
                        {'name': u'抱枕', 'id': 'baozhen', 'children': [], },
                        {'name': u'沙发垫', 'id': 'shafadian', 'children': [], },
                    ],
                },
                {
                    'name': u'鲜花园艺', 'id': 'xianhuayuanyi',
                    'children': [
                        {'name': u'植物/盆景', 'id': 'zhiwupenjing', 'children': [], },
                        {'name': u'花艺套装', 'id': 'huayitaozhuang', 'children': [], },
                    ],
                },
                {
                    'name': u'镜子', 'id': 'jingzhilei',
                    'children': [
                        {'name': u'试衣镜', 'id': 'shiyijing', 'children': [], },
                        {'name': u'化妆镜', 'id': 'huazhuangjing', 'children': [], },
                        {'name': u'浴室镜', 'id': 'yushijing', 'children': [], },
                    ],
                },
                {
                    'name': u'其它家饰', 'id': 'qitajiashi',
                    'children': [
                        {'name': u'乐器', 'id': 'yueqi', 'children': [], },
                        {'name': u'美术用品', 'id': 'meishuyongpin', 'children': [], },
                        {'name': u'体育器材', 'id': 'tiyuqicai', 'children': [], },
                    ],
                },
            ],
        },
        {
            'name': u'灯饰', 'id': 'dengshi',
            'children': [
                {
                    'name': u'灯具', 'id': 'dengju',
                    'children': [
                        {'name': u'吊灯', 'id': 'diaodeng', 'children': [], },
                        {'name': u'吸顶灯', 'id': 'xidingdeng', 'children': [], },
                        {'name': u'台灯', 'id': 'taideng', 'children': [], },
                        {'name': u'射灯', 'id': 'shedeng', 'children': [], },
                        {'name': u'筒灯', 'id': 'tongdeng', 'children': [], },
                        {'name': u'落地灯', 'id': 'luodideng', 'children': [], },
                        {'name': u'壁灯', 'id': 'bideng', 'children': [], },
                    ],
                },
            ],
        },
        {
            'name': u'家电', 'id': 'jiadian',
            'children': [
                {
                    'name': u'冰/洗/空', 'id': 'bingxikong',
                    'children': [
                        {'name': u'冰箱', 'id': 'bingxiang', 'children': [], },
                        {'name': u'洗衣机', 'id': 'xiyiji', 'children': [], },
                        {'name': u'空调', 'id': 'kongtiao', 'children': [], },
                    ],
                },
                {
                    'name': u'影音数码', 'id': 'yingyinshuma',
                    'children': [
                        {'name': u'电视', 'id': 'dianshi', 'children': [], },
                        {'name': u'影音设备', 'id': 'yingyinshebei', 'children': [], },
                        {'name': u'电脑', 'id': 'diannao', 'children': [], },
                    ],
                },
                {
                    'name': u'厨房电器', 'id': 'chufangdianqi',
                    'children': [
                        {'name': u'抽油烟机', 'id': 'chouyouyanji', 'children': [], },
                        {'name': u'燃气灶', 'id': 'ranqizao', 'children': [], },
                        {'name': u'电磁炉', 'id': 'diancilu', 'children': [], },
                        {'name': u'微波炉', 'id': 'weibolu', 'children': [], },
                        {'name': u'热水器', 'id': 'reshuiqi', 'children': [], },
                        {'name': u'消毒柜', 'id': 'xiaodugui', 'children': [], },
                    ],
                },
                {
                    'name': u'其它家电', 'id': 'qitajiadian',
                    'children': [
                        {'name': u'饮水机', 'id': 'yinshuiji', 'children': [], },
                    ],
                },
            ],
        },
    ],

    'AREA_TAGS': [
        {'name': u'客厅', 'id': 'keting', },
        {'name': u'餐厅', 'id': 'canting', },
        {'name': u'卧室', 'id': 'woshi', },
        {'name': u'书房', 'id': 'shufang', },
        {'name': u'儿童房', 'id': 'ertongfang', },
        {'name': u'厨房', 'id': 'chufang', },
        {'name': u'卫生间', 'id': 'weishengjian', },
        {'name': u'阳台', 'id': 'yangtai', },
        {'name': u'不限空间', 'id': 'buxiankongjian', },
    ],

    'STYLE_TAGS': [
        {'name': u'现代', 'id': 'xiandai', },
        {'name': u'欧式', 'id': 'oushi', },
        {'name': u'美式', 'id': 'meishi', },
        {'name': u'新中式', 'id': 'xinzhongshi', },
        {'name': u'新古典', 'id': 'xingudian', },
        {'name': u'田园', 'id': 'tianyuan', },
        {'name': u'地中海', 'id': 'dizhonghai', },
        {'name': u'中式', 'id': 'zhongshi', },
        {'name': u'东南亚', 'id': 'dongnanya', },
        {'name': u'混搭', 'id': 'hunda', },
    ],

    # 一下为系统保留的内部tag，若存在，则不删除
    'RESERVED_TAGS': [
        {'name': u'可定制', 'id': 'kedingzhi', },
    ],
}

ITEM_CATEGORY_SET = {
    'BASE_CATEGORY': [
        {'id': 'private', 'name': u'我的物品', 'children': [
            {'id': 'private', 'name': u'我的物品', 'children': [
                {'id': 'wodeshoucang', 'name': u'我的收藏', 'children': []},
                {'id': 'wodezuhe', 'name': u'我的组合', 'children': []},
                {'id': 'wodemoxing', 'name': u'我的模型', 'children': []},
            ]},
        ]},
    ],
    'EXTEND_CATEGORY': [

        {'id': 'menchuang', 'name': u'门窗', 'children': [
            {'id': 'men', 'name': u'门', 'children': [
                {'id': 'jinhumen', 'name': u'进户门', 'children': []},
                {'id': 'shineimen', 'name': u'室内门', 'children': []},
                {'id': 'yimen', 'name': u'移门', 'children': []},
                {'id': 'zhediemen', 'name': u'折叠门', 'children': []},
                {'id': 'mentao', 'name': u'门套', 'children': []},
            ]},
            {'id': 'chuang', 'name': u'窗', 'children': [
                {'id': 'pingkaichuang', 'name': u'平开窗', 'children': []},
                {'id': 'tuilachuang', 'name': u'推拉窗', 'children': []},
                {'id': 'guanjingchuang', 'name': u'观景窗', 'children': []},
                {'id': 'piaochuang', 'name': u'飘窗', 'children': []},
                {'id': 'luodichuang', 'name': u'落地窗', 'children': []},
                {'id': 'zhuangshichuang', 'name': u'装饰窗', 'children': []},
            ]},
        ]},

        {'id': 'yingzhuang', 'name': u'硬装', 'children': [
            {'id': 'dimian', 'name': u'地面', 'children': [
                {'id': 'diban', 'name': u'地板', 'children': []},
                {'id': 'dizhuan', 'name': u'地砖', 'children': []},
                {'id': 'manpuditan', 'name': u'满铺地毯', 'children': []},
                {'id': 'tijiaoxian', 'name': u'踢脚线', 'children': []},
            ]},
            {'id': 'qiangmian', 'name': u'墙面', 'children': [
                {'id': 'qiangzhi', 'name': u'墙纸', 'children': []},
                {'id': 'qiangzhuan', 'name': u'墙砖', 'children': []},
                {'id': 'rujiaoqi', 'name': u'乳胶漆', 'children': []},
                {'id': 'beijingqiang', 'name': u'背景墙', 'children': []},
                {'id': 'huqiangban', 'name': u'护墙板', 'children': []},
            ]},
            {'id': 'tianhuaban', 'name': u'天花板', 'children': [
                {'id': 'diaoding', 'name': u'吊顶', 'children': []},
                {'id': 'dingjiaoxian', 'name': u'顶角线', 'children': []},
            ]},
            {'id': 'beijingqianglei', 'name': u'背景墙类', 'children': [
                {'id': 'beijingqiang', 'name': u'背景墙', 'children': []},
                {'id': 'dsbeijingqiang', 'name': u'电视背景墙', 'children': []},
                {'id': 'wsbeijingqiang', 'name': u'卧室背景墙', 'children': []},
            ]},
            {'id': 'shuidian', 'name': u'水电', 'children': [
                {'id': 'kaiguan', 'name': u'开关', 'children': []},
                {'id': 'chazuo', 'name': u'插座', 'children': []},
                {'id': 'dianxiang', 'name': u'电箱', 'children': []},
                {'id': 'jiexianban', 'name': u'接线板', 'children': []},
            ]},
            {'id': 'qita', 'name': u'其它', 'children': [
                {'id': 'xuanguan', 'name': u'玄关', 'children': []},
                {'id': 'zhuzi', 'name': u'柱子', 'children': []},
                {'id': 'ditai', 'name': u'地台', 'children': []},
                {'id': 'langan', 'name': u'栏杆', 'children': []},
                {'id': 'louti', 'name': u'楼梯', 'children': []},
                {'id': 'bilu', 'name': u'壁炉', 'children': []},
            ]},
        ]},

        {'id': 'keting', 'name': u'客厅', 'children': [
            {'id': 'shafa', 'name': u'沙发', 'children': [
                {'id': 'duorenshafa', 'name': u'多人沙发', 'children': []},
                {'id': 'zuheshafa', 'name': u'组合沙发', 'children': []},
                {'id': 'danrenshafa', 'name': u'单人沙发', 'children': []},
                {'id': 'shuangrenshafa', 'name': u'双人沙发', 'children': []},
                {'id': 'shafayi', 'name': u'沙发椅', 'children': []},
                {'id': 'shafadeng', 'name': u'沙发凳', 'children': []},
            ]},
            {'id': 'ketingguilei', 'name': u'客厅柜类', 'children': [
                {'id': 'dianshigui', 'name': u'电视柜', 'children': []},
                {'id': 'xiegui', 'name': u'鞋柜', 'children': []},
                {'id': 'xuanguangui', 'name': u'门厅/玄关柜', 'children': []},
                {'id': 'jiugui', 'name': u'酒柜', 'children': []},
            ]},
            {'id': 'ketingjilei', 'name': u'客厅几类', 'children': [
                {'id': 'chaji', 'name': u'茶几', 'children': []},
                {'id': 'jiaojibianji', 'name': u'角几/边几', 'children': []},
                {'id': 'taoji', 'name': u'套几', 'children': []},
            ]},
            {'id': 'ketingjialei', 'name': u'客厅架类', 'children': [
                {'id': 'yimaojia', 'name': u'衣帽架', 'children': []},
                {'id': 'xiejia', 'name': u'鞋架', 'children': []},
                {'id': 'huajia', 'name': u'花架', 'children': []},
                {'id': 'gebanbijia', 'name': u'隔板/壁架', 'children': []},
                {'id': 'zazhibaokanjia', 'name': u'杂志/报刊架', 'children': []},
            ]},
            {'id': 'qita', 'name': u'其它', 'children': [
                {'id': 'dianshi', 'name': u'电视', 'children': []},
                {'id': 'chuanglian', 'name': u'窗帘', 'children': []},
                {'id': 'ditan', 'name': u'地毯', 'children': []},
                {'id': 'pingfenggeduan', 'name': u'屏风/隔断', 'children': []},
                {'id': 'majiangzhuo', 'name': u'麻将桌', 'children': []},
                {'id': 'aideng', 'name': u'矮凳', 'children': []},
            ]},
        ]},

        {'id': 'canting', 'name': u'餐厅', 'children': [
            {'id': 'canzhuoyi', 'name': u'餐桌椅', 'children': [
                {'id': 'canzhuo', 'name': u'餐桌', 'children': []},
                {'id': 'canyi', 'name': u'餐椅', 'children': []},
                {'id': 'canzhuoyizuhe', 'name': u'餐桌椅组合', 'children': []},
            ]},
            {'id': 'cantingguilei', 'name': u'餐厅柜类', 'children': [
                {'id': 'canbiangui', 'name': u'餐边柜', 'children': []},
                {'id': 'jiugui', 'name': u'酒柜', 'children': []},
            ]},
            {'id': 'qita', 'name': u'其它', 'children': [
                {'id': 'canju', 'name': u'餐具', 'children': []},
                {'id': 'bataibayi', 'name': u'吧台/吧椅', 'children': []},
            ]},
        ]},

        {'id': 'woshi', 'name': u'卧室', 'children': [
            {'id': 'chuanglei', 'name': u'床类', 'children': [
                {'id': 'chuang', 'name': u'床', 'children': []},
                {'id': 'danrenchuang', 'name': u'单人床', 'children': []},
                {'id': 'shuangrenchuan', 'name': u'双人床', 'children': []},
                {'id': 'shafachuang', 'name': u'沙发床', 'children': []},
                {'id': 'tatami', 'name': u'榻榻米', 'children': []},
            ]},
            {'id': 'woshiguilei', 'name': u'卧室柜类', 'children': [
                {'id': 'chuangtougui', 'name': u'床头柜', 'children': []},
                {'id': 'yigui', 'name': u'衣柜', 'children': []},
                {'id': 'dianshigui', 'name': u'电视柜', 'children': []},
                {'id': 'dougui', 'name': u'斗柜', 'children': []},
                {'id': 'jiaogui', 'name': u'角柜', 'children': []},
            ]},
            {'id': 'qita', 'name': u'其它', 'children': [
                {'id': 'chuanglian', 'name': u'窗帘', 'children': []},
                {'id': 'ditan', 'name': u'地毯', 'children': []},
                {'id': 'shuzhuangtai', 'name': u'梳妆台/桌', 'children': []},
                {'id': 'shuzhuangdeng', 'name': u'梳妆凳', 'children': []},
                {'id': 'huazhuangjing', 'name': u'化妆镜', 'children': []},
                {'id': 'chuangweideng', 'name': u'床尾凳', 'children': []},
                {'id': 'dianshi', 'name': u'电视', 'children': []},
            ]}, ]},

        {'id': 'shufang', 'name': u'书房', 'children': [
            {'id': 'shuzhuoyi', 'name': u'书桌椅', 'children': [
                {'id': 'shuzhuo', 'name': u'书桌', 'children': []},
                {'id': 'xieziyi', 'name': u'写字椅', 'children': []},
                {'id': 'diannaozhuo', 'name': u'电脑桌', 'children': []},
                {'id': 'shuzhuoyizuhe', 'name': u'书桌椅组合', 'children': []},
            ]},
            {'id': 'qita', 'name': u'其它', 'children': [
                {'id': 'shujia', 'name': u'书架', 'children': []},
                {'id': 'shugui', 'name': u'书柜', 'children': []},
                {'id': 'diannao', 'name': u'电脑', 'children': []},
                {'id': 'zazhibaokanjia', 'name': u'杂志/报刊架', 'children': []},
            ]},
        ]},

        {'id': 'chuwei', 'name': u'厨卫', 'children': [
            {'id': 'chufang', 'name': u'厨房', 'children': [
                {'id': 'chugui', 'name': u'橱柜', 'children': []},
                {'id': 'chufangpeijian', 'name': u'厨房配件/挂架', 'children': []},
                {'id': 'chuju', 'name': u'厨具', 'children': []},
                {'id': 'canju', 'name': u'餐具', 'children': []},
            ]},
            {'id': 'chufangdianqi', 'name': u'厨房电器', 'children': [
                {'id': 'chouyouyanji', 'name': u'抽油烟机', 'children': []},
                {'id': 'ranqizao', 'name': u'燃气灶', 'children': []},
                {'id': 'diancilu', 'name': u'电磁炉', 'children': []},
                {'id': 'weibolu', 'name': u'微波炉', 'children': []},
                {'id': 'reshuiqi', 'name': u'热水器', 'children': []},
                {'id': 'xiaodugui', 'name': u'消毒柜', 'children': []},
            ]},
            {'id': 'weiyu', 'name': u'卫浴', 'children': [
                {'id': 'zuobianqi', 'name': u'坐便器', 'children': []},
                {'id': 'yushigui', 'name': u'浴室柜', 'children': []},
                {'id': 'xiliantaipen', 'name': u'洗脸台盆', 'children': []},
                {'id': 'huasa', 'name': u'花洒', 'children': []},
                {'id': 'linyufang', 'name': u'淋浴房', 'children': []},
                {'id': 'yugang', 'name': u'浴缸', 'children': []},
                {'id': 'xiaobiandou', 'name': u'小便斗', 'children': []},
                {'id': 'weiyupeijian', 'name': u'卫浴配件/挂架', 'children': []},
                {'id': 'yuba', 'name': u'浴霸', 'children': []},
            ]},
        ]},

        {'id': 'ertongfang', 'name': u'儿童房', 'children': [
            {'id': 'ertongfang-xxx', 'name': u'儿童房', 'children': [
                {'id': 'ertongchuang', 'name': u'儿童床', 'children': []},
                {'id': 'gaodizimuchuang', 'name': u'高低/子母床', 'children': []},
                {'id': 'ertongyigui', 'name': u'儿童衣柜', 'children': []},
                {'id': 'ertongshuzhuo', 'name': u'儿童书桌', 'children': []},
                {'id': 'ertongyi', 'name': u'儿童椅', 'children': []},
                {'id': 'ertongshafa', 'name': u'儿童沙发', 'children': []},
                {'id': 'yinerchuang', 'name': u'婴儿床', 'children': []},
            ]},
        ]},

        {'id': 'dengshi', 'name': u'灯饰', 'children': [
            {'id': 'dengshi-xxx', 'name': u'灯饰', 'children': [
                {'id': 'diaodeng', 'name': u'吊灯', 'children': []},
                {'id': 'xidingdeng', 'name': u'吸顶灯', 'children': []},
                {'id': 'taideng', 'name': u'台灯', 'children': []},
                {'id': 'shedeng', 'name': u'射灯', 'children': []},
                {'id': 'tongdeng', 'name': u'筒灯', 'children': []},
                {'id': 'luodideng', 'name': u'落地灯', 'children': []},
                {'id': 'bideng', 'name': u'壁灯', 'children': []},
            ]},
        ]},

        {'id': 'jiashi', 'name': u'家饰', 'children': [
            {'id': 'jiajushipin', 'name': u'家居饰品', 'children': [
                {'id': 'pingfenggeduan', 'name': u'屏风/隔断', 'children': []},
                {'id': 'zhuangshijian', 'name': u'装饰摆件', 'children': []},
                {'id': 'zhaopianqiang', 'name': u'照片墙', 'children': []},
                {'id': 'zhuangshihua', 'name': u'装饰画', 'children': []},
                {'id': 'youhua', 'name': u'油画', 'children': []},
                {'id': 'huajia', 'name': u'花架', 'children': []},
                {'id': 'huaping', 'name': u'花瓶', 'children': []},
                {'id': 'yurgang', 'name': u'鱼缸', 'children': []},
            ]},
            {'id': 'buyiruanshi', 'name': u'布艺软饰', 'children': [
                {'id': 'chuanglian', 'name': u'窗帘', 'children': []},
                {'id': 'ditan', 'name': u'地毯', 'children': []},
                {'id': 'baozhen', 'name': u'抱枕', 'children': []},
                {'id': 'shafadian', 'name': u'沙发垫', 'children': []},
            ]},
            {'id': 'xianhuayuanyi', 'name': u'鲜花园艺', 'children': [
                {'id': 'zhiwupenjing', 'name': u'植物/盆景', 'children': []},
                {'id': 'huayitaozhuang', 'name': u'花艺套装', 'children': []},
            ]},
            {'id': 'jingzilei', 'name': u'镜子类', 'children': [
                {'id': 'shiyijing', 'name': u'试衣镜', 'children': []},
                {'id': 'huazhuangjing', 'name': u'化妆镜', 'children': []},
                {'id': 'yushijing', 'name': u'浴室镜', 'children': []},
            ]},
            {'id': 'qitajiashi', 'name': u'其它家饰', 'children': [

                {'id': 'yueqi', 'name': u'乐器', 'children': []},
                {'id': 'meishuyongpin', 'name': u'美术用品', 'children': []},
                {'id': 'tiyuqicai', 'name': u'体育器材', 'children': []},
            ]},
        ]},

        {'id': 'jiadian', 'name': u'家电', 'children': [
            {'id': 'bingxikong', 'name': u'冰/洗/空', 'children': [
                {'id': 'bingxiang', 'name': u'冰箱', 'children': []},
                {'id': 'xiyiji', 'name': u'洗衣机', 'children': []},
                {'id': 'kongtiao', 'name': u'空调', 'children': []},
            ]},
            {'id': 'yingyinshuma', 'name': u'影音数码', 'children': [
                {'id': 'dianshi', 'name': u'电视', 'children': []},
                {'id': 'yingyinshebei', 'name': u'影音设备', 'children': []},
                {'id': 'diannao', 'name': u'电脑', 'children': []},
            ]},
            {'id': 'chufangdianqi', 'name': u'厨房电器', 'children': [
                {'id': 'chouyouyanji', 'name': u'抽油烟机', 'children': []},
                {'id': 'ranqizao', 'name': u'燃气灶', 'children': []},
                {'id': 'diancilu', 'name': u'电磁炉', 'children': []},
                {'id': 'weibolu', 'name': u'微波炉', 'children': []},
                {'id': 'reshuiqi', 'name': u'热水器', 'children': []},
                {'id': 'xiaodugui', 'name': u'消毒柜', 'children': []},
            ]},
            {'id': 'qita', 'name': u'其它', 'children': [
                {'id': 'yinshuiji', 'name': u'饮水机', 'children': []},
            ]},
        ]},

        {'id': 'dingzhi', 'name': u'定制家具', 'children': [
            {'id': 'dingzhi-xxx', 'name': u'定制家具', 'children': [
                {'id': 'chugui', 'name': u'橱柜', 'children': []},
                {'id': 'zuheshafa', 'name': u'组合沙发', 'children': []},
                {'id': 'canzhuoyizuhe', 'name': u'餐桌椅组合', 'children': []},
                {'id': 'shuzhuoyizuhe', 'name': u'书桌椅组合', 'children': []},
            ]},
        ]},

        {'id': 'jiaju', 'name': u'全部家具', 'children': [
            {'id': 'chuanglei', 'name': u'床类', 'children': [
                {'id': 'chuang', 'name': u'床', 'children': []},
                {'id': 'danrenchuang', 'name': u'单人床', 'children': []},
                {'id': 'shuangrenchuan', 'name': u'双人床', 'children': []},
                {'id': 'gaodizimuchuang', 'name': u'高低/子母床', 'children': []},
                {'id': 'ertongchuang', 'name': u'儿童床', 'children': []},
                {'id': 'yingerchuang', 'name': u'婴儿床', 'children': []},
                {'id': 'shafachuang', 'name': u'沙发床', 'children': []},
                {'id': 'tatami', 'name': u'榻榻米', 'children': []},
            ]},
            {'id': 'shafa', 'name': u'沙发', 'children': [
                {'id': 'danrenshafa', 'name': u'单人沙发', 'children': []},
                {'id': 'shuangrenshafa', 'name': u'双人沙发', 'children': []},
                {'id': 'duorenshafa', 'name': u'多人沙发', 'children': []},
                {'id': 'zuheshafa', 'name': u'组合沙发', 'children': []},
                {'id': 'ertongshafa', 'name': u'儿童沙发', 'children': []},
            ]},
            {'id': 'guilei', 'name': u'柜类', 'children': [
                {'id': 'dianshigui', 'name': u'电视柜', 'children': []},
                {'id': 'yigui', 'name': u'衣柜', 'children': []},
                {'id': 'ertongyigui', 'name': u'儿童衣柜', 'children': []},
                {'id': 'chuangtougui', 'name': u'床头柜', 'children': []},
                {'id': 'canbiangui', 'name': u'餐边柜', 'children': []},
                {'id': 'shugui', 'name': u'书柜', 'children': []},
                {'id': 'chuwugui', 'name': u'储物柜', 'children': []},
                {'id': 'bigui', 'name': u'壁柜', 'children': []},
                {'id': 'dougui', 'name': u'斗柜', 'children': []},
                {'id': 'xiegui', 'name': u'鞋柜', 'children': []},
                {'id': 'jiugui', 'name': u'酒柜', 'children': []},
                {'id': 'menting', 'name': u'门厅/玄关柜', 'children': []},
                {'id': 'jiaogui', 'name': u'角柜', 'children': []},
            ]},
            {'id': 'zhuolei', 'name': u'桌类', 'children': [
                {'id': 'canzhuo', 'name': u'餐桌', 'children': []},
                {'id': 'canzhuoyizuhe', 'name': u'餐桌椅组合', 'children': []},
                {'id': 'shuzhuangtai', 'name': u'梳妆台/桌', 'children': []},
                {'id': 'shuzhuo', 'name': u'书桌', 'children': []},
                {'id': 'ertongshuzhuo', 'name': u'儿童书桌', 'children': []},
                {'id': 'shuzhuoyizuhe', 'name': u'书桌椅组合', 'children': []},
                {'id': 'diannaozhuo', 'name': u'电脑桌', 'children': []},
                {'id': 'bataibayi', 'name': u'吧台/吧椅', 'children': []},
                {'id': 'majiangzhuo', 'name': u'麻将桌', 'children': []},
            ]},
            {'id': 'yidengta', 'name': u'椅凳榻', 'children': [
                {'id': 'canzhuo', 'name': u'餐桌', 'children': []},
                {'id': 'canzhuoyizuhe', 'name': u'餐桌椅组合', 'children': []},
                {'id': 'shuzhuangtai', 'name': u'梳妆台/桌', 'children': []},
                {'id': 'shuzhuo', 'name': u'书桌', 'children': []},
                {'id': 'ertongshuzhuo', 'name': u'儿童书桌', 'children': []},
                {'id': 'shuzhuoyizuhe', 'name': u'书桌椅组合', 'children': []},
                {'id': 'diannaozhuo', 'name': u'电脑桌', 'children': []},
                {'id': 'bataibayi', 'name': u'吧台/吧椅', 'children': []},
                {'id': 'majiangzhuo', 'name': u'麻将桌', 'children': []},
            ]},
            {'id': 'jialei', 'name': u'架类', 'children': [
                {'id': 'yimaojia', 'name': u'衣帽架', 'children': []},
                {'id': 'xiejia', 'name': u'鞋架', 'children': []},
                {'id': 'shujia', 'name': u'书架', 'children': []},
                {'id': 'huajia', 'name': u'花架', 'children': []},
                {'id': 'bogujia', 'name': u'博古架', 'children': []},
                {'id': 'gebanbijia', 'name': u'隔板/壁架', 'children': []},
                {'id': 'zazhibaokanjia', 'name': u'杂志/报刊架', 'children': []},
            ]},
            {'id': 'jilei', 'name': u'几类', 'children': [
                {'id': 'chaji', 'name': u'茶几', 'children': []},
                {'id': 'jiaojibianji', 'name': u'角几/边几', 'children': []},
                {'id': 'taoji', 'name': u'套几', 'children': []},
            ]},
        ]},

    ]
}

keting_tag = {
    'no': '',
    'state': 1,
    'depth': 2,
    'area': 'keting',
    'name': u'客厅',
    'children': [
        {'name': u'沙发', 'children': [
            {'name': u'多人沙发'},
            {'name': u'单人沙发'},
            {'name': u'组合沙发'},
            {'name': u'双人沙发'},
            {'name': u'沙发椅'},
            {'name': u'沙发凳'}
        ]},
        {'name': u'客厅柜类', 'children': [
            {'name': u'电视柜'},
            {'name': u'鞋柜'},
            {'name': u'酒柜'},
            {'name': u'门厅/玄关柜'}
        ]},
        {'name': u'客厅几类', 'children': [
            {'name': u'茶几'},
            {'name': u'角几'},
            {'name': u'套几'}
        ]},
        {'name': u'客厅架类', 'children': [
            {'name': u'衣架帽'},
            {'name': u'鞋架'},
            {'name': u'花架'},
            {'name': u'笔架'},
            {'name': u'杂志/报刊架'}
        ]}
    ]
}

canting_tag = {
    'no': '',
    'state': 1,
    'depth': 2,
    'area': 'canting',
    'name': u'餐厅',
    'children': [
        {'name': u'餐桌椅', 'children': [
            {'name': u'餐桌'},
            {'name': u'餐椅'},
            {'name': u'餐桌椅组合'},

        ]},
        {'name': u'餐厅柜类', 'children': [
            {'name': u'餐边柜'},
            {'name': u'酒柜'},
        ]},
        {'name': u'其他', 'children': [
            {'name': u'餐具'},
            {'name': u'吧椅'},
        ]},

    ]
}

woshi_tag = {
    'no': '',
    'state': 1,
    'depth': 2,
    'area': 'woshi',
    'name': u'卧室',
    'children': [
        {'name': u'床类', 'children': [
            {'name': u'床'},
            {'name': u'单人床'},
            {'name': u'双人床'},

        ]},
        {'name': u'卧室柜类', 'children': [
            {'name': u'柜门'},
            {'name': u'床头柜'},
            {'name': u'衣柜'},
            {'name': u'电视柜'},
            {'name': u'交柜'},
        ]},
        {'name': u'其他', 'children': [
            {'name': u'窗帘'},
            {'name': u'地毯'},
            {'name': u'梳妆台'},
        ]},

    ]
}

shufang_tag = {
    'no': '',
    'state': 1,
    'depth': 2,
    'area': 'shufang',
    'name': u'书房',
    'children': [
        {'name': u'书桌椅', 'children': [
            {'name': u'书桌'},
            {'name': u'写字椅'},
            {'name': u'电脑桌'},
            {'name': u'电脑桌组合'},
            {'name': u'躺椅'}

        ]},

        {'name': u'其他', 'children': [
            {'name': u'书架'},
            {'name': u'书柜'},
            {'name': u'电脑'},
        ]},

    ]
}

ertongfang_tag = {
    'no': '',
    'state': 1,
    'depth': 2,
    'area': 'ertongfang',
    'name': u'儿童房',
    'children': [
        {'name': u'儿童房', 'children': [
            {'name': u'儿童床'},
            {'name': u'高低/母子床'},
            {'name': u'儿童衣柜'},
            {'name': u'儿童书桌'},
            {'name': u'儿童玩具'},
            {'name': u'儿童沙发'},
            {'name': u'婴儿床'}
        ]},
    ]
}

# noes = ['a312ff2b9b5946fc839437043e377702', 'f65c05b446004f93a6c162b13c2e5a71', '76dfd87e7d4849d3b41bfac8d6175a9a',
#         '7d0774102352493c94511bad29eb2572', '29559980efce4f7a88fa80afe5a0b675', '8e56ad89c07e4cf2af959bf88f828a6b',
#         '8e56ad89c07e4cf2af959bf88f828a6b', '6c992da5a7554beba21e47b60da218e0', '8bdb389e3af3423ba4ae81ccfa54927d',
#         '7574825e90684b36b456d85b131f9cf8', 'b7634e4938bb4e708db4b0c5d7785c94', 'd93253e4e9244a9f84d86c82d007ea55',
#         'f2f467a97f5f4f72b7222e53a9e0dd0a', '3749b1f98f594bcb86b1109cd4ff7435', 'bb2745f56a974eecab75574906124372',
#         '1f295b0ba7cc4511b95f2261262a2e2c', '68ed671b9ac445279bf2762863484f59', 'b9b1a60cc86d4dbea264ba0a91343277',
#         'c50170b843d54f7cae3abef464a2ad04', 'e2b71a1d8f80460593229c4a022c69b8']
NOes =[]

item_sample = {
    "length": 108,
    # "top_url": "http://1jbest-3d-img.img-cn-hangzhou.aliyuncs.com/ifuwo/item/15ebce643ad511e7b25300163e0026b6/top.png",
    "cargo_no": "中式风格吊灯DS20170517",
    "sku_id": "",
    "render_state": 3,
    "describe": "",
    "discount_price": 0,
    "system_type": 0,
    "direct_scalable": 1,
    "unit": 1,
    "merchant": ['ifuwo', '1jbest', 'longfa'],
    "user_id": 939,
    "no": "15ebce643ad511e7b25300163e0026b6",
    "product_length": 58.4202805,
    "salable": 0,
    "state": 0,
    "sub_type": 106,
    "product_price": 0,
    "width": 108,
    "product_name": "NO.7652中式风格吊灯DS20170517",
    "status": 40,
    "material": "",
    "scalable": 1,
    "lightable": 1,
    "product_brand": "非商品模型",
    "photo_degree": 45,
    "is_public": 1,
    "sale_count": 0,
    "inner_type": 1,
    "product_id": "",
    # "customizable": 0,
    "product_width": 58.4202766,
    "product_link": "",
    "preview_fpath": "ifuwo/1705/17/419073763adf11e7879200163e0026b6.jpg",
    # "preview_url": "http://1jbest-3d-img.img-cn-hangzhou.aliyuncs.com/ifuwo/1705/17/419073763adf11e7879200163e0026b6.jpg",
    "height": 98,
    "flat_height": 98.3741455,
    "product_height": 98.3741455,
    # "author_id": 1,
    "group_id": "",
    "photo_scale": 1.4,
}

EMPTY_IMG_FPATH = 'common/empty.jpg'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/data/media/fuwo/upload/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = 'http://img.fuwo.com/'
# MEDIA_URL = 'http://img-test.fuwo.com/'
MEDIA_URL = 'http://1jbest-3d-img.img-cn-hangzhou.aliyuncs.com/'

CATEGORY_ids = range(159,232)

CATEGORY_NOES = '9b7fdd0c9d6047e28fa3c4f8d444c224 \
,9af520371a294577b78a2e012abdf7d1 \
,e68b87b544ac4816b4cdd6fda31b7a6d \
,66aa2b74a33c42079487d70122002b6a \
,e4fda885c77f4e969b406f5aa2d22164 \
,7baf562948d246b58c15d5276fc70adf \
,db4cca558c334232a2547efee129c8a4 \
,39c16527418c4668871b1162831d4298 \
,bb38e1cd56244e628f1e2a6f516fff2e \
,833b4c4d46304ef19eb14afa3190d786 \
,b6c37a8ee6074e7ca0170753bb4a944f \
,ef57cb35dec9458b8e5751567e2d61e0\
,63c67abbeedd41a4b31c2041d55f27b7\
,a7ac158992a24f069053446d008047f5\
,0eb40f0b8a194f788511334332c6ee3c\
,3360925bdde949539ecffeeec6340093\
,f48a2fa443bc47059a9ae49d7795ea98\
,f40e250f5fde4b6c8543ae42668a6b07\
,228ac86a270f47caadbc3eb6ac399368\
,0e6ffb0ec99e406ba2be332c764bc8bc\
,2628fca95fc340d5bee70da68d7ecb05\
,9820613cca5f4ae7a3cb1bf1a707228b\
,d904c9311bdd4b11a47b5b22e82a14e8\
,021a61d608ad4881b21a448ebbe92187\
,db7c2c7fd3674c118f6cca55f62fba59\
,90e5520a70574833b2c0668832f5f00a\
,0169ddd49b1e4a68a40ad6f61c8b7611\
,15c0bf45ee1b4141a3571695bd1f6045\
,9bf632e994b14b43be667518c1dcd692\
,05c450b5ea26446a80443a17edc60e88\
,d13edb587279452fa4dc101874b0cda5\
,cca575f849f045d8acb2bd8ccae87ee5\
,dd41e9fb482540879c91c55e3550ae17\
,761fa23cb46d48eaa0a1d5059eda8337\
,3825da30d26449e8911d13ebe61bbd04\
,dca80f3e45a847a9ab268406a4dccd66\
,87459bdb639745eebbe7ead4b13bef87\
,ae93cf6aa60d421a9b05997e5f17ca83\
,74183d98e7eb4dd89b8cddace454ba22\
,1aa379d763324de2a93a000a5243156e\
,bc459efbd51b4fa0b1ceed354afd7e9b\
,16e15a50639c41e39b2ec8d59bb2d5e8\
,32573af21d37431cb6d0c3d41938b363\
,9ea28d2c98b84482bec2aa0a6d11b698\
,652225241f6e43528568ea613a0187e5\
,a99194ef95a94c5d938eb2bab6bc94e0\
,15c2a2f14e9e4d369f6d0db0411f43b2\
,f5a022724d214566bbc5d3a33b340580\
,646b03ad24ab4f8782c1581972907660\
,49e8612359e248348c526ed84b356cb2\
,ea9e6a49b0a34a46b253e8632aaae084\
,7e552f08fa5042e5b8605dde962df3c7\
,9a35740fb30b4989b4f589388077169c\
,0683bc19ecba41f5a09e656a43d67c54\
,1ac4fb8695c14a5892ad99620f144f23\
,9096ba62565b4f5eab283b1678e0b546\
,93197d3f61d947b7b0907793c95cff45\
,c40a0e9c68c14cce860312aaff413b11\
,63252dc35fb447b1bf439da9fb38acea\
,e1f1330b19854598999e637c2c294b26\
,824a1c5b63dd4a42a85fdec3366fdcb5\
,1218a36a02864cdba0f423fb08403ca3\
,40e6a0f998f4461d8bed0d4fcab26379\
,c1b1fca8b64e4f9dbabb6eeb0832d460\
,80f3199c6dfc43888d2f3b8e437b5ed4\
,fd76d8612afb410ba068c0740106b0ec\
,97b02cd5fb9c43059cc1fb167a152ab1\
,36f3a47e490a453387f89a3f6ebfc380\
,ded427efc4dd487bb96280934921e9d9\
,145136ec0171484a8a0f13342e33dd4d\
,3cc18f16c1934787a264a1635f1469e5\
,09a63e903cae4a2aadf2ce8261e7e83a\
,205f35a8396f42cb8559372e09aa6496'