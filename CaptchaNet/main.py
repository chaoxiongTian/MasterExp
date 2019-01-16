# -*- coding: utf-8 -*-
# @Time    : 18-12-27 下午8:16
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : main.py
# @Software: PyCharm

# pytorch
import torch
import numpy as np

from net_options import Options
from pre_net import PreNet

opt = Options().parse()
if __name__ == '__main__':
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

    net = PreNet(opt)

    if opt.mode == 'train':
        net.train()
    elif opt.mode == 'test':
        net.test()
    elif opt.mode == 'generate':
        net.generate(epsilon=opt.epsilon,  # 扰动因子
                     alpha=opt.alpha,  # alpha for i-FGSM  2 / 255
                     iteration=opt.iteration)  # the number of iteration for FGSM
    print('[*] Finished')

