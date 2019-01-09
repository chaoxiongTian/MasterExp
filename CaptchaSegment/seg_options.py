# -*- coding: utf-8 -*-
# @Time    : 19-1-8 下午10:53
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : seg_options.py
# @Software: PyCharm

import argparse


class Options:
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def initialize(self):
        self.parser.add_argument('--captcha', dest='captcha', help='captcha_name', type=str, default='qq')
        self.parser.add_argument('--use', dest='use', help='cnn or seg', type=str, default='seg')
        self.parser.add_argument('--tar', dest='tar', help='segment folder', type=str, default='org')
        self.parser.add_argument('--cond', dest='cond', help='pre,conditions', type=str, default='')

    def parse(self):
        self.initialize()
        self.opt = self.parser.parse_args()
        return self.opt
