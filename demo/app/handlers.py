# coding: utf-8

import tornado.web

from core.handlers import BaseRequestHandler
from .models import Blog


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world ! \n')


class BlogHandler(BaseRequestHandler):
    def get(self, pk=None):
        if pk is None:
            blog = Blog.objects.first()
        else:
            blog = Blog.objects.get(id=pk)
        self.finish(blog.content)
