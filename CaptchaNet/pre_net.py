# -*- coding: utf-8 -*-
# @Time    : 18-12-27 下午8:19
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : solver.py
# @Software: PyCharm

# pytorch
import torch
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F
import torch.nn as nn
import numpy as np

import random
# from adversary import Attack
from out_utils import *
from models.core_net import CNN
from models.core_net import CNN_256


def cuda(tensor, is_cuda):
    if is_cuda:
        return tensor.cuda()
    else:
        return tensor


def get_data(data_sets, flag, num):
    folder = os.path.join(data_sets, flag)
    image_paths = [os.path.join(folder, str(i) + '.png') for i in range(num)]
    labels = open(os.path.join(data_sets, flag + '_labels.txt'), 'r').read().strip().split('#')
    return [(image_paths[i], labels[i]) for i in range(num)]


# 向量转回文本
def vec2text(vec, idx_char):
    char_pos = vec.nonzero()[0]
    text = []
    for i, c in enumerate(char_pos):
        c = c - i * len(idx_char)
        text.append(idx_char.get(c))
    return "".join(text)


# 文本转向量
def text2vec(text, cap_len, char_idx):
    text_len = len(text)
    if text_len > cap_len:
        raise ValueError('labels len in over range')
    vector = np.zeros(cap_len * len(char_idx))
    for i, c in enumerate(text):
        idx = i * len(char_idx) + char_idx.get(c)
        vector[idx] = 1
    return vector


# 遍历验证码的labels 返回出现的字符集合
def get_char_set(train_data, test_data):
    def get_chars(data):
        char_sets = set()
        for _, labels in data:
            for i in labels:
                char_sets.add(i)
        return char_sets

    train_chars = get_chars(train_data)
    test_chars = get_chars(test_data)
    if sorted(train_chars) == sorted(test_chars):
        return list(train_chars)
    else:
        if len(train_chars) > len(test_chars):
            return list(train_chars)
        else:
            raise RuntimeError("train labels chars set is more than test")


# 获得 倍数 进1
def times(train_num, batch_size):
    if train_num % batch_size == 0:
        return int(train_num / batch_size)
    else:
        return int(train_num / batch_size) + 1


