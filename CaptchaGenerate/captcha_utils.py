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
def generate_char_images(char, font_path, font_size, font_color=(0, 0, 0), font_bg_color=None):
    """返回字符的Image对象"""
    # 构造字体对象
    image_font = ImageFont.truetype(font_path, font_size)
    # 构造Image对象
    if font_bg_color is not None:
        char_image = Image.new('RGBA', (image_font.getsize(char)), font_bg_color)
    else:
        char_image = Image.new('RGBA', (image_font.getsize(char)))
    draw = ImageDraw.Draw(char_image)
    # TODO: 这里的Draw.text存在问题，需要修改。
    draw.text((0, -5), char, font_color, font=image_font)
    del draw
    return char_image


#  根据这组图片预估需要的长度
def pre_calc(start, step, images, step_randoms, ):
    """预估char的Image对象是否可以粘贴到背景的Image上面"""
    preCalc = start
    for i in range(len(images)):
        eachW = images[i].size[0]
        preCalc = preCalc + eachW + step + step_randoms[i]
    return preCalc + abs(step) * 2


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


def convert_gray(im):
    return im.convert("L")


# 转二值化
def convert_binary(im, threshold=127):
    im = convert_gray(im)
    (image_w, image_h) = im.size
    pix_data = im.load()
    for iter_y in range(image_h):
        for iter_x in range(image_w):
            if pix_data[iter_x, iter_y] < threshold:
                pix_data[iter_x, iter_y] = 0
            else:
                pix_data[iter_x, iter_y] = 255
    return im


# 把一个image 粘贴到另外一个image上面 重合部分改为黑色
def paste(bg_image, image, offset_x, offset_y):
    b_w, b_h = bg_image.size
    w, h = image.size
    # 创建一个新白色背景把旋转之后的image粘贴在其上
    image_new = Image.new('RGB', (w, h), (255, 255, 255))
    image_new.paste(image, (0, 0), image)
    bg_image = convert_binary(bg_image)
    bg_pix = bg_image.load()
    image_pix = convert_binary(image_new).load()

    for iter_x in range(w):
        if iter_x + offset_x >= b_w:
            break
        for iter_y in range(h):
            if iter_y + offset_y >= b_h:
                break
            if image_pix[iter_x, iter_y] == 0:
                if bg_pix[iter_x + offset_x, iter_y + offset_y] == 0:
                    bg_pix[iter_x + offset_x, iter_y + offset_y] = 255
                else:
                    bg_pix[iter_x + offset_x, iter_y + offset_y] = 0
    return bg_image


# 画出一个image的轮廓
def outline(im):
    im = convert_binary(im)
    w, h = im.size
    from skimage import measure
    import numpy as np
    numpy_im = np.array(im, dtype=np.float32)  # =skimage
    contours = measure.find_contours(numpy_im, 0.3)
    contours_points = set()
    for each in contours:
        for (x, y) in each:
            contours_points.add((int(x), int(y)))
    im_new = Image.new('RGB', (w, h), (255, 255, 255))
    pix_data = im_new.load()
    for (x, y) in contours_points:
        pix_data[y, x] = 0
    return im_new


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
