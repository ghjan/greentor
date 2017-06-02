#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author david, create Date: 5/20/17
"""
# import MySQLdb
import torndb
import random
from myfarm.settings import ITEM_TAG_SETS, ITEM_CATEGORY_SET, item, noes
import uuid
from datetime import datetime


# connect(**settings.DATABASE)
DATABASE = dict(
    db='testdb',
    host='192.168.4.94:3306',
)
dbconn = torndb.Connection(DATABASE.host,DATABASE.db,user='root',password='123456')


def generate_uuid():
    uuid_str = str(uuid.uuid4())
    return uuid_str.replace('-', '')

STATE_CHOICE = (
    (0, 'valid'),
    (1, 'temp valid'),
    (9, 'delete')

)


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
    INITIAL = 0         # not convert
    PENDING_CONVERT = 10  # converting
    CONVERTING = 20       # convert failed
    CONVERT_FAILED = 30   # converted

UNREAL_STATUS_CHOICES = (
    (UnrealStatusEnum.INITIAL,        "not convert"),
    (UnrealStatusEnum.PENDING_CONVERT,  "converting"),
    (UnrealStatusEnum.CONVERTING,    "convert failed"),
    (UnrealStatusEnum.CONVERT_FAILED,    "converted"),
)


class BoolNumberEnum(object):
    NO = 0
    YES = 1
BOOL_NUMBER_CHOICES = (
    (BoolNumberEnum.NO, 'No'),
    (BoolNumberEnum.YES, 'Yes'),
)


class Auth(Document):
    no = StringField(required=True, max_length=32)
    mac_address = StringField(max_length=64)
    remote_ip = StringField(max_length=64)
    create_time = DateTimeField(default=datetime.now(), required=True)
    modify_time = DateTimeField(default=datetime.now(), required=True)


class Merchant(EmbeddedDocument):
    no = StringField(required=True, max_length=32)
    name = StringField(max_length=64)
    url = URLField()
    app_no = IntField(default=0)
    domain = StringField(max_length=128)
    farm_domain = StringField(max_length=128)
    spec = StringField(max_length=256)


class Unreal(EmbeddedDocument):
    no = StringField(required=True, max_length=32)
    platform = StringField(max_length=128)
    status = IntField(choices=UNREAL_STATUS_CHOICES, default=UnrealStatusEnum.INITIAL)
    real_type = IntField(choices=UNREAL_TYPE_CHOICES)
    filename = StringField(max_length=128)
    is_exist = IntField(choices=BoolNumberEnum, default=BoolNumberEnum.NO)


# class Item(Document):
#
#     no = StringField(required=True, max_length=32)
#     state = IntField(default=0, choices=STATE_CHOICE)
#     width = FloatField()
#     height = FloatField()
#     length = FloatField()
#     merchant = ListField(StringField(max_length=30))
#     model_flag = DictField()
#     product_name = StringField(required=True, max_length=128)
#     user_fuwo = IntField(default=0)
#     author_fuwo = IntField(default=0)
#     create_time = DateTimeField(default=datetime.now(), required=True)
#     modify_time = DateTimeField(default=datetime.now(), required=True)
#
#     model_user = ReferenceField(Auth)
#     merchant = ListField(EmbeddedDocumentField(Merchant))
#     unreal = ListField(EmbeddedDocumentField(Unreal))

class Item(DynamicDocument):

    no = StringField(required=True, max_length=32)
    state = IntField(default=0, choices=STATE_CHOICE)
    width = FloatField()
    height = FloatField()
    length = FloatField()
    merchant = ListField(StringField(max_length=30))
    product_name = StringField(required=True, max_length=128)
    user_id = IntField(default=0)
    author_id = IntField(default=0)
    create_time = DateTimeField(default=datetime.now(), required=True)
    modify_time = DateTimeField(default=datetime.now(), required=True)

    model_user = ReferenceField(Auth)


class Category(DynamicDocument):
    no = StringField(required=True, max_length=32)
    state = IntField(default=0, choices=STATE_CHOICE)

""" this is my test to test document EmbeddedDocument """
###


class Comment(EmbeddedDocument):
   content = StringField()


class Page(Document):
  comments = ListField(EmbeddedDocumentField(Comment))

if __name__ == '__main__':

    # item = Item(no=generate_uuid(), width=12, height=10, length=10, merchant=['ifuwo', '1jbest', 'yunchao'])
    # item.save()
    # item = Item()
    # item.no = generate_uuid()
    # item.product_name = 'test'
    # print item.no
    # item.save()
    #  model_flag={'octane': 1, 'max': 0, 'model': 1}).save()
    # comment1 = Comment(content='Good work magic, please continue !')
    # comment1.save()
    # comment2 = Comment(content='This is my mongodb orm test, it is nice')
    # page = Page(comments=[comment1, comment2]).save()
    # categorys_tags = ITEM_TAG_SETS['AREA_TAGS']
    # import json
    #
    # for data in categorys_tags:
    #     if data['name'] == u'儿童房':
    #         tag = {
    #             'no': generate_uuid(),
    #             'state': 1,
    #             'depth': 1,
    #             'area': data['id'],
    #             'name': data['name'],
    #             'children': [
    #                 {'name': u'儿童房'},
    #             ]
    #         }
    #         category = Category(**tag).save()
    for i in range(5000000):
        item = item
        item['no'] = generate_uuid()
        item['category'] = random.sample(noes, 5)

        print(item['no'], item['category'][0])
        Item(**item).save()