class PreNet(object):
    def __init__(self, args):
        self.args = args
        self.data_root = os.path.dirname(__file__)
        # 网络参数
        self.cuda = (args.cuda and torch.cuda.is_available())
        self.epoch = args.epoch
        self.batch_size = args.batch_size
        self.lr = args.lr
        self.mode = args.mode
        self.net = args.net

        # 需要的文件夹
        self.data_sets = os.path.join(self.data_root, args.data_sets, args.model_name)
        self.model_name = args.model_name
        self.ckpt_dir = os.path.join(self.data_root, args.ckpt_dir, args.model_name)
        self.load_ckpt = args.load_ckpt  # 有内容的时候才加载
        self.output_dir = os.path.join(self.data_root, args.output_dir, args.model_name)
        # 创建文件夹 模型保存地址 对抗样本输出地址
        make_folders(self.ckpt_dir, self.output_dir)

        # 验证码相关
        self.train_num = args.train_num
        self.test_num = args.test_num
        self.captcha_len = args.captcha_len
        # list [image_path,label]
        self.train_data = get_data(self.data_sets, 'train', self.train_num)
        self.test_data = get_data(self.data_sets, 'test', self.test_num)
        self.captcha_char_set = sorted(get_char_set(self.train_data, self.test_data))
        self.char_idx = {str(self.captcha_char_set[i]): i for i in range(len(self.captcha_char_set))}
        self.idx_char = {i: str(self.captcha_char_set[i]) for i in range(len(self.captcha_char_set))}

        # 对抗样本参数
        self.target = args.target
        self.iteration = args.iteration
        self.epsilon = args.epsilon

        self.bast_accuracy = 0
        self.model_init()

        if self.load_ckpt != '':
            self.load_checkpoint(os.path.join(self.data_root, self.ckpt_dir, args.load_ckpt))

        # criterion = nn.MultiLabelSoftMarginLoss
        # self.attack = Attack(self.net, criterion=criterion)

    # 初始化网络
    def model_init(self):
        if self.net == 'cnn':
            self.net = cuda(CNN(y_dim=self.captcha_len * len(self.captcha_char_set)), self.cuda)
        elif self.net == 'cnn_256':
            self.net = cuda(CNN_256(y_dim=self.captcha_len * len(self.captcha_char_set)), self.cuda)
        self.net.weight_init(_type='kaiming')  # 对net中的参数进行初始化
        print(self.net)
        # Optimizers 初始化优化器
        self.optim = optim.Adam([{'params': self.net.parameters(), 'lr': self.lr}],
                                betas=(0.5, 0.999))
        self.loss_func = nn.MultiLabelSoftMarginLoss()

    # train_data格式为：[images,labels] 分别将其转为tensor；batch_idx,表示第几个batch
    def cus_data_loader(self, batch_idx, batch_size, data):
        # 判断结余是否够一个batch
        start_idx = batch_idx * batch_size
        images = list()
        labels = list()
        count = 0

        while start_idx < len(data) and count < batch_size:
            image, label = data[start_idx]
            images.append(image_2_tensor(Image.open(image).convert('L')))
            labels.append(torch.from_numpy(text2vec(label, self.captcha_len, self.char_idx)))
            count += 1
            start_idx += 1
        return torch.stack(images, 0).float(), torch.stack(labels, 0).float()

    # 加载模型
    def load_checkpoint(self, file_path):
        if os.path.exists(file_path):
            print("=> loading checkpoint '{}'".format(file_path))
            checkpoint = torch.load(open(file_path, 'rb'))
            self.net.load_state_dict(checkpoint['model_states']['net'])
            self.optim.load_state_dict(checkpoint['optim_states']['optim'])
            print("=> loaded checkpoint '{}'".format(file_path))
        else:
            print("=> no checkpoint found at '{}'".format(file_path))

    # 保存模型
    def save_checkpoint(self, file_name):
        model_states = {
            'net': self.net.state_dict(),
        }
        optim_states = {
            'optim': self.optim.state_dict(),
        }
        states = {
            'model_states': model_states,
            'optim_states': optim_states,
        }
        file_path = os.path.join(self.ckpt_dir, file_name)
        torch.save(states, open(file_path, 'wb+'))
        print("=> saved checkpoint '{}'".format(file_path))

    def train(self):
        for epoch_idx in range(self.epoch):
            for batch_idx in range(times(self.train_num, self.batch_size)):
                images, labels = self.cus_data_loader(batch_idx, self.batch_size, self.train_data)
                x = Variable(cuda(images, self.cuda))
                y = Variable(cuda(labels, self.cuda))

                output = self.net(x)
                predict = torch.reshape(output, [-1, self.captcha_len, len(self.captcha_char_set)])
                max_idx_p = predict.max(2)[1]
                real = torch.reshape(y, [-1, self.captcha_len, len(self.captcha_char_set)])
                max_idx_l = real.max(2)[1]
                accuracy = max_idx_p.eq(max_idx_l).float().mean().item()

                cost = self.loss_func(output, y)
                self.optim.zero_grad()
                cost.backward()
                self.optim.step()

                if batch_idx % 4 == 0:
                    print('Epoch:', epoch_idx,
                          '| iter:', batch_idx * self.batch_size,
                          '| train loss: %.4f' % cost.item(),
                          '| train accuracy: %.3f' % accuracy)
            random.shuffle(self.train_data)
            self.test()

    def test(self):
        # 把test中所有的数据的大小直接作为一个batch 进行测试。
        images, labels = self.cus_data_loader(0, len(self.test_data), self.test_data)
        x = Variable(cuda(images, self.cuda))
        y = Variable(cuda(labels, self.cuda))

        output = self.net(x)
        predict = torch.reshape(output, [-1, self.captcha_len, len(self.captcha_char_set)])
        max_idx_p = predict.max(2)[1]

        real = torch.reshape(y, [-1, self.captcha_len, len(self.captcha_char_set)])
        max_idx_l = real.max(2)[1]
        accuracy = max_idx_p.eq(max_idx_l).float().mean().item()
        cost = self.loss_func(output, y)

        def index2vec(index_tensor):
            vector = np.zeros(self.captcha_len * len(self.captcha_char_set))
            for i in range(self.captcha_len):
                vector[index_tensor[i].item() + i * len(self.captcha_char_set)] = 1
            return vector

        for i in range(5):
            print("real:'{}' predict:'{}'".format(vec2text(index2vec(max_idx_l[i]), self.idx_char),
                                                  vec2text(index2vec(max_idx_p[i]), self.idx_char)))

        if accuracy >= self.bast_accuracy and self.mode == 'train':
            self.bast_accuracy = accuracy
            self.save_checkpoint('best_acc.tar')

        print('test loss: %.4f' % cost,
              '| test accuracy: %.3f' % accuracy,
              '| bast accuracy: %.3f\n' % self.bast_accuracy)

    # def generate(self, num_sample, target=-1, epsilon=0.03, alpha=2 / 255, iteration=1):
    #     # 无目标攻击。
    #     images, labels = self.cus_data_loader(0, len(self.test_data), self.test_data)
    #
    #     def pred_acc(input_x, real_y):
    #         output = self.net(input_x)
    #         predict = torch.reshape(output, [-1, self.captcha_len, len(self.captcha_char_set)])
    #         max_idx_p = predict.max(2)[1]
    #
    #         real = torch.reshape(real_y, [-1, self.captcha_len, len(self.captcha_char_set)])
    #         max_idx_l = real.max(2)[1]
    #         accuracy = max_idx_p.eq(max_idx_l).float().mean().item()
    #         cost = self.loss_func(output, real_y)
    #         return accuracy, cost
    #
    #     accuracy, cost = pred_acc(images, labels)  # 生成之前先做检测
    #     # 修改tensor x_adv
    #     x_adv = self.FGSM(images, labels, epsilon, alpha, iteration)
    #
    #     accuracy_adv, cost_adv = pred_acc(x_adv, labels)  # 再做检测
    #     print('[BEFORE] accuracy : {:.4f} cost : {:.4f}'.format(accuracy, cost))
    #     print('[AFTER] accuracy : {:.4f} cost : {:.4f}'.format(accuracy_adv, cost_adv))

    # 对抗样本生成算法
    # def FGSM(self, x, y_true, y_target=None, eps=0.03, alpha=2 / 255, iteration=1):
    #     x = Variable(cuda(x, self.cuda), requires_grad=True)
    #     y_true = Variable(cuda(y_true, self.cuda), requires_grad=False)
    #     targeted = False
    #     # 开始扰动
    #     if iteration == 1:
    #         if targeted:
    #             x_adv, h_adv, h = self.attack.fgsm(x, y_target, True, eps)
    #         else:
    #             x_adv, h_adv, h = self.attack.fgsm(x, y_true, False, eps)
    #     else:
    #         if targeted:
    #             x_adv, h_adv, h = self.attack.i_fgsm(x, y_target, True, eps, alpha, iteration)
    #         else:
    #             x_adv, h_adv, h = self.attack.i_fgsm(x, y_true, False, eps, alpha, iteration)
    #
    #     return x_adv.data
