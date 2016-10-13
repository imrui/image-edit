# -*- coding: utf-8 -*-
from handlers.base_handler import BaseHandler


class AppIconSetHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render_obj(self.app_icon_set)


class IconMergeHandler(BaseHandler):

    def get(self, *args, **kwargs):
        os = self.get_argument('os', '')
        icon = self.get_argument('icon', '')
        subscript = self.get_argument('subscript', '')
        print(os, icon, subscript)
        self.render_obj(dict(msg='success'))
