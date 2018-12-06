# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : CaptchaGenerate.py
# @Software: PyCharm Community Edition
import os
import sys
import random

from Captcha import Captcha
from CaptchaUtils import image_resize_scale, image_merge_horizontal

# 为了导入上层的工具包，将上层的路径添加到环境变量
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from Utils import make_folders

data_folder = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0], "data")


def generate_blizzard():
    # 构造captcha
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
    label_path = os.path.join(data_folder, "labels", "Blizzard_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", "Blizzard")
    A_folder = os.path.join(captcha_save_folder, "A")  # 有背景的验证码
    B_folder = os.path.join(captcha_save_folder, "B")  # 没有背景的验证码
    make_folders(A_folder, B_folder)

    print("generate %d captcha in %s\n" % (len(labels), captcha_save_folder))
    for i, each in enumerate(labels):
        # 传入两个参数表示值生成一个验证码
        captcha.generate_save_captcha(each,
                                      os.path.join(A_folder, str(i) + '.png'),
                                      os.path.join(B_folder, str(i) + '.png'),  # 该参数为可省略参数
                                      rotate_start=-20, rotate_end=20
                                      )
        print("Nub.%d in complete" % i)


def generate_authorize():
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
    label_path = os.path.join(data_folder, "labels", "Authorize_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", "Authorize")
    A_folder = os.path.join(captcha_save_folder, "A")  # 有背景的验证码
    B_folder = os.path.join(captcha_save_folder, "B")  # 没有背景的验证码
    make_folders(A_folder, B_folder)

    print("generate %d captcha in %s\n" % (len(labels), captcha_save_folder))
    for i, each in enumerate(labels):
        # 传入两个参数表示值生成一个验证码
        captcha.generate_save_captcha(each,
                                      os.path.join(A_folder, str(i) + '.png'),
                                      os.path.join(B_folder, str(i) + '.png'),
                                      noise_number=300, noise_width=1, noise_color=(128, 128, 128),
                                      rotate_start=-10, rotate_end=10
                                      )
        print("Nub.%d in complete" % i)


def generate_save_captcha():
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
    label_path = os.path.join(data_folder, "labels", "captcha_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", "captcha")
    A_folder = os.path.join(captcha_save_folder, "A")  # 有背景的验证码
    B_folder = os.path.join(captcha_save_folder, "B")  # 没有背景的验证码
    make_folders(A_folder, B_folder)

    print("generate %d captcha in %s\n" % (len(labels), captcha_save_folder))
    for i, each in enumerate(labels):
        # 传入两个参数表示值生成一个验证码
        captcha.generate_save_captcha(each,
                                      os.path.join(A_folder, str(i) + '.png'),
                                      os.path.join(B_folder, str(i) + '.png'),  # 该参数为可省略参数
                                      rotate_start=-10, rotate_end=10,
                                      noise_number=2500, noise_width=0.7, noise_color=(50, 50, 50)
                                      # noise_number1=500, noise_width1=1, noise_color1=(96, 96, 96)
                                      )
        print("Nub.%d in complete" % i)


def generate_NIH():
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
    label_path = os.path.join(data_folder, "labels", "NIH_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", "NIH")
    A_folder = os.path.join(captcha_save_folder, "A")  # 有背景的验证码
    B_folder = os.path.join(captcha_save_folder, "B")  # 没有背景的验证码
    make_folders(A_folder, B_folder)

    print("generate %d captcha in %s\n" % (len(labels), captcha_save_folder))
    for i, each in enumerate(labels):
        # 传入两个参数表示值生成一个验证码
        captcha.generate_save_captcha(each,
                                      os.path.join(A_folder, str(i) + '.png'),
                                      os.path.join(B_folder, str(i) + '.png'),  # 该参数为可省略参数
                                      noise_number=500, noise_width=0.7, noise_color=(96, 96, 96),

                                      )
        print("Nub.%d in complete" % i)


