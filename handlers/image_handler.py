# -*- coding: utf-8 -*-
from handlers.base_handler import BaseHandler
import os
import utils
import zipfile
import traceback


class AppIconSetHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render_obj(dict(appIconSet=self.app_icon_set, downloadHost=self.application.settings.get('download_host')))


class IconMergeHandler(BaseHandler):

    def get(self, *args, **kwargs):
        try:
            app_os = self.get_argument('os', '')
            icon = self.get_argument('icon', '')
            subscript = self.get_argument('subscript', '')
            icon_set = self.app_icon_set.get(app_os)
            if not icon_set or not icon:
                self.render_obj(dict(code=400, msg='arguments error'))
                return
            img_icon, fp_icon = utils.get_upload_image_file(self.upload_path, 'icon', icon)
            img_sub, fp_sub = None, ''
            if not img_icon:
                self.render_obj(dict(code=404, msg='image file not found'))
                return
            if subscript:
                img_sub, fp_sub = utils.get_upload_image_file(self.upload_path, 'subscript', subscript)
                if not img_sub:
                    self.render_obj(dict(code=404, msg='image file not found'))
                    return
            new_img = utils.img_composite(img_icon, img_sub) if img_sub else img_icon
            fp = '%s-%s' % (fp_icon, fp_sub) if fp_sub else fp_icon
            app_os_path = os.path.join(self.media_path, 'icons', app_os)
            new_img_path = os.path.join(app_os_path, fp)
            for d in icon_set:
                size = d.get('size', '')
                filename = d.get('filename', '')
                if not filename or not size:
                    continue
                d_img = utils.img_resize(new_img, size)
                if not d_img:
                    continue
                utils.img_save(d_img, new_img_path, filename)
            # 生成所有icon的zip文件
            zf_name = os.path.join(app_os_path, '%s.zip' % fp)
            zf = zipfile.ZipFile(zf_name, 'w', zipfile.ZIP_DEFLATED)
            for fn in os.listdir(new_img_path):
                zf.write(os.path.join(new_img_path, fn), os.path.join(fp, fn))
            zf.close()
            self.render_obj(dict(code=200, msg='success', fp=fp))
        except:
            traceback.print_exc()
            self.render_obj(dict(code=500, msg='system error'))
