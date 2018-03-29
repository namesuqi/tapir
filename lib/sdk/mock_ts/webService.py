# coding=utf-8
# author: Pan Pan
# 根据配置返回get请求，来模拟TS的响应

import tornado
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self, temp_url):
        with open("jsontext.txt", "r") as fh:
            ret_json = fh.readline()
        self.write(ret_json)


def start_service(port):
    application = tornado.web.Application([
        (r"/(.*)", MainHandler),
    ])
    application.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_service(80)