def generate_Reddit():
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
    label_path = os.path.join(data_folder, "labels", "Reddit_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", "Reddit")
    A_folder = os.path.join(captcha_save_folder, "A")  # 有背景的验证码
    B_folder = os.path.join(captcha_save_folder, "B")  # 没有背景的验证码
    make_folders(A_folder, B_folder)

    print("generate %d captcha in %s\n" % (len(labels), captcha_save_folder))
    for i, each in enumerate(labels):
        # 传入两个参数表示值生成一个验证码
        rotate = random.randint(-7, 7)
        captcha.generate_save_captcha(each,
                                      os.path.join(A_folder, str(i) + '.png'),
                                      os.path.join(B_folder, str(i) + '.png'),  # 该参数为可省略参数
                                      rotate_start=rotate, rotate_end=rotate
                                      )
        print("Nub.%d in complete" % i)


def generate_Digg():
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
    label_path = os.path.join(data_folder, "labels", "Digg_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", "Digg")
    A_folder = os.path.join(captcha_save_folder, "A")  # 有背景的验证码
    B_folder = os.path.join(captcha_save_folder, "B")  # 没有背景的验证码
    make_folders(A_folder, B_folder)

    print("generate %d captcha in %s\n" % (len(labels), captcha_save_folder))
    for i, each in enumerate(labels):
        # 传入两个参数表示值生成一个验证码
        captcha.generate_save_captcha(each,
                                      os.path.join(A_folder, str(i) + '.png'),
                                      os.path.join(B_folder, str(i) + '.png'),  # 该参数为可省略参数
                                      rotate_start=-25, rotate_end=25
                                      )
        print("Nub.%d in complete" % i)


def generate_baidu():
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
    label_path = os.path.join(data_folder, "labels", "Baidu_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", "Baidu")
    A_folder = os.path.join(captcha_save_folder, "A")  # 有背景的验证码
    B_folder = os.path.join(captcha_save_folder, "B")  # 没有背景的验证码
    make_folders(A_folder, B_folder)

    print("generate %d captcha in %s\n" % (len(labels), captcha_save_folder))
    for i, each in enumerate(labels):
        # 传入两个参数表示值生成一个验证码
        rotate = random.randint(-15, 15)
        captcha.generate_save_captcha(each,
                                      os.path.join(A_folder, str(i) + '.png'),
                                      os.path.join(B_folder, str(i) + '.png'),  # 该参数为可省略参数
                                      rotate_start=rotate, rotate_end=rotate,
                                      )
        print("Nub.%d in complete" % i)


def generate_Qq():
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
    label_path = os.path.join(data_folder, "labels", "Qq_off_1000_labels.txt")
    labels = open(label_path, 'r', encoding="utf-8").read().strip().split("#")

    captcha_save_folder = os.path.join(data_folder, "captcha", "Qq")
    A_folder = os.path.join(captcha_save_folder, "A")  # 有背景的验证码
    B_folder = os.path.join(captcha_save_folder, "B")  # 没有背景的验证码
    train_folder = os.path.join(captcha_save_folder, "train")  # 有背景的验证码
    make_folders(A_folder, B_folder, train_folder)

    print("generate %d captcha in %s\n" % (len(labels), captcha_save_folder))
    for i, each in enumerate(labels):
        # 传入两个参数表示值生成一个验证码
        rotate = random.randint(-15, 15)
        # captcha.generate_save_captcha(each,
        #                               os.path.join(A_folder, str(i) + '.png'),
        #                               os.path.join(B_folder, str(i) + '.png'),  # 该参数为可省略参数
        #                               rotate_start=rotate, rotate_end=rotate
        #                               )
        image, image_clean = captcha.generate_captcha(each, rotate_start=rotate, rotate_end=rotate)
        image_merge_horizontal(image, image_clean).save(os.path.join(train_folder, str(i) + '.png'))
        print("Nub.%d in complete" % i)


if __name__ == "__main__":
    # generate_blizzard()
    # generate_authorize()
    # generate_captcha()
    # generate_NIH()
    # generate_Reddit()
    # generate_Digg()
    # generate_baidu()
    generate_Qq()
    pass
