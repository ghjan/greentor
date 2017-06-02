# encoding: utf-8

from django.db import connection
import random

def execute_query(cursor, query, params={}, fetchall=True):
    """function: SQL 执行"""
    cursor.execute(query, params)
    if fetchall:
        result = cursor.fetchall()
    else:
        result = cursor.fetchone()
    return result

def ids_str2int(ids):
    """ 格式化 str ids -> int """
    try:
        return [int(str_id) for str_id in ids]
    except:
        return []
    

def order_by_str(order):
    '''转化Orderby字符串'''
    
    if order.startswith('-'):
        return '%s DESC' % order[1:]
    return '%s ASC' % order

def execute_fetchone(query, params={}, cursor=None, close_cursor=False):
    if not cursor:
        cursor = connection.cursor()
        
    cursor.execute(query, params)
    row = cursor.fetchone()
    desc = [col[0] for col in cursor.description]
    
    if close_cursor:
        cursor.close()
    
    return dict(zip(desc, row))

def create_random_id_by_table(table_name, min_add=4, max_add=20):
    """根据表最大ID创建一个随机ID"""
    query = "SHOW TABLE STATUS LIKE '%s'" % table_name
    status = execute_fetchone(query, close_cursor=True)
    
    auto_increment = status['Auto_increment']
    # 增长值：4~20
    add_num = random.randint(min_add, max_add)
    
    return auto_increment + add_num
    