# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : CaptchaGenerate.py
# @Software: PyCharm Community Edition

import os
import sys
from Label import CaptchaLabel

# 为了导入上层的工具包，将上层的路径添加到环境变量
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from Utils import make_folder, save_string_2_file

data_folder = os.path.join(os.path.split(os.path.abspath(os.sys.argv[0]))[0], "data")


def get_chars():
    complete_chars = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    live_chars = [
        '3', '4', '5', '6',
        'd', 'p', 's', 'y',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    Sohu_chars = [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y'
    ]
    EBay_chars = [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N',
        'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    Baidu_chars = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y'
    ]
    _360_chars = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q',
        'r', 's', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q',
        'R', 'S', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    Jd_chars = [
        '3', '4', '5', '6', '8',
        'A', 'B', 'C', 'E', 'F', 'H', 'K', 'M', 'N', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y'
    ]
    Weibo_chars = [
        '2', '3', '4', '6', '7', '8', '9',
        'A', 'B', 'C', 'E', 'F', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R',
        'S', 'T', 'V', 'W', 'X', 'Y', 'Z'
    ]
    Ebay_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    Sina_chars = [
        '2', '3', '4', '5', '6', '7', '8',
        'a', 'b', 'c', 'd', 'e', 'f', 'h', 'k', 'm', 'n', 'p', 'q', 's', 'u',
        'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'P', 'Q', 'R', 'S',
        'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    # xin
    # len = 6
    Blizzard_chars = [
        'a', 'b', 'c', 'd', 'e', 'f', 'h', 'k', 'm', 'n', 'p', 'q', 's', 'u',
        'v', 'w', 'x', 'y', 'z', 'g'
    ]
    # 5
    Authorize_chars = [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 'u', 'v', 'w', 'x', 'y', 'z',
    ]
    # 6
    Captcha_chars = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ]
    # 5
    NIH_chars = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    # 6
    Reddit_chars = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    # 5
    Digg_chars = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ]
    # 4
    Baidu_2016_chars = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ]
    # 4
    QQ_chars = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    # 5
    Sina_old_chars = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'd', 'e', 'f', 'g', 'h', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't'
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    # 8
    reCaptcha_chars = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ]
    # 6
    Amazon_chars = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    # 7
    Yahoo_chars = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    return Baidu_2016_chars


def get_labels(chars, captcha_number, captcha_len):
    label = CaptchaLabel(chars, captcha_len)
    labels = []
    for _ in range(captcha_number):
        labels.append(label.get_label())
    return '#'.join(labels)


def main():
    label_folder = os.path.join(data_folder, "labels")
    make_folder(label_folder)

    chars = get_chars()
    captcha_number = 2000
    captcha_len = 4
    labels = get_labels(chars, captcha_number, captcha_len)
    print(labels)
    save_string_2_file(os.path.join(label_folder, "Baidu_off_2000_labels.txt"), labels)


if __name__ == '__main__':
    main()
