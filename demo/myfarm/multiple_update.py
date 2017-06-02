# coding: utf-8
from __future__ import unicode_literals

import MySQLdb

import random
import uuid
from datetime import datetime
import traceback

from myfarm.settings import *

DATABASE = dict(
    host='192.168.4.94',
    user='user',
    passwd='AzMNTOk%',
    db='testdb'
)
DATABASE_source = dict(
    host='192.168.2.133',
    user='user',
    passwd='AzMNTOk%',
    db='fuwo'
)
# list_CATEGORY_NOES = CATEGORY_NOES.split(',')


def get_data_from_source():
    conn = MySQLdb.connect(**DATABASE_source)
    curs = conn.cursor()
    sql = "select ic.item_no, group_concat(cast(ic.category_id as CHAR )), ii.product_name \
        from ifuwo_itemcategory ic left join ifuwo_ifuwoitem ii on ic.item_no=ii.no \
        where item_no<>'' and product_name is not null group by item_no order by item_no"
    count = curs.execute(sql)
    result = curs.fetchall()
    return count, result

def update_target_data(begin=10, count=1000):
    count, result = get_item_nos(begin=10, count=1000)
    if not result:
        return False
    L = []
    for row in result:
        item_no = row[0]
        category_ids = random.sample(CATEGORY_ids, random.randint(2, 4))
        # print("item_no:{}, category_ids:{}".format(item_no,category_ids))
        for category_id in category_ids:
            L.append((item_no, category_id))
    conn = MySQLdb.connect(**DATABASE)
    curs = conn.cursor()
    try:
        curs.executemany("insert into myfarm_itemcategory (item_no, category_id) values(%s,%s)", L)
        conn.commit()  # 没有提交的话，无法完成插入
    except:
        conn.rollback()
        traceback.print_exc()
        print('exception, begin:{}, count:{}'.format(begin, count))
        conn.close()
        return False
    finally:
        conn.close()
    return True

def get_item_nos(begin=10, count=1000):
    conn = MySQLdb.connect(**DATABASE)
    curs = conn.cursor()
    sql = "SELECT no FROM myfarm_item where id > {} limit {}".format(begin, count)
    count = curs.execute(sql)
    result = curs.fetchall()
    return count, result

def init_test(begin):
    result = True
    count_source, data_source = get_data_from_source()
    dict_item = dict()

    for row in data_source:
        lst_catid = list(set(row[1].split(',')))
        dict_item.update({row[0]:{'name':row[2],'cat':lst_catid}})
    while result:
        result = init_itemcategory(begin, count_source, dict_item)
        begin = begin + result


def init_itemcategory_all(begin):
    result = True
    count_source, data_source = get_data_from_source()
    dict_item = dict()

    for row in data_source:
        lst_catid = list(set(row[1].split(',')))
        dict_item.update({row[0]:{'name':row[2],'cat':lst_catid}})
    while result:
        result = init_itemcategory(begin, count_source, dict_item)
        begin = begin + result

def init_itemcategory(begin, count_source, dict_item):
    count, result = get_item_nos(begin=begin, count=count_source)
    if not result:
        return False
    i = 0
    lst_item_target = []
    lst_item = []
    lst_item_cat = []
    for k, v in dict_item.iteritems():
        if i< count:
            item_no_target = result[i][0]
            lst_item_target.append(item_no_target)
            lst_item.append((v['name'], item_no_target)) # product_name, item_no
            for c in v['cat']:
                lst_item_cat.append((item_no_target, c)) # item_no, category_id
            i += 1

    conn = MySQLdb.connect(**DATABASE)
    curs = conn.cursor()
    try:
        curs.execute('set names utf8')
        curs.executemany("update myfarm_item set product_name=%s where no=%s", lst_item)
        # first remove old records
        curs.execute("delete from myfarm_itemcategory where item_no in('{}')".format("','".join(lst_item_target) ))
        curs.executemany("insert into myfarm_itemcategory (item_no, category_id) values(%s,%s)", lst_item_cat)

        conn.commit()  # 没有提交的话，无法完成插入
    except:
        conn.rollback()
        traceback.print_exc()
        print('exception, begin:{}, count:{}'.format(begin, count))
        conn.close()
        return False
    finally:
        conn.close()
    return count


if __name__ == '__main__':
    # init_test(210)
    begin = 9355
    init_itemcategory_all(begin)