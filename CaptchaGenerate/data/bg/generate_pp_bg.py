# -*- coding: utf-8 -*-
# @Time    : 19-1-7 下午4:50
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : generate_pp_bg.py
# @Software: PyCharm

import os
import random
from PIL import Image, ImageDraw, ImageFont

default_font = '/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaGenerate/data/font/paypal_bg/calibriz.ttf'
default_content = 'PayPal'
def_width = 220
def_high = 60
MUL = 2


def image_resize(image, target_weight, target_high):
    return image.resize((int(target_weight), int(target_high)), Image.ANTIALIAS)


def add_one(im, font_size, content=default_content, font_path=default_font, font_color=(0, 0, 0)):
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(im)
    w, h = im.size
    draw.text((random.randint(0, w), random.randint(0, h)), content, font_color, font=font)
    del draw
    return im


# 创建paypal的背景
def generate_paypal_bg(image_width=def_width*MUL, image_high=def_high*MUL, big_num=25, small_num=25):
    big_num = random.randint(big_num, big_num + 10)
    small_num = random.randint(small_num, small_num + 10)
    big_font_size = 20
    small_font_size = 10
    image = Image.new("RGBA", (image_width, image_high), (255, 255, 255))

    def iter_generate(im, epoch, font_size):
        for i in range(epoch):
            im = add_one(im, font_size)
        return im

    image = iter_generate(image, big_num, big_font_size)
    image = iter_generate(image, small_num, small_font_size)
    return image_resize(image, def_width, def_high)


def main():
    num = 300
    save_folder = '/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaGenerate/data/bg/paypal'
    for i in range(num):
        file_name = os.path.join(save_folder, str(i) + '.png')
        image = generate_paypal_bg()
        image.save(file_name)
        print('num {} is complete'.format(str(i)))


if __name__ == '__main__':
    main()
