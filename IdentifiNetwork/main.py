# -*- coding: utf-8 -*-
# @Time    : 18-12-19 下午10:34
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : mnist.py
# @Software: PyCharm

import torch
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F

import numpy as np

from id_utils import *
from id_options import Options

from models.nets import CNN

opt = Options().parse()


# 网络的预处理类，包括定义网络的类型，网络的参数等等。
class PreNet(object):
    def __init__(self, options):
        self.opt = options  # 保存参数
        # 基本元素
        self.cuda = (options.cuda and torch.cuda.is_available())
        self.epoch = options.epoch
        self.batch_size = options.batch_size
        self.lr = options.lr
        self.mode = options.mode
        self.model_name = options.model_name  # 模型的名字，对应训练样本文件夹的名字，最后文件保存的文件名
        self.y_dim = return_y_dim(os.path.join(os.path.dirname(__file__),
                                               options.data_set_folder,
                                               options.model_name))  # TODO:根据训练数据文件夹返回需要的类别
        print('y_dim', self.y_dim)
        self.data_loader = return_loader(options)  # 返回data_loader

        # 设置模型保存的位置
        self.ckpt_folder = os.path.join(os.path.dirname(__file__), options.ckpt_dir, options.model_name)
        if not os.path.exists(self.ckpt_folder):
            make_folder(self.ckpt_folder)  # 不存在创建

        self.model_init()

        self.load_ckpt = options.load_ckpt
        # 没有指明调用用的模型 则调用 best_acc.tar
        if self.load_ckpt != '':
            self.load_checkpoint(self.load_ckpt)
        self.bast_accuracy = 0

    def model_init(self):
        # 加载网络
        self.net = cuda(CNN(channel=1, y_dim=10), self.cuda)
        # 凯明初始化
        self.net.weight_init(_type='kaiming')  # 对net中的参数进行初始化
        print(self.net)
        # 定义优化器
        self.optim = optim.Adam([{'params': self.net.parameters(), 'lr': self.lr}],
                                betas=(0.5, 0.999))

    def load_checkpoint(self, file_name='best_acc.tar'):
        file_path = os.path.join(self.ckpt_folder, file_name)
        if os.path.exists(file_path):
            print("=> loading checkpoint '{}'".format(file_path))
            checkpoint = torch.load(open(file_path, 'rb'))
            self.net.load_state_dict(checkpoint['model_states']['net'])
            self.optim.load_state_dict(checkpoint['optim_states']['optim'])

        else:
            print("=> no checkpoint found at '{}'".format(file_path))

    def save_checkpoint(self, file_name='ckpt.tar'):
        model_states = {
            'net': self.net.state_dict(),
        }
        optim_states = {
            'optim': self.optim.state_dict(),
        }
        states = {
            'args': self.opt,
            'model_states': model_states,
            'optim_states': optim_states,
        }
        file_path = os.path.join(self.ckpt_folder, file_name)
        torch.save(states, open(file_path, 'wb+'))
        print("=> saved checkpoint '{}'".format(file_path))

    def train(self):
        for epoch_idx in range(self.epoch):
            for batch_idx, (batch_images, batch_labels) in enumerate(self.data_loader['train']):
                x = Variable(cuda(batch_images, self.cuda))
                y = Variable(cuda(batch_labels, self.cuda))
                output = self.net(x)[0]
                prediction = output.max(1)[1]
                # 求准确率
                accuracy = prediction.eq(y).float().mean().item()
                cost = F.cross_entropy(output, y)

                self.optim.zero_grad()
                cost.backward()
                self.optim.step()

                if batch_idx % 100 == 0:
                    print(self.model_name)
                    print('Epoch:', epoch_idx, '| train loss: %.4f' % cost.item(),
                          '| train accuracy: %.3f' % accuracy)
            self.test()

    def test(self):
        accuracy = 0.
        cost = 0.
        total = 0.
        for batch_idx, (batch_images, batch_labels) in enumerate(self.data_loader['test']):
            x = Variable(cuda(batch_images, self.cuda))
            y = Variable(cuda(batch_labels, self.cuda))

            output = self.net(x)[0]
            prediction = output.max(1)[1]

            accuracy += prediction.eq(y).float().sum().item()
            cost += F.cross_entropy(output, y, reduction='mean').item()
            total += x.size(0)
        accuracy = accuracy / total
        cost /= total
        print('test loss: %.4f' % cost, '| test accuracy: %.3f' % accuracy)
        if accuracy >= self.bast_accuracy and self.mode == 'train':
            self.bast_accuracy = accuracy
            self.save_checkpoint('best_acc.tar')


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

    net = PreNet(opt)  # 初始化网络，初始化网络参数，初始化网络优化器等等。

    if opt.mode == 'train':
        net.train()
    else:
        net.test()
    print('[*] Finished')
