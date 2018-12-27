# -*- coding: utf-8 -*-
# @Time    : 18-12-21 下午10:45
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : options.py
# @Software: PyCharm

import argparse
from adversarial_utils import str2bool


class Options:
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def initialize(self):
        self.parser.add_argument('--epoch', type=int, default=20, help='epoch size')  # 循环次数
        self.parser.add_argument('--batch_size', type=int, default=100, help='mini-batch size')  # 批大小
        self.parser.add_argument('--lr', type=float, default=0.001, help='learning rate')  # 学习率
        self.parser.add_argument('--y_dim', type=int, default=10, help='the number of classes')  # 目标类别
        self.parser.add_argument('--target', type=int, default=-1,
                                 help='target class for targeted generation')  # 含目标攻击时候的目标
        # self.parser.add_argument('--eps', type=float, default=1e-9, help='epsilon')  # 干扰因子
        self.parser.add_argument('--model_name', type=str, default='main', help='experiment name')  # 模型的名字（文件夹名）
        self.parser.add_argument('--data_type', type=str, default='FMNIST', help='dataset type')  # 攻击的类型（这里用来限制loader的样子）
        self.parser.add_argument('--data_set_folder', type=str, default='data_sets', help='dataset directory path')  # 目录
        self.parser.add_argument('--summary_dir', type=str, default='summary', help='summary directory path')  #
        self.parser.add_argument('--output_dir', type=str, default='output', help='output directory path')  # 输出目录
        self.parser.add_argument('--ckpt_dir', type=str, default='checkpoints',
                                 help='checkpoint directory path')  # 模型目录
        self.parser.add_argument('--load_ckpt', type=str, default='', help='')  # 加载模型的名字
        self.parser.add_argument('--cuda', type=str2bool, default=True, help='enable cuda')  # 是否使用cuda
        self.parser.add_argument('--silent', type=str2bool, default=False, help='')  #
        self.parser.add_argument('--mode', type=str, default='train',
                                 help='train / test / generate / universal')  # 训练的类型
        self.parser.add_argument('--seed', type=int, default=1, help='random seed')  # 随机因子
        self.parser.add_argument('--iteration', type=int, default=3, help='the number of iteration for FGSM')  # 对抗样本算法
        self.parser.add_argument('--epsilon', type=float, default=0.03, help='epsilon for FGSM and i-FGSM')  # ？？
        self.parser.add_argument('--alpha', type=float, default=2 / 255, help='alpha for i-FGSM')  # ？？
        self.parser.add_argument('--tensorboard', type=str2bool, default=False, help='enable tensorboard')  # ？？
        self.parser.add_argument('--visdom', type=str2bool, default=False, help='enable visdom')  # 数据可视化
        self.parser.add_argument('--visdom_port', type=str, default=55558, help='visdom port')

    def parse(self):
        self.initialize()
        self.opt = self.parser.parse_args()
        return self.opt
