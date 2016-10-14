# -*- coding: utf-8 -*-
import os
from PIL import Image


def img_composite(img1, img2, position=(0, 0)):
    if img1.mode != 'RGBA':
        img1 = img1.convert('RGBA')
    if img2.mode != 'RGBA':
        img2 = img2.convert('RGBA')
    layer = Image.new('RGBA', img1.size, (0, 0, 0, 0))
    layer.paste(img2, position)
    return Image.composite(layer, img1, layer)


def img_save(img, file_path, filename, img_format='PNG'):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    img.save(os.path.join(file_path, filename), img_format, quality=100)


def get_upload_image_file(upload_path, category, file_info):
    if not file_info:
        return None, ''
    fp, fn = get_file_path_name(file_info)
    if not fp or not fn:
        return None, ''
    file_path = os.path.join(upload_path, category, fp, fn)
    if not os.path.exists(file_path):
        return None, ''
    return Image.open(file_path), fp


def get_file_path_name(file_info=''):
    if file_info:
        info = file_info.split('/')
        if len(info) == 2:
            return info[0], info[1]
    return '', ''


def img_resize(img, size='512x512'):
    if not size:
        return img
    ss = size.split('x')
    if len(ss) != 2:
        return None
    return img.resize((int(ss[0]), int(ss[1])), Image.ANTIALIAS)
