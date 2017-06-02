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
# list_CATEGORY_NOES = CATEGORY_NOES.split(',')


def get_item_nos(begin=290980, count=1000):
    conn = MySQLdb.connect(**DATABASE)
    curs = conn.cursor()
    sql = "SELECT no FROM myfarm_item where id > {} limit {}".format(begin, count)
    count = curs.execute(sql)
    result = curs.fetchall()
    return count, result


def init_itemcategory_all(begin):
    result = True
    while result:
        result = init_itemcategory(begin, 1000)
        begin = begin + 1000


def init_itemcategory(begin=290980, count=1000):
    count, result = get_item_nos(begin=begin, count=count)
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


if __name__ == '__main__':
    # init_itemcategory(begin=290997, count=10)
    init_itemcategory_all(begin=290997)
