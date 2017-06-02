# coding:utf-8

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.gen

from tornado.options import options, define

define("port", default=8001, help="跑在8001", type=int)

import time


class SleepHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        # 使用yield得到了一个生成器，先把流程挂起，等完全完毕，再唤醒继续执行。另，生成器都是异步的。
        yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 5)
        self.write("this is SleepHandler...")


class DirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("this is DirectHandler...")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/d", DirectHandler),
            (r"/s", SleepHandler),
        ],
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()
