# -*- coding: utf-8 -*-
import os
import tornado.web


class SiteHandler(tornado.web.StaticFileHandler):

    def initialize(self, path, default_filename=None):
        self.dirname, self.filename = os.path.split(path)
        super(SiteHandler, self).initialize(self.dirname)

    def get_modified_time(self):
        return None

    def get(self, path=None, include_body=True):
        super(SiteHandler, self).get(self.filename, include_body)
