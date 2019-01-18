# -*- coding: utf-8 -*-
# @Time    : 19-1-18 下午5:04
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : read_log.py
# @Software: PyCharm

from out_utils import *


def main():
    file_path = '/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/CaptchaNet/checkpoints/mnist/SimpleCnn5/log.pickle'
    order_log = load_pickle(file_path)
    train_acc, train_lost = order_log['train_acc'], order_log['train_lost']
    test_acc, test_lost = order_log['test_acc'], order_log['test_lost']
    for i in range(len(train_acc)):
        print(train_acc[i], train_lost[i], test_acc[i], test_lost[i])


if __name__ == '__main__':
    main()
