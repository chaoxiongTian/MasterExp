# -*- coding: utf-8 -*-
# @Time    : 18-12-10 下午3:14
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : generate_util.py
# @Software: PyCharm

import random
from out_utils import *
from captcha import MUL
from captcha_utils import *
from captcha import Captcha
from captcha import generate_captcha
from captcha_utils import image_merge_horizontal, image_resize_scale


def generate_megaupload(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=70,  # 验证码宽
        captcha_high=35,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "megaupload"),  # 有背景的话，背景路径
        start_x=10,  # 第一个字符的开始位置
        start_x_random_range=7,
        step=-3,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=1,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "megaupload"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=23,  # 字体基准大小
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
        bg_folder=os.path.join(data_folder, "bg", "blizzard"),  # 有背景的话，背景路径
        start_x=20,  # 第一个字符的开始位置
        step=10,  # 每个字符之间的距离
        step_stretch=10,  # 字符间距扩大每个字符之间的距离
        step_random_range=5,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "blizzard"),  # 字体路径，多种字体直接全部读出来
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
        captcha_width=75,  # 验证码宽
        captcha_high=16,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "authorize"),  # 有背景的话，背景路径
        start_x=15,  # 第一个字符的开始位置
        step=1,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "authorize"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=15,  # 字体基准大小
        font_size_random_range=0  # 字体随机范围
    )
    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each,
                                              rotate_start=-10, rotate_end=10,
                                              noise_number=300, noise_width=1, noise_color=(128, 128, 128)
                                              )
        # image_resize(image, 256, 256).save(os.path.join(folder, str(i) + '.png'))
        image = image_resize_scale(image, 256, padding=20)
        image_clean = image_resize_scale(image_clean, 256, padding=20)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_captcha_net(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=150,  # 验证码宽
        captcha_high=38,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "captcha_net"),  # 有背景的话，背景路径
        start_x=20,  # 第一个字符的开始位置
        step=5,  # 每个字符之间的距离
        step_stretch=5,  # 字符间距扩大每个字符之间的距离
        step_random_range=2,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "captcha_net"),  # 字体路径，多种字体直接全部读出来
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
        mul=1,
        captcha_width=150,  # 验证码宽
        captcha_high=38,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "nih"),  # 有背景的话，背景路径
        start_x=10,  # 第一个字符的开始位置
        step=5,  # 每个字符之间的距离
        step_stretch=5,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "nih"),  # 字体路径，多种字体直接全部读出来
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
        bg_folder=os.path.join(data_folder, "bg", "reddit"),  # 有背景的话，背景路径
        start_x=20,  # 第一个字符的开始位置
        start_x_random_range=60,
        step=1,  # 每个字符之间的距离
        step_stretch=3,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "reddit"),  # 字体路径，多种字体直接全部读出来
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
        bg_folder=os.path.join(data_folder, "bg", "digg"),  # 有背景的话，背景路径
        start_x=5,  # 第一个字符的开始位置
        start_x_random_range=5,
        step=15,  # 每个字符之间的距离
        step_stretch=15,  # 字符间距扩大每个字符之间的距离
        step_random_range=8,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "digg"),  # 字体路径，多种字体直接全部读出来
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
        captcha_width=65,  # 验证码宽
        captcha_high=30,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "baidu"),  # 有背景的话，背景路径
        start_x=10,  # 第一个字符的开始位置
        start_x_random_range=10,
        step=-3,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "baidu"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=30,  # 字体基准大小
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
        captcha_width=65,  # 验证码宽
        captcha_high=30,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "qq"),  # 有背景的话，背景路径
        start_x=10,  # 第一个字符的开始位置
        start_x_random_range=8,
        step=-4,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "qq", "kong"),  # 字体路径，多种字体直接全部读出来
        font_folder_clean=os.path.join(data_folder, "font", "qq", "shi"),
        font_color=(81, 105, 53),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=23,  # 字体基准大小
        font_size_random_range=5  # 字体随机范围
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        rotate = random.randint(-15, 15)
        image, image_clean = generate_captcha(captcha, each, rotate_start=rotate, rotate_end=rotate)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def draw_line(im, draw_feature):
    # 开口角度也应该随机。
    import random
    (width, start, end) = draw_feature
    N = random.randint(start, end)
    draw = ImageDraw.Draw(im)
    im_w, im_h = im.size
    flag = random.randint(0, 1)
    if flag == 0:
        end_x = random.randint(int(im_w / 2), im_w)
        end_y = random.randint(int(im_h / 2), im_h)
        angle_start = random.randint(0, 15)
        angle_end = N - random.randint(0, 15)
        draw.arc((-end_x, -end_y, end_x, end_y), angle_start, angle_end, fill=(0, 0, 0), width=width)
    else:
        end_x = random.randint(0, int(im_w / 3))
        end_y = random.randint(0, int(im_h / 3))
        angle_start = 180 + random.randint(0, 30)
        angle_end = 180 + N - random.randint(0, 30)
        draw.arc((end_x, end_y, (im_w - end_x + im_w), (im_h - end_y + im_h)), angle_start, angle_end,
                 fill=(0, 0, 0), width=width)
    return im


