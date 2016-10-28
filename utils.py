# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageFont, ImageDraw


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
        return None, '', ''
    fp, fn = get_file_path_name(file_info)
    if not fp or not fn:
        return None, '', ''
    file_path = os.path.join(upload_path, category, fp, fn)
    if not os.path.exists(file_path):
        return None, '', ''
    return Image.open(file_path), fp, fn


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

WIDTH_PADDING = 2
HEIGHT_PADDING = 2
MARK_RADIO = 10


def get_mark_position(img, mark, pos='rb'):
    img_w, img_h = img.size[0], img.size[1]
    mark_w, mark_h = mark.size[0], mark.size[1]
    r_w = img_w // MARK_RADIO
    if mark_w > r_w:
        radio = mark_w // r_w
        mark_w, mark_h = mark_w // radio, mark_h // radio
        re_mark = mark.resize((mark_w, mark_h), Image.ANTIALIAS)
    else:
        re_mark = mark
    pos_coordinate = dict(
        lt=(WIDTH_PADDING, HEIGHT_PADDING),
        lb=(WIDTH_PADDING, img_h - mark_h - HEIGHT_PADDING),
        rt=(img_w - mark_w - WIDTH_PADDING, HEIGHT_PADDING),
        rb=(img_w - mark_w - WIDTH_PADDING, img_h - mark_h - HEIGHT_PADDING),
        md=(int((img_w - mark_w)/2), int((img_h - mark_h)/2))
    )
    return pos_coordinate.get(pos), re_mark


def text2img(text, font_path, font_name='Lato.tff', font_color='#333333', font_size=24):
    font_file = os.path.join(font_path, font_name)
    print(font_file)
    font = ImageFont.truetype(font_file, font_size)
    width, height = font.getsize(text)
    mark = Image.new('RGBA', (width, height))
    draw = ImageDraw.ImageDraw(mark, "RGBA")
    draw.setfont(font)
    draw.text((0, 0), text, fill=font_color)
    return mark
