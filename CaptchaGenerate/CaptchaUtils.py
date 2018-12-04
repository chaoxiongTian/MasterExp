# -*- coding: utf-8 -*-
# @Time    : 18-12-4 上午11:24
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : CaptchaUtils.py
# @Software: PyCharm

import random
from PIL import Image, ImageDraw, ImageFont


#  根据labels生成一组char的Image对象。
def generate_char_images(char, font_path, font_size, font_color=(0, 0, 0)):
    """返回字符的Image对象"""
    # 构造字体对象
    image_font = ImageFont.truetype(font_path, font_size)
    # 构造Image对象
    char_image = Image.new('RGBA', (image_font.getsize(char)))
    draw = ImageDraw.Draw(char_image)
    # TODO: 这里的Draw.text存在问题，需要修改。
    draw.text((0, -5), char, font_color, font=image_font)
    del draw
    return char_image


#  根据这组图片预估需要的长度
def pre_calc(start, step, images, step_randoms):
    """预估char的Image对象是否可以粘贴到背景的Image上面"""
    preCalc = start
    for i in range(len(images)):
        eachW = images[i].size[0]
        preCalc = preCalc + eachW + step + step_randoms[i]
    return preCalc


#  等比例缩小多少倍
def zoom_down_mul(image, mul):
    """image等比例缩小mul倍"""
    width, high = image.size
    return image.resize((int(width / mul), int(high / mul)), Image.ANTIALIAS)


#  扭曲一组图片
def warp_images(images, images_clean, list_1, list_2):
    """返回扭曲过得Image集合"""

    def warp_image(im_char, im_char_clean, list1, list2):
        (w, h) = im_char.size
        dx = w * random.uniform(list1[0], list1[1])
        dy = h * random.uniform(list2[0], list2[1])
        x1 = int(random.uniform(-dx, dx))
        y1 = int(random.uniform(-dy, dy))
        x2 = int(random.uniform(-dx, dx))
        y2 = int(random.uniform(-dy, dy))
        w2 = w + abs(x1) + abs(x2)
        h2 = h + abs(y1) + abs(y2)
        # 变量data是一个8元组(x0, y0, x1, y1, x2, y2, x3, y3)，它包括源四边形的左下，左上，右上和右下四个角。
        data = (
            x1,
            y1,
            -x1,
            h2 - y2,
            w2 + x2,
            h2 + y2,
            w2 - x2,
            -y1,
        )
        im_char = im_char.resize((w2, h2))
        im_char_1 = im_char.transform((int(w), int(h)), Image.QUAD, data)

        im_char_clean = im_char_clean.resize((w2, h2))
        im_char_2 = im_char_clean.transform((int(w), int(h)), Image.QUAD, data)
        return im_char_1, im_char_2

    if list_1.__eq__((0, 0)) and list_2.__eq__((0, 0)):
        return images, images_clean
    for i in range(len(images)):
        images[i], images_clean[i] = warp_image(images[i],
                                                images_clean[i],
                                                list_1, list_2)
    return images, images_clean


#  旋转一组图片
def rotate_images(images, images_clean, start, end):
    """返回旋转过得Image集合"""

    def rotate_image(im_char, angle):
        im_char = im_char.crop(im_char.getbbox())
        im_char = im_char.rotate(angle, Image.BILINEAR, expand=1)
        return im_char

    if start == 0 and end == 0:
        return images, images_clean
    for i in range(len(images)):
        rotate_angle = random.uniform(start, end)
        images[i] = rotate_image(images[i], rotate_angle)
        images_clean[i] = rotate_image(images_clean[i], rotate_angle)
    return images, images_clean


# 添加干扰信息
def add_noise(image, noise_number, noise_width, noise_color):
    """返回添加了干扰信息的Image"""
    if noise_number == 0:
        return image
    draw = ImageDraw.Draw(image)
    w, h = image.size
    while noise_number:
        x1 = random.randint(0, w)
        y1 = random.randint(0, h)
        draw.ellipse(((x1, y1), (x1 + noise_width, y1 + noise_width)), fill=noise_color)
        noise_number -= 1
    del draw
    return image
