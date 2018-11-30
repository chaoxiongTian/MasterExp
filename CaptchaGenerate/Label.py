# -*- coding: utf-8 -*-
# @Time    : 18-11-29 下午10:49
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : Label.py
# @Software: PyCharm Community Edition

import random


class CaptchaLabel(object):
    chars = []
    captcha_len = 0

    def __init__(self, chars, captcha_len):  # captcha_len 每个验证码中字符的个数
        self.chars = chars
        self.captcha_len = captcha_len
        self.get_label()

    def get_label(self):
        label = []
        for _ in range(self.captcha_len):
            label.append(random.choice(self.chars))
        return ''.join(label)
