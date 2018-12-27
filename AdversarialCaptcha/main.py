# -*- coding: utf-8 -*-
# @Time    : 18-12-21 下午10:45
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : train.py
# @Software: PyCharm

import torch
import numpy as np

from solver import Solver

from ad_options import Options

opt = Options().parse()

if __name__ == "__main__":
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True
    seed = opt.seed  # 设置随机种子
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    np.set_printoptions(precision=4)  # 设置精度
    torch.set_printoptions(precision=4)

    print('\n[ARGUMENTS]')
    print(opt)

    # 初始化网络，初始化网络参数，初始化网络优化器等，参数放在Solver 的net实例中。
    net = Solver(opt)

    if opt.mode == 'train':
        net.train()
    elif opt.mode == 'test':
        net.test()
    elif opt.mode == 'generate':
        net.generate(num_sample=len(net.test_data),
                     target=opt.target,
                     epsilon=opt.epsilon,
                     alpha=opt.alpha,
                     iteration=opt.iteration)
    elif opt.mode == 'universal':
        net.universal(opt)
    print('[*] Finished')
