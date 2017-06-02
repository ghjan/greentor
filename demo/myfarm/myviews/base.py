#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author magic, create Date: 5/16/17
"""
import tornado.web
import concurrent.futures
import tornado

executor = concurrent.futures.ThreadPoolExecutor(2)


class BaseHandler(tornado.web.RequestHandler):
    pass