# -*- coding: utf-8 -*-
import tornado.web
import traceback
import logging
from tornado import gen
from tornado.escape import json_encode, json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat


class BaseHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @property
    def media_path(self):
        return self.application.media_path

    @property
    def tmp_path(self):
        return self.application.tmp_path

    @property
    def app_icon_set(self):
        return self.application.settings.get('app_icon_set')

    def get_current_user(self):
        return self.get_secure_cookie('username')

    def render_obj(self, obj, status=200):
        self.set_status(status)
        self.set_header('Content-Type', 'application/json')
        self.write(json_encode(obj))
        self.finish()

    def on_finish(self):
        pass

    def get_all_arguments(self):
        _args = dict()
        for k in self.request.arguments:
            v = self.get_argument(k)
            if not v:
                continue
            _args[k] = v
        return _args

    @gen.coroutine
    def fetch(self, url, args=None):
        if not url:
            logging.info('url is none')
            return
        if args:
            _url = url_concat(url, args)
        else:
            _url = url
        print(_url)
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(_url)
        return json_decode(response.body)


class ApiCacheHandler(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.__cache_text = None

    @property
    def cache_text(self):
        return self.__cache_text

    @cache_text.setter
    def cache_text(self, cache_text):
        self.__cache_text = cache_text

    def url(self, *args, **kwargs):
        pass

    @gen.coroutine
    def get(self, *args, **kwargs):
        try:
            response = yield AsyncHTTPClient().fetch(self.url(**kwargs))
            if response.code == 200:
                self.cache_text = response.body
        except:
            traceback.print_exc()
        self.set_header('Content-Type', 'application/json')
        self.write(self.cache_text)
        self.finish()
