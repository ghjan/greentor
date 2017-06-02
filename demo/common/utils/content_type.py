# coding: utf-8
#__author__ = 'chang'
#__create__ = '14-11-13'

from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType

CONTENT_TYPE_KEY_PREFIX = 'django.content_type'
CONTENT_TYPE_TIMEOUT = 7*24*60*60

def make_content_type_key(app_label,model):
    '''生成content type 缓存key'''
    return '%s.%s.%s' %(CONTENT_TYPE_KEY_PREFIX,app_label,model)

def get_content_type_cache(app_label,model):
    '''django content type 缓存 '''
    content_type = cache.get(make_content_type_key(app_label,model))

    if not content_type:
        try:
            content = ContentType.objects.get(app_label=app_label,model=model)
            content_type = {
                'id':content.id,
                'name':content.name
            }
        except ContentType.DoesNotExist:
            content_type = None

        cache.set(make_content_type_key(app_label,model),content_type,CONTENT_TYPE_TIMEOUT)

    return content_type

def get_objects_by_contenttype_ids(content_type_id, ids, fields=None):
    """通过content_type_id及对象ids取对象"""
    contenttype = ContentType.objects.get(id=content_type_id)
    model       = contenttype.model_class()
    if fields:
        objects = model.objects.only(*fields).filter(id__in=ids)
    else:
        objects = model.objects.filter(id__in=ids)
    return objects
    