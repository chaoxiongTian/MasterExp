# -*- coding: utf-8 -*-
# @Time    : 18-12-4 上午11:24
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : CaptchaUtils.py
# @Software: PyCharm

import random
import math
from out_utils import *
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


# 对一张图片x轴进行波浪处理
def sin_warp_x(image, amplitude, period, phase, background):
    """
    对图片进行水平方向的波浪处理
    :param image: 需要处理的图片
    :param amplitude: 振幅
    :param period: 周期
    :param phase: 相位
    :param background: 填充的颜色
    :return: 处理之后的图片
    """
    image_w, image_h = image.size
    bg_image = Image.new('RGBA', (image_w, image_h + 2 * amplitude),
                         background)
    unit_length = 6.28318530717958 / period
    offsets = [
        int(amplitude * math.sin(phase * unit_length + unit_length * i))
        for i in range(period)
    ]
    for i in range(image_w - 1):
        box = (i, 0, i + 1, image_h)
        region = image.crop(box)
        bg_image.paste(region, (i, amplitude + offsets[i % period]))
    return bg_image.resize((image_w, image_h), Image.ANTIALIAS)


# 对一张图片y轴进行波浪处理
def sin_warp_y(image, amplitude, period, phase, background):
    """
    对图片进行垂直方向的波浪处理
    :param image: 需要处理的图片
    :param amplitude: 振幅
    :param period: 周期
    :param phase: 相位
    :param background: 填充的颜色
    :return: 处理之后的图片
    """
    image_w, image_h = image.size
    bg_image = Image.new('RGBA', (image_w + 2 * amplitude, image_h),
                         background)
    unit_length = 6.28318530717958 / period
    offsets = [
        int(amplitude *
            math.sin((phase / period) * unit_length + unit_length * i))
        for i in range(period)
    ]
    for i in range(image_h - 1):
        box = (0, i, image_w, i + 1)
        region = image.crop(box)
        bg_image.paste(region, ((amplitude + offsets[i % period]), i))
    return bg_image.resize((image_w, image_h), Image.ANTIALIAS)


# 把image resize到target_weight, target_high的长度
def image_resize(image, target_weight, target_high):
    return image.resize((int(target_weight), int(target_high)), Image.ANTIALIAS)


#  把image resize到边长为target_side长的正方形
#  等比例扩到最大边为target_side-padding，然后再其周围使用填充padding长度白边
def image_resize_scale(image, target_side, padding):
    (origin_w, origin_h) = image.size
    target_image = Image.new("RGBA", (target_side, target_side), (255, 255, 255))
    if origin_w >= origin_h:
        # 宽窄
        target_w = target_side - 2 * padding
        mul = target_w / origin_w
        target_h = int(mul * origin_h)
        image = image_resize(image, target_w, target_h)
        target_image.paste(image, (padding, int((target_side - target_h) / 2)))
    else:
        # 短长
        target_h = target_side - 2 * padding
        mul = target_h / origin_h
        target_w = int(origin_h * mul)
        image = image_resize(image, target_w, target_h)
        target_image.paste(image, (int((target_side - target_w) / 2), padding), image)
    return target_image


# 两个图片的纵向拼接
def image_merge_horizontal(image1, image2):
    w1, h1 = image1.size
    w2, h2 = image2.size
    h = (h1, h2)[h1 < h2]
    image = Image.new("RGB", (w1 + w2, h))
    image.paste(image1, (0, 0))
    image.paste(image2, (w1, 0))
    return image

# image = Image.new("RGBA", (100 * 4, 40 * 4), (0, 0, 0))
# MUL_x = 30
# MUL_y = 15
# image_width, image_high = image.size
# step_x = int(image_width / MUL_x)
# step_y = int(image_high / MUL_y)
# draw = ImageDraw.Draw(image)
# for i in range(1, MUL_x + 1):
#     draw.line(((step_x * i, 0), (step_x * i, image_high)), (255, 255, 255), 1)
#     pass
# for i in range(1, MUL_y + 1):
#     draw.line(((0, step_y * i), (image_width, step_y * i)), (255, 255, 255), 1)
# image = sin_warp_x(image, 10, 100, 10, (0, 0, 0))
# image = sin_warp_y(image, 10, 100, 10, (0, 0, 0))
# # image.show()
# image.save("/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaGenerate/data/bg/bg.png")
