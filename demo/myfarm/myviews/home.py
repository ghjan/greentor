#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author magic, create Date: 5/16/17
"""
import tornado
import tornado.web
import tornado.gen
import tornado.ioloop
import functools
from .base import BaseHandler
import time
import tornado.concurrent
import datetime
from myfarm.mymodels.mongo import *
from concurrent.futures import ThreadPoolExecutor


class Executor(ThreadPoolExecutor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=10)
        return cls._instance


class OtherHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.redirect('/')     # Http redirect
        # raise tornado.web.HTTPError(status_code=404, log_message='not found')


class HomeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        # self.write('hello world!')
        pagers = Page.objects.all()

        comments = []
        for page in pagers:
            for content in page.comments:
                content = content['content']
                print(content)
                comments.append(str(content))
        print(comments)
        self.render('index.html', error=comments)

        # print " ok "
        # self.finish('It work!')


class AsyncHomeHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # self.write('hello world!')
        # self.render('index.html', error='123')
        tornado.ioloop.IOLoop.instance().add_timeout(0, callback=functools.partial(self.test, 'magic_test'))
        self.finish('It work!')

    def test(self, params):
        time.sleep(10)
        print(params)


class AsyncTaskHandler(BaseHandler):
    """
    when we need the result of async task to do something with the result,
    we need write tornado task just like this.
    for example:
    """
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # yield result
        response = yield tornado.gen.Task(self.test, 'magic task test')
        print("response:{}".format(response))

        self.finish('jas')

    @tornado.gen.coroutine
    def test(self, params):
        time.sleep(2)
        return params


class FutureHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        params = 'magic future test'
        tornado.ioloop.IOLoop.instance().add_callback(functools.partial(self.test, params))

        self.finish('futurexxxxxxxxxx')

    @tornado.concurrent.run_on_executor
    def test(self, params):
        time.sleep(10)
        print(params)


class FutureResponseHandler(tornado.web.RequestHandler):
    excutor = Executor()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        params = 'future params'
        future = Executor().submit(self.test, params)

        response = yield tornado.gen.with_timeout(datetime.timedelta(10), future)

        if response:
            print('response', response.result())

    @tornado.concurrent.run_on_executor
    def test(self, params):
        return params