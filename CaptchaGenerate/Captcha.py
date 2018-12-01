# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : Captcha.py
# @Software: PyCharm Community Edition

import os
import sys
import random
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from Utils import get_internal_path

data_folder = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0], "data")


class Char(object):
    def __init__(self,
                 font_paths,  # 字体路径列表
                 font_size,  # 字体大小
                 font_size_random_range,  # 字体随机的区间
                 font_color  # 字体的颜色 （此处 因为多数都进行二值化，所以不存在随机颜色）
                 ):
        self.font_paths = font_paths
        self.font_size = font_size
        self.font_size_random_range = font_size_random_range
        self.font_color = font_color

    # 生成字符char的Image对象
    def generateChar(self, char):
        """返回字符的Image对象"""
        font_path = random.choice(self.font_paths)  # 选字体
        font_size = random.randint(self.font_size - self.font_size_random_range,
                                   self.font_size + self.font_size_random_range)  # 选字符大小
        # 构造字体对象
        font = ImageFont.truetype(font_path, font_size)
        # 构造Image对象
        char_image = Image.new('RGBA', (font.getsize(char)))
        draw = ImageDraw.Draw(char_image)
        # TODO: 这里的Draw.text存在问题，需要修改。
        draw.text((0, -5), char, (0, 0, 0), font=font)
        del draw
        return char_image


def pre_calc(start, step, images, step_randoms):
    """预估char的Image对象是否可以粘贴到背景的Image上面"""
    preCalc = start
    for i in range(len(images) - 1):
        eachW = images[i].size[0]
        preCalc = preCalc + eachW + step+step_randoms[i]
    return preCalc + images[-1].size[0]


