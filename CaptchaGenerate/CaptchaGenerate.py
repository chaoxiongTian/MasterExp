# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : CaptchaGenerate.py
# @Software: PyCharm Community Edition
import os
import sys

from Captcha import Captcha

# 为了导入上层的工具包，将上层的路径添加到环境变量
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from Utils import make_folders

data_folder = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0], "data")


def generate_blizzard():
    # 构造captcha
    captcha = Captcha(
        captcha_width=150,  # 验证码宽
        captcha_higt=30,  # 验证按高
        have_bg=False,  # 是否有背景
        bg_folder=os.path.join(data_folder, "bg", "Blizzard"),  # 有背景的话，背景路径
        start_x=10,  # 第一个字符的开始位置
        step=10,  # 每个字符之间的距离
        step_stretch=10,  # 字符间距扩大每个字符之间的距离
        font_folder=os.path.join(data_folder, "font", "Blizzard"),  # 字体路径，多种字体直接全部读出来
        font_color=(0, 0, 0),  # 指定颜色(处理之后都需要二值化，所以可不用随机颜色)
        font_size=32,  # 字体基准大小
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
        captcha.generateCaptcha(each,
                                os.path.join(A_folder, str(i) + '.png'),
                                os.path.join(B_folder, str(i) + '.png')  # 该参数为可省略参数
                                )
        print("Nub.%d in complete" % i)


def generate_baidu():
    pass


if __name__ == "__main__":
    generate_blizzard()
    # generate_baidu()
