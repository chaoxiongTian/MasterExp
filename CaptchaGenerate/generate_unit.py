# -*- coding: utf-8 -*-
# @Time    : 18-12-10 下午3:14
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : generate_util.py
# @Software: PyCharm

import random
from out_utils import *
from captcha_utils import *
from captcha import Captcha
from captcha import generate_captcha
from captcha_utils import image_merge_horizontal, image_resize_scale


def generate_megaupload(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=140,  # 验证码宽
        captcha_high=70,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "megaupload"),  # 有背景的话，背景路径
        start_x=10,  # 第一个字符的开始位置
        start_x_random_range=7,
        step=-4,  # 每个字符之间的距离
        step_stretch=4,  # 字符间距扩大每个字符之间的距离
        step_random_range=2,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "megaupload"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=45,  # 字体基准大小
        font_size_random_range=0,  # 字体随机范围
        # font_bg_color=(255, 255, 255)
    )
    print("generate %d captcha in %s\n" % (len(labels), folder))

    def cus_paste(captcha, bg_image, bg_image_clean, images, images_clean):
        # 每两个字符之间的距离的step，有个验证码字符之间是随机的，所以在此基础上添加一个数据数组。
        step_randoms = []
        for i in range(len(images)):
            step_randoms.append(random.randint(-captcha.step_random_range, captcha.step_random_range))

        offset_y_randoms = []
        for i in range(len(images)):
            offset_y_randoms.append(random.randint(-captcha.offset_y_range, captcha.offset_y_range))
        # TODO：目的（把char的Image对象粘贴到对象背景上粘连上去）

        # 1. 预估images+step和step_randoms需要的长度，若背景image对象不够长，先调整背景image长度。
        start_rio = abs(random.randint(captcha.start_x - captcha.start_x_random_range,
                                       captcha.start_x + captcha.start_x_random_range))
        target_width = pre_calc(start_rio, captcha.step, images, step_randoms)
        if target_width > captcha.captcha_width:
            # 重新调整背景的大小
            bg_image = bg_image.resize((target_width, captcha.captcha_high), Image.ANTIALIAS)

        target_width_clean = pre_calc(start_rio, captcha.step_stretch, images_clean, step_randoms)
        if target_width_clean > captcha.captcha_width:
            bg_image_clean = bg_image_clean.resize((target_width_clean, captcha.captcha_high), Image.ANTIALIAS)

        # 2. 开始粘贴 为了保证一致，对于含有背景和没有背景的一起粘贴。
        offset_x = start_rio
        offset_y = 0
        offset_x_clean = start_rio
        offset_y_clean = 0
        for i in range(len(images)):
            char_w, char_h = images[i].size
            char_w_clean, char_h_clean = images_clean[i].size
            bg_image = paste(bg_image, images[i],
                             offset_x, int((captcha.captcha_high - char_h) / 2) + offset_y_randoms[i])
            bg_image_clean.paste(images_clean[i],
                                 (offset_x_clean, int((captcha.captcha_high - char_h_clean) / 2) + offset_y_randoms[i]),
                                 images_clean[i]
                                 )
            offset_x = offset_x + char_w + captcha.step + step_randoms[i]
            offset_x_clean = offset_x_clean + char_w_clean + captcha.step_stretch + step_randoms[i]
        bg_image = bg_image.resize((captcha.captcha_width, captcha.captcha_high), Image.ANTIALIAS)
        bg_image_clean = bg_image_clean.resize((captcha.captcha_width, captcha.captcha_high), Image.ANTIALIAS)
        return bg_image, bg_image_clean

    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each,
                                              fun_paste=cus_paste,
                                              rotate_start=-20,
                                              rotate_end=20)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_blizzard(labels, folder):
    # 构造captchas
    captcha = Captcha(
        captcha_width=150,  # 验证码宽
        captcha_high=38,  # 验证按高
        have_bg=True,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "Blizzard"),  # 有背景的话，背景路径
        start_x=20,  # 第一个字符的开始位置
        step=10,  # 每个字符之间的距离
        step_stretch=10,  # 字符间距扩大每个字符之间的距离
        step_random_range=5,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "Blizzard"),  # 字体路径，多种字体直接全部读出来
        font_color=(255, 190, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=15,  # 字体基准大小
        font_size_random_range=0  # 字体随机范围
    )
    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each, rotate_start=-20, rotate_end=20)

        image = image_resize_scale(image, 256, padding=20)
        image_clean = image_resize_scale(image_clean, 256, padding=20)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_authorize(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=150,  # 验证码宽
        captcha_high=38,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "Authorize"),  # 有背景的话，背景路径
        start_x=30,  # 第一个字符的开始位置
        step=3,  # 每个字符之间的距离
        step_stretch=3,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "Authorize"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=28,  # 字体基准大小
        font_size_random_range=0  # 字体随机范围
    )
    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each,
                                              rotate_start=-10, rotate_end=10,
                                              noise_number=300, noise_width=1, noise_color=(128, 128, 128)
                                              )
        image_resize(image, 256, 256).save(os.path.join(folder, str(i) + '.png'))
        # image = image_resize_scale(image, 256, padding=20)
        # image_clean = image_resize_scale(image_clean, 256, padding=20)
        # image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_captchanet(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=150,  # 验证码宽
        captcha_high=38,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "captcha"),  # 有背景的话，背景路径
        start_x=20,  # 第一个字符的开始位置
        step=5,  # 每个字符之间的距离
        step_stretch=5,  # 字符间距扩大每个字符之间的距离
        step_random_range=2,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "captcha"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=20,  # 字体基准大小
        font_size_random_range=0,  # 字体随机范围
        offset_y_range=3
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each,
                                              rotate_start=-10, rotate_end=10,
                                              noise_number=2500, noise_width=0.7, noise_color=(50, 50, 50),
                                              )
        image = image_resize_scale(image, 256, padding=20)
        image_clean = image_resize_scale(image_clean, 256, padding=20)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_nih(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=150,  # 验证码宽
        captcha_high=38,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "NIH"),  # 有背景的话，背景路径
        start_x=10,  # 第一个字符的开始位置
        step=5,  # 每个字符之间的距离
        step_stretch=5,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "NIH"),  # 字体路径，多种字体直接全部读出来
        font_color=(107, 123, 139),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=34,  # 字体基准大小
        font_size_random_range=0,  # 字体随机范围
        offset_y_range=5
    )
    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each, noise_number=500, noise_width=0.7,
                                              noise_color=(96, 96, 96))
        image = image_resize_scale(image, 256, padding=20)
        image_clean = image_resize_scale(image_clean, 256, padding=20)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_reddit(labels, folder):
    captcha = Captcha(
        captcha_width=120,  # 验证码宽
        captcha_high=50,  # 验证按高
        have_bg=True,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "Reddit"),  # 有背景的话，背景路径
        start_x=20,  # 第一个字符的开始位置
        start_x_random_range=60,
        step=1,  # 每个字符之间的距离
        step_stretch=3,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "Reddit"),  # 字体路径，多种字体直接全部读出来
        font_color=(255, 255, 255),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=19,  # 字体基准大小
        font_size_random_range=0,  # 字体随机范围
        offset_y_range=2
    )
    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        rotate = random.randint(-7, 7)
        image, image_clean = generate_captcha(captcha, each, rotate_start=rotate, rotate_end=rotate)
        image = image_resize_scale(image, 256, padding=20)
        image_clean = image_resize_scale(image_clean, 256, padding=20)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_digg(labels, folder):
    captcha = Captcha(
        captcha_width=150,  # 验证码宽
        captcha_high=35,  # 验证按高
        have_bg=True,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "Digg"),  # 有背景的话，背景路径
        start_x=5,  # 第一个字符的开始位置
        start_x_random_range=5,
        step=15,  # 每个字符之间的距离
        step_stretch=15,  # 字符间距扩大每个字符之间的距离
        step_random_range=8,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "Digg"),  # 字体路径，多种字体直接全部读出来
        font_color=(50, 50, 50),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=20,  # 字体基准大小
        font_size_random_range=2,  # 字体随机范围
        offset_y_range=5
    )
    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each, rotate_start=-25, rotate_end=25)
        image = image_resize_scale(image, 256, padding=20)
        image_clean = image_resize_scale(image_clean, 256, padding=20)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_baidu(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=75,  # 验证码宽
        captcha_high=40,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "Baidu"),  # 有背景的话，背景路径
        start_x=10,  # 第一个字符的开始位置
        start_x_random_range=10,
        step=-3,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "Baidu"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=35,  # 字体基准大小
        font_size_random_range=0  # 字体随机范围
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        rotate = random.randint(-15, 15)
        image, image_clean = generate_captcha(captcha, each, rotate_start=rotate, rotate_end=rotate)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_qq(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=100,  # 验证码宽
        captcha_high=40,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "Qq"),  # 有背景的话，背景路径
        start_x=15,  # 第一个字符的开始位置
        start_x_random_range=10,
        step=-4,  # 每个字符之间的距离
        step_stretch=0,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "Qq", "kong"),  # 字体路径，多种字体直接全部读出来
        font_folder_clean=os.path.join(data_folder, "font", "Qq", "shi"),
        font_color=(81, 105, 53),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=28,  # 字体基准大小
        font_size_random_range=8  # 字体随机范围
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        rotate = random.randint(-15, 15)
        image, image_clean = generate_captcha(captcha, each, rotate_start=rotate, rotate_end=rotate)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)

