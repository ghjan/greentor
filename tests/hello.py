# coding: utf-8

from greentor import green
# green.enable_debug()
from greentor import mysql

mysql.patch_pymysql()

import pymysql

pymysql.install_as_MySQLdb()

import MySQLdb

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("host", default='localhost', help="run on the given host", type=str)

db_options = {
    'user': 'user',
    'passwd': 'AzMNTOk%',
    'db': 'testdb',
    'host': '192.168.4.94',  # ''localhost',
    'port': 3306,
    'charset': 'utf8'
}


# user='root',
#       passwd='',
#       db='test',
#       host='localhost',
#       port=3306,
#       charset='utf8'
class MainHandler(tornado.web.RequestHandler):
    @green.green
    def get(self):
        connect = MySQLdb.connect(**db_options)
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM app_blog LIMIT 1')
        result = cursor.fetchone()
        cursor.close()
        connect.close()
        self.finish(u'<p>{}</p><p>{}</p>'.format(result[1], result[2]))


pool = mysql.ConnectionPool(mysql_params=db_options)


class ConnectionPoolHandler(tornado.web.RequestHandler):
    @green.green
    def get(self):
        connect = pool.get_conn()
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM app_blog LIMIT 1')
        result = cursor.fetchone()
        cursor.close()
        pool.release(connect)
        self.finish(u'<p>{}</p><p>{}</p>'.format(result[1], result))


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([(r"/", MainHandler),
                                           (r"/pool/", ConnectionPoolHandler)]
                                          ,debug=False
                                          )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


def main_process():
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/pool/", ConnectionPoolHandler)
        ],
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    # main()
    # main_process()
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/pool/", ConnectionPoolHandler)
        ],
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()