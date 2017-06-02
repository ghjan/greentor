#!/usr/bin/env python
#coding: utf-8

'''
Created on 2016-07-05

@author: butter
'''
import requests
import oss2

from django.conf import settings

class Session(oss2.http.Session):
    def __init__(self):
        self.session = requests.Session()
        psize = 10
        self.session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=psize, pool_maxsize=psize, max_retries=10))
        self.session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=psize, pool_maxsize=psize, max_retries=10))

auth = oss2.Auth(settings.ALIYUN_ACCESS_KEY_ID, settings.ALIYUN_ACCESS_KEY_SECRET)
oss_media_bucket = oss2.Bucket(auth, settings.OSS_BUCKET_ENDPOINT, settings.OSS_MEIDA_BUCKET_NAME)
oss_store_bucket = oss2.Bucket(auth, settings.OSS_BUCKET_ENDPOINT, settings.OSS_STORE_BUCKET_NAME)

farm_auth = oss2.Auth(settings.ALIYUN_FARM_KEY_ID, settings.ALIYUN_FARM_KEY_SECRET)
oss_farm_bucket = oss2.Bucket(farm_auth, settings.OSS_FARM_BUCKET_ENDPOINT, settings.OSS_FARM_BUCKET_NAME)
