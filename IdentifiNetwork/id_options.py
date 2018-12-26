# -*- coding: utf-8 -*-
# @Time    : 18-12-21 下午10:45
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : options.py
# @Software: PyCharm

import argparse
from id_utils import str2bool


class Options:
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def initialize(self):
        self.parser.add_argument('--epoch', type=int, default=20, help='epoch size')  # 循环次数
        self.parser.add_argument('--batch_size', type=int, default=100, help='mini-batch size')  # 批大小
        self.parser.add_argument('--lr', type=float, default=0.001, help='learning rate')  # 学习率
        self.parser.add_argument('--y_dim', type=int, default=10, help='the number of classes')  # 目标类别
        self.parser.add_argument('--model_name', type=str, default='d_mnist', help='dataset and model save_name')  # 目录
        self.parser.add_argument('--data_set_folder', type=str, default='data_sets', help='dataset directory path')  # 目录
        self.parser.add_argument('--ckpt_dir', type=str, default='checkpoints',
                                 help='checkpoint directory path')  # 模型目录
        self.parser.add_argument('--load_ckpt', type=str, default='', help='')  # 加载模型的名字
        self.parser.add_argument('--cuda', type=str2bool, default=True, help='enable cuda')  # 是否使用cuda
        self.parser.add_argument('--mode', type=str, default='train',
                                 help='train / test / generate / universal')  # 训练的类型
        self.parser.add_argument('--seed', type=int, default=1, help='random seed')  # 随机因子
        # 是否为验证码如果是验证码需要提供 字符的顺序
        self.parser.add_argument('--captcha', type=bool, default=False, help='captcha or not')
        self.parser.add_argument('--captcha_len', type=int, default=4, help='captcha')
    def parse(self):
        self.initialize()
        self.opt = self.parser.parse_args()
        return self.opt
