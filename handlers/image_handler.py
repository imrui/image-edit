# -*- coding: utf-8 -*-
from handlers.base_handler import BaseHandler
import os
import utils
import zipfile
import traceback


class AppIconSetHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render_obj(dict(appIconSet=self.app_icon_set))


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
            img_icon, fp_icon, _ = utils.get_upload_image_file(self.upload_path, 'icon', icon)
            img_sub, fp_sub = None, ''
            if not img_icon:
                self.render_obj(dict(code=404, msg='image file not found'))
                return
            if subscript:
                img_sub, fp_sub, _ = utils.get_upload_image_file(self.upload_path, 'subscript', subscript)
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


class WatermarkHandler(BaseHandler):

    def get(self, *args, **kwargs):
        image = self.get_argument('image', '')
        _type = self.get_argument('type', '')
        pos = self.get_argument('pos', '')
        if not image or not _type or not pos or _type not in ('txt', 'img'):
            self.render_obj(dict(code=400, msg='arguments error'))
            return
        img_image, fp_image, fn_image = utils.get_upload_image_file(self.upload_path, 'image', image)
        if not img_image:
            self.render_obj(dict(code=404, msg='image file not found'))
            return
        wm_path = os.path.join(self.media_path, 'watermark', _type)
        if _type == 'img':
            mark = self.get_argument('mark', '')
            if not mark:
                self.render_obj(dict(code=400, msg='args error: mark'))
                return
            img_mark, fp_mark, _ = utils.get_upload_image_file(self.upload_path, 'mark', mark)
            if not img_mark:
                self.render_obj(dict(code=404, msg='mark file not found'))
                return
            position, img_re_mark = utils.get_mark_position(img_image, img_mark, pos)
            if not position:
                self.render_obj(dict(code=404, msg='args error: pos'))
                return
            fp = '%s-%s' % (fp_image, fp_mark)
        elif _type == 'txt':
            txt = self.get_argument('txt', '')
            font = self.get_argument('font', '')
            font_size = int(self.get_argument('fontSize', '24'))
            font_color = self.get_argument('fontColor', '')
            if not txt or not font or not font_size or not font_color:
                self.render_obj(dict(code=400, msg='args error: txt or font setting'))
                return
            img_mark = utils.text2img(txt, os.path.join(self.static_path, 'fonts'), font, font_color=font_color, font_size=font_size)
            fp = fp_image
        else:
            self.render_obj(dict(code=404, msg='args error: type'))
            return
        position, img_re_mark = utils.get_mark_position(img_image, img_mark, pos)
        if not position:
            self.render_obj(dict(code=404, msg='args error: pos'))
            return
        fn = '%s-%s' % (pos, fn_image)
        new_img = utils.img_composite(img_image, img_re_mark, position)
        new_img_path = os.path.join(wm_path, fp)
        utils.img_save(new_img, new_img_path, fn)
        self.render_obj(dict(code=200, msg='success', fp=fp, fn=fn))
