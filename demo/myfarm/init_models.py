# coding: utf-8

from __future__ import unicode_literals

from models import *
from myfarm.settings import *

def create_category_top(top_tag, parent_id):
    ertongfang = top_tag.get('children', None)
    depth = 1
    create_category(ertongfang, parent_id, depth)


def create_category(data, parent_id, depth):
    if type(data) in (list, tuple, set):
        if len(data) == 1:
            data = data[0]
        else:
            for item in data:
                create_category(item, parent_id, depth)
            return
    try:
        tag = {
            'no': generate_uuid(),
            'state': 1,
            'depth': depth,
            'alias_name': data['name'],
            'name': data['name'],
            'parent_id': parent_id,
        }
        category, created = Category.objects.get_or_create(**tag)
    except:
        print("data:{}, parent_id:{}, depth:{}".format(data, parent_id, depth))
    parent_id2 = category.id if category else 0

    children = data.get('children', None)
    if children:
        depth += 1
        for child in children:
            create_category(child, parent_id2, depth)


def generate_all_categories():
    categorys_tags = ITEM_TAG_SETS['AREA_TAGS']
    import json
    used_tags = [keting_tag, canting_tag, woshi_tag, shufang_tag, ertongfang_tag]
    dict_used_tags = dict()
    for tag in used_tags:
        dict_used_tags.update({tag['name']: {'tag': tag}})
    for data in categorys_tags:
        tag = {
            'no': generate_uuid(),
            'state': 1,
            'depth': 1,
            'alias_name': data['id'],
            'name': data['name'],
        }
        category, created = Category.objects.get_or_create(**tag)
        if data['name'] in dict_used_tags.keys():
            dict_used_tags[data['name']].update({'id': category.id})
    for name, dict_value in dict_used_tags.iteritems():
        create_category_top(dict_value['tag'], dict_value['id'])


        # for i in range(5000000):
        #     item = item_sample
        #     item['no'] = generate_uuid()
        #     item['category'] = random.sample(noes, 5)
        #
        #     print(item['no'], item['category'][0])
        #     Item(**item).save()

def generate_item(count=5):
    global NOes
    if not NOes:
        all_noes = Category.objects.only("id") #.filter(state__in=(StateEnum.VALID, StateEnum.TEMPORARY) )
        NOes =[cat.id for cat in all_noes]
    for i in range(count):
        item = item_sample
        # print("item:{}".format(item))
        item['no'] = generate_uuid()
        category_ids = random.sample(NOes, random.randint(2,5))
        # print("item_no:{}, category_ids:{}".format(item['no'],category_ids))
        Item(**item).save()
        for category_id in category_ids:
            item_cat = {'category_id': int(category_id) ,
                                    'item_no': item['no']}
            itemCat = ItemCategory(**item_cat)

            itemCat.save()


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

    # generate_all_categories()

    generate_item(5000000)