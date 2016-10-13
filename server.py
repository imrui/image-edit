# -*- coding: utf-8 -*-
import os.path
import uuid
import tornado
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from handlers.site_handler import SiteHandler, UploadHandler
from handlers.image_handler import AppIconSetHandler, IconMergeHandler


define('debug', default=True, type=bool)
define('port', default=8080, type=int, help='run on the given port')
define('app_icon_set', type=dict)


class Application(tornado.web.Application):

    def __init__(self):
        root_path = os.path.dirname(__file__)
        self.tmp_path = os.path.join(root_path, 'tmp')
        self.media_path = os.path.join(root_path, 'media')
        handlers = [
            (r'/', SiteHandler, {'path': os.path.join(os.path.dirname(__file__), 'static/starter.html')}),
            (r"/media/(.*)", tornado.web.StaticFileHandler, {'path': self.media_path}),
            (r'/upload_to/(?P<category>\w+)', UploadHandler),
            (r'/app/icon/set', AppIconSetHandler),
            (r'/icon/merge', IconMergeHandler),
        ]
        settings = dict(
            static_path=os.path.join(root_path, 'static'),
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
