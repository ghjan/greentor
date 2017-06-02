#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author magic, create Date: 5/15/17
"""
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print("listening at 127.0.0.1:8888...")
    tornado.ioloop.IOLoop.current().start()