def generate_sina_2014(labels, folder):
    captcha = Captcha(
        captcha_width=75,  # 验证码宽
        captcha_high=30,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "sina_2014"),  # 有背景的话，背景路径
        start_x=10,  # 第一个字符的开始位置
        start_x_random_range=10,
        step=-2,  # 每个字符之间的距离
        step_stretch=0,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "sina_2014"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=18,  # 字体基准大小
        font_size_random_range=0  # 字体随机范围
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        rotate = random.randint(-15, 15)
        image, image_clean = generate_captcha(captcha, each,
                                              inter_line=draw_line, draw_feature=(1, 84, 90),
                                              rotate_start=rotate, rotate_end=rotate)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_recaptcha_2011(labels, folder):
    captcha = Captcha(
        captcha_width=100,  # 验证码宽
        captcha_high=50,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "recaptcha_2011"),  # 有背景的话，背景路径
        start_x=7,  # 第一个字符的开始位置
        start_x_random_range=10,
        step=-2,  # 每个字符之间的距离
        step_stretch=0,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "recaptcha_2011"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=28,  # 字体基准大小
        font_size_random_range=4  # 字体随机范围
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        rotate = random.randint(-15, 15)
        image, image_clean = generate_captcha(captcha, each,
                                              rotate_start=rotate, rotate_end=rotate)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


# 对image按照feature进行波浪化
def image_wave(image, feature):
    """
    对image进行波浪化
    :param image: obj
    :param feature: （amplitude振幅，period周期，phase相位，background拉开之后填充的颜色）
    :return: tar_obj
    """
    if feature is None:
        return image
    else:
        (amplitude, period, phase, background) = feature
        w, h = image.size
        bg_image = Image.new('RGBA', (w, h + 2 * amplitude), background)
        unit_length = 6.28318530717958 / period  # 单位长度
        offsets = [
            int(amplitude * math.sin(phase * unit_length + unit_length * i))
            for i in range(period)
        ]
        for i in range(w - 1):
            box = (i, 0, i + 1, h)
            region = image.crop(box)
            bg_image.paste(region, (i, amplitude + offsets[i % period]))
        return bg_image.resize((w, h), Image.ANTIALIAS)


