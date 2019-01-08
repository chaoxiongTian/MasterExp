# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : CaptchaGenerate.py
# @Software: PyCharm Community Edition

from out_utils import *
from label import CaptchaLabel
from options import Options

opt = Options().parse()

switch = {
    'complete': [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'live': [
        '3', '4', '5', '6',
        'd', 'p', 's', 'y',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'sohu': [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y'
    ],
    'baidu_2018': [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y'
    ],
    '360': [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q',
        'r', 's', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q',
        'R', 'S', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'jd': [
        '3', '4', '5', '6', '8',
        'A', 'B', 'C', 'E', 'F', 'H', 'K', 'M', 'N', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y'
    ],
    'weibo': [
        '2', '3', '4', '6', '7', '8', '9',
        'A', 'B', 'C', 'E', 'F', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R',
        'S', 'T', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'ebay': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'sina': [
        '2', '3', '4', '5', '6', '7', '8',
        'a', 'b', 'c', 'd', 'e', 'f', 'h', 'k', 'm', 'n', 'p', 'q', 's', 'u',
        'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'P', 'Q', 'R', 'S',
        'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'megaupload': [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'blizzard': [
        'a', 'b', 'c', 'd', 'e', 'f', 'h', 'k', 'm', 'n', 'p', 'q', 's', 'u',
        'v', 'w', 'x', 'y', 'z', 'g'
    ],
    'authorize': [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 'u', 'v', 'w', 'x', 'y', 'z',
    ],
    'captcha_net': [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ],
    'nih': [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'reddit': [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'digg': [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ],
    'baidu': [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ],
    'qq': [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'sina_2014': [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'd', 'e', 'f', 'g', 'h', 'm', 'n',
        'q', 'r', 't',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'recaptcha_2011': [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    ],
    'amazon': [
        'A', 'B', 'C', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'T', 'U', 'X', 'Y'
    ],
    'yahoo': [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'd', 'e', 'f', 'g', 'h', 'm', 'n',
        'q', 'r', 't',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'recaptcha_2013': [
        'b', 'd', 'e', 'f', 'h', 'q', 'r', 't',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'baidu_2011': [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'baidu_2013': [
        'a', 'b', 'd', 'e', 'f', 'g', 'h',
        'q', 'r', 't', 'y',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'paypal': [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k',
        'p', 'q', 'r', 't', 'u', 'v', 'w', 'x', 'y',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ],
    'cnn': [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ],
}

captcha_name = opt.captcha
# folder = opt.tar
labels_name = captcha_name + "_" + opt.labels + "_labels.txt"
captcha_number = opt.captcha_number
captcha_len = opt.captcha_len


def get_labels(chars):
    label = CaptchaLabel(chars, captcha_len)
    labels = []
    for _ in range(captcha_number):
        l = label.get_label()
        # print('out:', len(l), l)
        if len(l) == captcha_len:
            labels.append(l)
        else:
            raise RuntimeError('char sets has error')

    return '#'.join(labels)


def main():
    label_folder = os.path.join(data_folder, "labels")
    make_folder(label_folder)

    chars = switch[captcha_name]
    labels = get_labels(chars)
    print(labels_name, ":", labels)
    save_string_2_file(os.path.join(label_folder, labels_name), labels)


if __name__ == '__main__':
    main()
