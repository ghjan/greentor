# coding: utf-8
#__author__ = 'chang'
#__create__ = '14-11-19'
from django.core.cache import cache
from django.db import connection,transaction

VISIT_COUNT_KEY_PREFIX = 'visit_count'
VISIT_COUNT_TIMEOUT = 7*24*60*60

def make_visit_count_key(app_label, model, id):
    '''
    生成访问量 缓存key
    '''
    return '%s.%s.%s.%s' % (VISIT_COUNT_KEY_PREFIX,app_label,model,id)


def get_visit_count_cache(app_label, model, id):
    '''获取增量访问数缓存'''
    visit_count = cache.get(make_visit_count_key(app_label, model, id))
    if not visit_count:
        visit_count = 0
        set_visit_count_cache(app_label, model, id, visit_count)
    return visit_count

def delete_visit_count(app_label, model, id):
    '''删除增量访问数缓存'''
    cache.delete(make_visit_count_key(app_label, model, id))

def set_visit_count_cache(app_label, model, id, visit_count):
    '''设定增量访问数缓存'''
    cache.set(make_visit_count_key(app_label, model, id), visit_count, VISIT_COUNT_TIMEOUT)

def add_visit_count_cache(model_class, id, visit=1):
    '''function : 更新访问数量 '''
    app_label = model_class._meta.app_label
    model_name = model_class._meta.module_name
    visit_count = get_visit_count_cache(app_label, model_name, id)
    visit_count += visit
    set_visit_count_cache(app_label, model_name, id,visit_count)
    return visit_count

VISIT_COUNT_UPDATE_RATE = 50
def get_visit_count(model_class, id):
    '''获取增量缓存，超过50写入数据库'''
    app_label = model_class._meta.app_label
    model_name = model_class._meta.module_name
    visit_count = get_visit_count_cache(app_label, model_name, id)
    update_db = False
    if visit_count >= VISIT_COUNT_UPDATE_RATE:
        visit_count = 0
        update_visit_count_db(model_class, VISIT_COUNT_UPDATE_RATE, id)
        set_visit_count_cache(app_label, model_name, id, visit_count)
        update_db = True
    return visit_count, update_db


def update_visit_count_db(model_class, count, id):
    '''同步数据库数据'''
    table_name = model_class._meta.db_table
    try:
        update_query = '''UPDATE %s SET visit_count=visit_count+%s WHERE id=%s ''' % (table_name, count, id)
        cursor = connection.cursor()
        cursor.execute(update_query)
        transaction.commit_unless_managed()
        cursor.close()
    except:
        pass
