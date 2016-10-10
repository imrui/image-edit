# -*- coding: utf-8 -*-
import os.path
import uuid
import tornado
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from handlers.site_handler import SiteHandler


define('debug', default=True, type=bool)
define('port', default=8080, type=int, help='run on the given port')


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', SiteHandler, {'path': os.path.join(os.path.dirname(__file__), 'static/starter.html')}),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=False,
            cookie_secret='VAgYv0fQ5KLKdVUH7OlGHUTkOq9DZbSY',
        )
        if not options.debug:
            settings['cookie_secret'] = str(uuid.uuid4())
        settings.update(options.as_dict())
        super(Application, self).__init__(handlers, **settings)


def main():
    tornado.options.parse_command_line()
    if options.debug:
        tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__), 'development.conf'))
    else:
        tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__), 'product.conf'))
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