def generate_yahoo(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=100,  # 验证码宽
        captcha_high=30,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "yahoo"),  # 有背景的话，背景路径
        start_x=6,  # 第一个字符的开始位置
        start_x_random_range=8,
        step=-2,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "yahoo", "kong"),  # 字体路径，多种字体直接全部读出来
        font_folder_clean=os.path.join(data_folder, "font", "yahoo", "shi"),
        font_color=(81, 105, 53),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=24,  # 字体基准大小
        font_size_random_range=0  # 字体随机范围
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        amplitude = random.randint(5, 10)
        flag = random.randint(4, 6)
        period = int(captcha.captcha_width / flag)
        phase = random.randint(0, period)
        background = 255, 255, 255
        feature = (amplitude, period, phase, background)
        image, image_clean = generate_captcha(captcha, each, wave=image_wave, wave_feature=feature,
                                              rotate_start=(-8), rotate_end=8)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_baidu_2011(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=50,  # 验证码宽
        captcha_high=20,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "baidu_2011"),  # 有背景的话，背景路径
        start_x=8,  # 第一个字符的开始位置
        start_x_random_range=8,
        step=-1,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "baidu_2011"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=15,  # 字体基准大小
        font_size_random_range=2,  # 字体随机范围
        offset_y_range=2
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each,
                                              inter_line=draw_line, draw_feature=(1, 40, 60),
                                              list_1=(0.1, 0.2), list_2=(0.1, 0.2),
                                              rotate_start=-10, rotate_end=10,
                                              )
        image = image_resize_scale(image, 256, padding=20)
        image_clean = image_resize_scale(image_clean, 256, padding=20)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_baidu_2013(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=100,  # 验证码宽
        captcha_high=40,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "baidu_2013"),  # 有背景的话，背景路径
        start_x=8,  # 第一个字符的开始位置
        start_x_random_range=8,
        step=-2,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "baidu_2013", "kong"),  # 字体路径，多种字体直接全部读出来
        font_folder_clean=os.path.join(data_folder, "font", "baidu_2013", "shi"),
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=27,  # 字体基准大小
        font_size_random_range=2,  # 字体随机范围
        offset_y_range=2
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each,
                                              inter_line=draw_line, draw_feature=(1, 45, 64),
                                              rotate_start=-10, rotate_end=10,
                                              )
        image = image_resize_scale(image, 256, padding=20)
        image_clean = image_resize_scale(image_clean, 256, padding=20)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_amazon(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=100,  # 验证码宽
        captcha_high=35,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "amazon"),  # 有背景的话，背景路径
        start_x=13,  # 第一个字符的开始位置
        start_x_random_range=5,
        step=-1,  # 每个字符之间的距离
        step_stretch=2,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "amazon"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=25,  # 字体基准大小
        font_size_random_range=0,  # 字体随机范围
        offset_y_range=3
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each, rotate_start=-18, rotate_end=18)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_recaptcha_2013(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=100,  # 验证码宽
        captcha_high=40,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "recaptcha_2013"),  # 有背景的话，背景路径
        start_x=13,  # 第一个字符的开始位置
        start_x_random_range=5,
        step=-2,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "recaptcha_2013"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=25,  # 字体基准大小
        font_size_random_range=0,  # 字体随机范围
        offset_y_range=0
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        amplitude = random.randint(4, 7)
        flag = random.randint(4, 4)
        period = int(captcha.captcha_width / flag)
        phase = random.randint(0, period)
        background = 255, 255, 255
        feature = (amplitude, period, phase, background)
        image, image_clean = generate_captcha(captcha, each, wave=image_wave, wave_feature=feature,
                                              rotate_start=-18, rotate_end=18)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_paypal(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=110,  # 验证码宽
        captcha_high=30,  # 验证按高
        have_bg=True,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "paypal"),  # 有背景的话，背景路径
        start_x=20,  # 第一个字符的开始位置
        start_x_random_range=40,
        step=-1,  # 每个字符之间的距离
        step_stretch=2,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "paypal"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=26,  # 字体基准大小
        font_size_random_range=0,  # 字体随机范围
        offset_y_range=0
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each, rotate_start=-13, rotate_end=13)
        image = image_resize_scale(image, 256, padding=30)
        image_clean = image_resize_scale(image_clean, 256, padding=30)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


def generate_cnn(labels, folder):
    # 构造captcha
    captcha = Captcha(
        captcha_width=100,  # 验证码宽
        captcha_high=25,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "cnn"),  # 有背景的话，背景路径
        start_x=8,  # 第一个字符的开始位置
        start_x_random_range=8,
        step=-1,  # 每个字符之间的距离
        step_stretch=1,  # 字符间距扩大每个字符之间的距离
        step_random_range=0,  # 字符之间距离随机的范围
        font_folder=os.path.join(data_folder, "font", "cnn"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=23,  # 字体基准大小
        font_size_random_range=0,  # 字体随机范围
        offset_y_range=0
    )

    print("generate %d captcha in %s\n" % (len(labels), folder))
    for i, each in enumerate(labels):
        image, image_clean = generate_captcha(captcha, each,
                                              inter_line=draw_line, draw_feature=(2, 80, 90),
                                              list_1=(0.1, 0.2), list_2=(0.1, 0.2),
                                              rotate_start=-10, rotate_end=10,
                                              )
        image = image_resize_scale(image, 256, padding=20)
        image_clean = image_resize_scale(image_clean, 256, padding=20)
        image_merge_horizontal(image, image_clean).save(os.path.join(folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)

