# -*- coding: utf-8 -*-
# @Time    : 18-12-27 下午8:11
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : net_options.py
# @Software: PyCharm

import argparse


class Options:
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def initialize(self):
        # 训练参数
        self.parser.add_argument('--cuda', type=bool, default=True, help='enable cuda')  # 是否使用cuda
        self.parser.add_argument('--seed', type=int, default=1, help='random seed')  # 随机因子
        self.parser.add_argument('--epoch', type=int, default=20, help='epoch size')  # 循环次数
        self.parser.add_argument('--batch_size', type=int, default=64, help='mini-batch size')  # 批大小
        self.parser.add_argument('--lr', type=float, default=0.001, help='learning rate')  # 学习率
        self.parser.add_argument('--net', type=str, default='cnn', help='which net')

        # 文件夹
        self.parser.add_argument('--data_sets', type=str, default='data_sets', help='dataset directory path')  # 目录
        self.parser.add_argument('--output_dir', type=str, default='output', help='output directory path')  # 输出目录
        self.parser.add_argument('--ckpt_dir', type=str, default='checkpoints', help='checkpoint directory path')
        self.parser.add_argument('--load_ckpt', type=str, default='', help='')  # 加载模型的名字
        self.parser.add_argument('--captcha', type=str, default='jd', help='experiment name')  # 模型的名字（文件夹名）
        self.parser.add_argument('--mode', type=str, default='train', help='train / test / generate ')
        self.parser.add_argument('--train_folder', type=str, default='train', help='name of train folder ')
        self.parser.add_argument('--test_folder', type=str, default='test', help='name of test folder ')
        self.parser.add_argument('--silent', type=bool, default=False, help='')

        # 验证码相关
        self.parser.add_argument('--train_num', type=int, default=0, help='the number of train sets')
        self.parser.add_argument('--test_num', type=int, default=0, help='the number of test sets')
        self.parser.add_argument('--captcha_len', type=int, default=4, help='the len of captcha in labels')
        self.parser.add_argument('--real_captcha_len', type=int, default=0, help='the len of captcha in real')

        # 对抗样本
        self.parser.add_argument('--target', type=int, default=-1, help='target class for targeted generation')
        self.parser.add_argument('--iteration', type=int, default=3, help='the number of iteration for FGSM')  # 对抗样本算法
        self.parser.add_argument('--epsilon', type=float, default=0.03, help='epsilon for FGSM and i-FGSM')
        self.parser.add_argument('--alpha', type=float, default=2 / 255, help='alpha for i-FGSM')
        self.parser.add_argument('--fun', type=str, default='fgsm', help='FGSM or deepfool')

        # 可视化
        self.parser.add_argument('--tensorboard', type=bool, default=False, help='enable tensorboard')
        self.parser.add_argument('--visdom', type=bool, default=False, help='enable visdom')  # 数据可视化
        self.parser.add_argument('--visdom_port', type=str, default=55558, help='visdom port')

    def parse(self):
        self.initialize()
        self.opt = self.parser.parse_args()
        return self.opt
