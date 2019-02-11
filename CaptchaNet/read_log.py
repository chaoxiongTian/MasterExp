# -*- coding: utf-8 -*-
# @Time    : 19-1-18 下午5:04
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : read_log.py
# @Software: PyCharm

import matplotlib.pyplot as plt
import numpy as np
from out_utils import *
from net_options import Options

opt = Options().parse()
log_folder = os.path.join(os.path.dirname(__file__), opt.ckpt_dir, opt.captcha, opt.net)
log_path = os.path.join(log_folder, 'log.pickle')
print('log image save in {}'.format(log_path))


def draw(train_acc, train_lost, test_acc, test_lost):
    length = len(train_acc)
    epoch = np.arange(0, length, 1)

    # 设置坐标轴及刻度
    my_x_ticks = np.arange(0, length, 50)
    my_y_ticks = np.arange(0.0, 1.0, 0.1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)

    # 子图1：训练集
    plt.subplot(2, 1, 1)
    plt.plot(epoch, train_acc, color='black', label='train_accuracy')
    plt.plot(epoch, train_lost, color='green', label='train_lost')
    # plt.title('Baidu captcha accuracy & loss')

    # 显示图例
    plt.legend()

    # 设置坐标轴名称
    plt.xlabel('epoch')
    plt.ylabel('train value')

    # 子图2：测试集
    plt.subplot(2, 1, 2)
    plt.plot(epoch, test_acc, color='red', label='test_accuracy')
    plt.plot(epoch, test_lost, color='orange', label='test_lost')

    plt.legend()

    plt.xlabel('epoch')
    plt.ylabel('test value')

    # 保存图片
    plt.savefig(os.path.join(log_folder, 'log.png'))
    plt.show()


def main():
    order_log = load_pickle(log_path)
    train_acc, train_lost = order_log['train_acc'], order_log['train_lost']
    test_acc, test_lost = order_log['test_acc'], order_log['test_lost']
    draw(train_acc, train_lost, test_acc, test_lost)


if __name__ == '__main__':
    main()