class Captcha(object):
    def __init__(self,
                 captcha_width,  # 验证码宽
                 captcha_higt,  # 验证按高
                 have_bg,  # 是否有背景
                 bg_folder,  # 有背景的话，背景路径
                 font_folder,  # 字体路径，多种字体直接全部读出来
                 font_color,  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
                 font_size,  # 字体基准大小
                 font_size_random_range,  # 字体随机范围
                 start_x=0,  # 第一个字符的开始位置
                 step=10,  # 每个字符之间的距离
                 step_stretch=10,  # 拉伸之后的step
                 step_random_range=5  # 字符之间的距离变化
                 ):
        self.captcha_width = captcha_width
        self.captcha_higt = captcha_higt
        self.have_bg = have_bg
        self.bg_folder = bg_folder
        self.start_x = start_x
        self.step = step
        self.step_stretch = step_stretch
        self.font_folder = font_folder
        self.font_color = font_color
        self.font_size = font_size
        self.font_size_random_range = font_size_random_range
        self.step_random_range = step_random_range
        print(self)  # 打印类信息

    # 定制打印
    def __str__(self):
        return ("Captcha info\n-----------\n(captcha_width: %s)" % self.captcha_width
                + "\n(captcha_higt: %s)" % self.captcha_higt
                + '\n(have_bg: %s)' % self.have_bg
                + '\n(bg_folder: %s)' % self.bg_folder
                + '\n(start_x: %s)' % self.start_x
                + '\n(step: %s)' % self.step
                + '\n\nchar info\n-----------\n(font_color:' + str(self.font_color) + ")"
                + '\n(font_folder: %s)' % self.font_folder
                + '\n(font_size: %s)' % self.font_size
                + '\n(font_size_random_range: %s)' % self.font_size_random_range + "\n-----------\n")

    def get_captcha_bg(self):
        """根据参数返回两个Image，一个是含有背景的，一个是去除背景的"""
        if self.have_bg:
            # 有背景的话，随机取出一个背景。
            bg_image_path = random.choice(get_internal_path(self.bg_folder))
            bg_image = Image.open(bg_image_path)
            bg_image = bg_image.resize((self.captcha_width, self.captcha_higt), Image.ANTIALIAS)
            bg_image_clean = Image.new('RGBA', (self.captcha_width, self.captcha_higt), (255, 255, 255))
            return bg_image, bg_image_clean
        else:
            # 生成一个新的白底背景 
            bg_image = Image.new('RGBA', (self.captcha_width, self.captcha_higt), (255, 255, 255))
            return bg_image, bg_image

    def get_char_images(self, label):
        """根据labels生成 char的Image对象列表"""
        char = Char(font_paths=get_internal_path(self.font_folder),
                    font_size=self.font_size,
                    font_size_random_range=self.font_size_random_range,
                    font_color=self.font_color
                    )
        images = []  # 生成一组字符图片
        for each in label:
            images.append(char.generateChar(each))
        return images

    def paste_images_2_bg_image(self, bg_image, bg_image_clean, images):
        """把一组char的Image对象粘贴到背景Image上面"""
        # TODO:字符之间的距离也可能随机，生成一个随机距离的集合
        step_randoms = []
        for i in range(len(images)):
            step_randoms.append(random.randint(-self.step_random_range, self.step_random_range))

        # TODO：目的（把char的Image对象粘贴到对象背景上粘连上去）
        # 1. 预估charImageList需要的长度，若背景image对象不够长，调整背景image长度
        target_width = pre_calc(self.start_x, self.step, images, step_randoms)
        if target_width > self.captcha_width:
            # 重新调整背景的大小
            bg_image = bg_image.resize((target_width, self.captcha_higt), Image.ANTIALIAS)
        # 计算拉伸之后的图片是否超出边界
        target_width = pre_calc(self.start_x, self.step_stretch, images, step_randoms)
        if target_width > self.captcha_width:
            # 重新调整背景的大小
            bg_image_clean = bg_image_clean.resize((target_width, self.captcha_higt), Image.ANTIALIAS)
        # 2. 开始粘贴 为了保证一致，对于含有背景和没有背景的一起粘贴。
        offset_x = self.start_x
        offset_y = 0
        offset_x_clean = self.start_x
        offset_y_clean = 0
        for i, each in enumerate(images):
            char_w, char_h = each.size
            mask = each
            bg_image.paste(each, (offset_x, int((self.captcha_higt - char_h) / 2)), mask)
            bg_image_clean.paste(each, (offset_x_clean, int((self.captcha_higt - char_h) / 2)), mask)
            offset_x = offset_x + char_w + self.step+step_randoms[i]
            offset_x_clean = offset_x_clean + char_w + self.step_stretch+step_randoms[i]
        bg_image = bg_image.resize((self.captcha_width, self.captcha_higt), Image.ANTIALIAS)
        bg_image_clean = bg_image_clean.resize((self.captcha_width, self.captcha_higt), Image.ANTIALIAS)
        return bg_image, bg_image_clean

    def generateCaptcha(self, label, save_path, save_path_clean="null",
                        # list_1=(0.1, 0.3), list_2=(0.2, 0.4),
                        # rotate_start=-20, rotate_end=20,
                        # noise_number=100, noise_width=2, noise_color=(0, 0, 0)):
                        list_1=(0, 0), list_2=(0, 0),
                        rotate_start=0, rotate_end=0,
                        noise_number=0, noise_width=0, noise_color=(0, 0, 0)):
        """生成验证码并保存"""
        bg_image, bg_image_clean = self.get_captcha_bg()  # 生成背景
        images = self.get_char_images(label)
        # 对图片进行旋转
        images = rotate_images(images, rotate_start, rotate_end)
        # 对图片进行扭曲
        images = warp_images(images, list_1, list_2)
        image, image_clean = self.paste_images_2_bg_image(bg_image, bg_image_clean, images)
        image = add_noise(image, noise_number, noise_width, noise_color)
        if save_path_clean.__eq__("null"):
            # 只保存一个
            image.save(save_path)
        else:
            # 做两个保存
            image.save(save_path)
            image_clean.save(save_path_clean)


def warp_images(char_image_list, list_1, list_2):
    """返回扭曲过得Image集合"""

    def warp_image(im_char, list1, list2):
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
        return im_char_1

    if list_1.__eq__((0, 0)) and list_2.__eq__((0, 0)):
        return char_image_list
    for i in range(len(char_image_list)):
        char_image_list[i] = warp_image(char_image_list[i], list_1, list_2)
    return char_image_list


def rotate_images(images, start, end):
    """返回旋转过得Image集合"""

    def rotate_image(im_char, in_start, in_end):
        im_char = im_char.crop(im_char.getbbox())
        im_char = im_char.rotate(
            random.uniform(in_start, in_end), Image.BILINEAR, expand=1)
        return im_char

    if start == 0 and end == 0:
        return images
    for i in range(len(images)):
        images[i] = rotate_image(images[i], start, end)
    return images


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
