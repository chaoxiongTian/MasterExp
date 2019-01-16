# -*- coding: utf-8 -*-
# @Time    : 18-12-10 下午4:16
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : options.py
# @Software: PyCharm

import argparse


class Options:
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def initialize(self):
        self.parser.add_argument('--captcha', dest='captcha', help='captcha_name', type=str, default='blizzard')
        self.parser.add_argument('--tar', dest='tar', help='train or test', type=str, default='ceshi')
        self.parser.add_argument('--labels', dest='labels', help='labels`s name', type=str, default='ceshi')
        self.parser.add_argument('--captcha_len', dest='captcha_len', help='captcha_len', type=int, default=4)
        self.parser.add_argument('--captcha_number', dest='captcha_number', help='captcha_number', type=int, default=20)
        self.parser.add_argument('--single_char', dest='single_char', help='save clean for single char train',
                                 type=bool, default=False)
        self.parser.add_argument('--origin_captcha', type=bool, default=False, help='save origin captcha not other')

    def parse(self):
        self.initialize()
        self.opt = self.parser.parse_args()
        return self.opt
