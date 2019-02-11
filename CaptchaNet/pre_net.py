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
from cap_adversary import Attack
from out_utils import *
from models.core_net import SimpleCnn3, SimpleCnn5, SimpleCnn128, LeNet5, AlexNet, GoogLeNet


def cuda(tensor, is_cuda):
    if is_cuda:
        return tensor.cuda()
    else:
        return tensor


# 这里用来制定多GPU有一些BUG,没有继续尝试,而是使用 CUDA_VISIBLE_DEVICES=id 来制定运行的gpu
def gpu_ids(net, is_cuda, ids):
    if is_cuda:
        # net = torch.nn.DataParallel(net, device_ids=ids)
        return cuda(net, is_cuda)
    else:
        return net


def get_data(data_sets, folder, labels, num):
    folder = os.path.join(data_sets, folder)
    if num == 0:
        num = len(os.listdir(folder))
    image_paths = [os.path.join(folder, str(i) + '.png') for i in range(num)]
    label_path = os.path.join(data_sets, labels)
    labels = open(label_path, 'r').read().strip().split('#')
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


def save_image(tensor, nrow=8, padding=2,
               normalize=False, range=None, scale_each=False):
    from PIL import Image
    tensor = tensor.cpu()
    from torchvision.utils import make_grid
    grid = make_grid(tensor, nrow=nrow, padding=padding,
                     normalize=normalize, range=range, scale_each=scale_each)
    ndarr = grid.mul(255).clamp(0, 255).byte().permute(1, 2, 0).numpy()
    im = Image.fromarray(ndarr)
    return im


# 保存tensor类型的image
def save_perturbed_image(tensor, folder, w, h):
    make_folder(folder)
    for i in range(len(tensor)):
        image_path = os.path.join(folder, str(i) + '.png')
        print("num.'{}'is saved".format(i))
        # im = tensor_2_image(tensor[i])
        im = save_image(tensor[i], padding=0)
        image_resize(im, w, h).save(image_path)


# 解析gpu_id
def parse_gpu_id(gpu_id):
    gpu_ids = list()
    for each in gpu_id.split(','):
        try:
            id = int(each)
            if id < 4:
                gpu_ids.append(id)
            else:
                raise RuntimeError(" gpu ids input error")
        except:
            raise RuntimeError(" gpu ids input error")
    return gpu_ids


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
        self.net_str = args.net
        self.gpu_ids = parse_gpu_id(args.gpu_id)

        # 需要的文件夹
        self.data_sets = os.path.join(self.data_root, args.data_sets, args.captcha)
        self.captcha_name = args.captcha
        self.ckpt_dir = os.path.join(self.data_root, args.ckpt_dir, args.captcha, self.net_str)
        self.load_ckpt = args.load_ckpt  # 有内容的时候才加载
        self.output_dir = os.path.join(self.data_sets, 'perturbed')
        # 创建文件夹 模型保存地址 对抗样本输出地址
        make_folder(self.ckpt_dir)

        # 验证码相关 如果都没有赋值就都是0，则按照文件夹取，取完之后重新赋值。
        self.train_num = args.train_num
        self.test_num = args.test_num
        # list [image_path,label]
        self.train_data = get_data(self.data_sets, args.train_folder, args.train_labels, self.train_num)
        self.test_data = get_data(self.data_sets, args.test_folder, args.test_labels, self.test_num)
        self.train_num = len(self.train_data)
        self.test_num = len(self.test_data)
        self.captcha_len = len(self.train_data[0][1])
        self.captcha_w, self.captcha_h = Image.open(self.train_data[0][0]).size
        self.real_captcha_len = args.real_captcha_len
        self.captcha_char_set = sorted(get_char_set(self.train_data, self.test_data))
        self.dim = self.captcha_len * len(self.captcha_char_set)
        self.char_idx = {str(self.captcha_char_set[i]): i for i in range(len(self.captcha_char_set))}
        self.idx_char = {i: str(self.captcha_char_set[i]) for i in range(len(self.captcha_char_set))}

        #  数据输出
        self.train_acc = list()
        self.train_lost = list()
        self.test_acc = list()
        self.test_lost = list()

        # 对抗样本参数
        self.target = args.target
        self.iteration = args.iteration
        self.epsilon = args.epsilon
        self.fun = args.fun

        self.bast_accuracy = 0
        self.bast_real_accuracy = 0
        self.model_init()

        if self.load_ckpt != '':
            self.load_checkpoint(os.path.join(self.data_root, self.ckpt_dir, args.load_ckpt))

    def get_net(self, prob=0):
        print('load net :', self.net_str)
        # TODO:bug 可以把数据放在不同的gpu中,不过取出数据的时候出错.
        if self.net_str == 'SimpleCnn3':
            net = gpu_ids(SimpleCnn3(y_dim=self.captcha_len * len(self.captcha_char_set), keep_prob=prob), self.cuda,
                          self.gpu_ids)
        elif self.net_str == 'SimpleCnn5':
            net = gpu_ids(SimpleCnn5(y_dim=self.captcha_len * len(self.captcha_char_set), keep_prob=prob), self.cuda,
                          self.gpu_ids)
        elif self.net_str == 'SimpleCnn128':
            net = gpu_ids(SimpleCnn128(y_dim=self.captcha_len * len(self.captcha_char_set), keep_prob=prob), self.cuda,
                          self.gpu_ids)
        elif self.net_str == 'LeNet5':
            net = gpu_ids(LeNet5(y_dim=self.captcha_len * len(self.captcha_char_set), keep_prob=prob), self.cuda,
                          self.gpu_ids)
        elif self.net_str == 'AlexNet':
            net = gpu_ids(AlexNet(y_dim=self.captcha_len * len(self.captcha_char_set), keep_prob=prob), self.cuda,
                          self.gpu_ids)
        elif self.net_str == 'GoogLeNet':
            net = gpu_ids(GoogLeNet(y_dim=self.captcha_len * len(self.captcha_char_set), keep_prob=prob), self.cuda,
                          self.gpu_ids)
        else:
            raise RuntimeError("Net param input error")
        return net

    # 初始化网络
    def model_init(self):
        if self.mode == 'train':
            prob = 0.4
        else:
            prob = 0
        self.net = self.get_net(prob=prob)
        # self.net.weight_init(_type='kaiming')  # 对net中的参数进行初始化
        self.test_net = self.get_net(prob=0)
        # self.test_net.weight_init(_type='kaiming')  # 对net中的参数进行初始化
        # Optimizers 初始化优化器
        self.optim = optim.Adam([{'params': self.net.parameters(), 'lr': self.lr}],
                                betas=(0.5, 0.999))
        self.loss_func = nn.MultiLabelSoftMarginLoss()
        self.attack = Attack(self.test_net, criterion=self.loss_func)

    # train_data格式为：[images,labels] 分别将其转为tensor；batch_idx,表示第几个batch
    def cus_data_loader(self, batch_idx, batch_size, data):
        # 判断结余是否够一个batch
        start_idx = batch_idx * batch_size
        images = list()
        labels = list()
        count = 0

        while start_idx < len(data) and count < batch_size:
            image, label = data[start_idx]
            # 对尺寸做检测，如果使用的是cnn 图片大小不是28*28 将其改为resize 28*28 128。
            image = Image.open(image)
            w, h = image.size
            if self.net_str == 'SimpleCnn3' or self.net_str == 'SimpleCnn5' or self.net_str == 'LeNet5':  # 28*28
                if w != 28 and h != 28:
                    image = image_resize(image, 28, 28)
            elif self.net_str == 'SimpleCnn128':  # 128*128
                if w != 128 and h != 128:
                    image = image_resize(image, 128, 128)
            elif self.net_str == 'AlexNet':  # 227*227
                if w != 227 and h != 227:
                    image = image_resize(image, 227, 227)
            elif self.net_str == 'GoogLeNet':  # 96*96
                if w != 32 and h != 32:
                    image = image_resize(image, 32, 32)
            else:
                raise RuntimeError("net input error")
            images.append(image_2_tensor(image.convert('L')))
            labels.append(torch.from_numpy(text2vec(label, self.captcha_len, self.char_idx)))
            count += 1
            start_idx += 1
        return torch.stack(images, 0).float(), torch.stack(labels, 0).float()

    # 加载模型
    def load_checkpoint(self, file_path):
        if os.path.exists(file_path):
            print("=> loading checkpoint '{}'".format(file_path))
            if torch.cuda.is_available():
                checkpoint = torch.load(open(file_path, 'rb'))
            else:
                # cpu 加载 bug
                checkpoint = torch.load(open(file_path, 'rb'), map_location='cpu')
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
            print(self.captcha_name)
            epoch_acc, epoch_loss = 0., 0.
            total = 0.
            for batch_idx in range(times(self.train_num, self.batch_size)):
                images, labels = self.cus_data_loader(batch_idx, self.batch_size, self.train_data)
                x = Variable(cuda(images, self.cuda))
                y = Variable(cuda(labels, self.cuda))

                output = self.net(x)
                predict = output.view([-1, self.captcha_len, len(self.captcha_char_set)])
                max_idx_p = predict.max(2)[1]
                real = y.view([-1, self.captcha_len, len(self.captcha_char_set)])
                max_idx_l = real.max(2)[1]
                # bug
                correct = max_idx_p.eq(max_idx_l).float().mean().item()

                cost = self.loss_func(output, y)
                self.optim.zero_grad()
                cost.backward()
                self.optim.step()

                if batch_idx % 4 == 0:
                    print('Epoch:', epoch_idx,
                          '| iter:', batch_idx * self.batch_size,
                          '| train loss: %.4f' % cost.item(),
                          '| train accuracy: %.3f' % correct)
                epoch_acc = epoch_acc + correct
                epoch_loss = epoch_loss + cost.item()
                total += 1

            random.shuffle(self.train_data)
            self.train_acc.append(epoch_acc / total)
            self.train_lost.append(epoch_loss / total)
            self.test()
        log_dict = {'train_acc': self.train_acc,
                    'train_lost': self.train_lost,
                    'test_acc': self.test_acc,
                    'test_lost': self.test_lost}
        log_path = os.path.join(self.ckpt_dir, self.mode + '_log.pickle')
        save_pickle(log_path, log_dict)

    def test(self):
        # 把test中所有的数据按照batch_size = captcha_len 进行测试。
        self.test_net.load_state_dict(self.net.state_dict())

        if self.real_captcha_len == 0:
            # 表示这是一般的测试，不存在验证码分割之后的整体与预估
            test_batch = len(self.test_data)
            Times = 1
        else:
            if self.test_num % self.real_captcha_len != 0:
                raise RuntimeError("There is a problem with the test sample")
            test_batch = self.real_captcha_len
            Times = int(self.test_num / self.real_captcha_len)
        accuracy = 0.
        cost = 0.
        com_correct = 0.
        total = 0.
        for i in range(Times):
            images, labels = self.cus_data_loader(i, test_batch, self.test_data)
            x = Variable(cuda(images, self.cuda))
            y = Variable(cuda(labels, self.cuda))
            output = self.test_net(x)
            predict = output.view([-1, self.captcha_len, len(self.captcha_char_set)])
            max_idx_p = predict.max(2)[1]

            real = y.view([-1, self.captcha_len, len(self.captcha_char_set)])
            max_idx_l = real.max(2)[1]
            # 如果是普通的训练　把前两个预测结果做一个打印．
            if self.real_captcha_len == 0:
                self.show_predict(2, max_idx_p, max_idx_l)
                pd, pd_num = self.get_pd(len(labels), max_idx_p, max_idx_l)
                # print("test num : {} | acc num: | acc : {}".format(len(labels), pd_num, pd))
            correct = max_idx_p.eq(max_idx_l).float().mean().item()
            if correct == 1:
                com_correct += 1
            accuracy = accuracy + correct
            cost += self.loss_func(output, y).item()
            total += 1
        accuracy = accuracy / total
        cost = cost / total
        self.test_acc.append(accuracy)
        self.test_lost.append(cost)

        # 选择最好的模型保存
        if accuracy > self.bast_accuracy and (self.mode == 'train' or self.mode == 'fine'):
            self.bast_accuracy = accuracy
            self.save_checkpoint(self.mode + '_best_acc.tar')

        print('test loss: %.4f' % cost,
              '| test accuracy: %.3f' % accuracy,
              '| bast accuracy: %.3f' % self.bast_accuracy)

        if self.real_captcha_len != 0:  # 分割之后的验证码需要检查出最大的验证码准确率进行保存
            real_accuracy = com_correct / 200
            if real_accuracy > self.bast_real_accuracy and self.mode == 'train':
                self.bast_real_accuracy = real_accuracy
                self.save_checkpoint('best_acc_captcha.tar')
            print('real num: %.1f' % com_correct,
                  '| real accuracy: %.3f' % real_accuracy,
                  '| bast real accuracy: %.3f\n' % self.bast_real_accuracy)

    def fine_tune(self):
        # TODO: 加载模型 使用新的数据集合重新迭代训练. 之后保存模型.
        # 1. 测试之前的准确率.
        self.test()
        # 2. 在之前的模型上继续训练.
        self.train()

    def get_pd(self, num, max_idx_l, max_idx_p):
        def index2vec(index_tensor):
            vector = np.zeros(self.captcha_len * len(self.captcha_char_set))
            for i in range(self.captcha_len):
                # bug item()版本问题。
                vector[index_tensor[i].item() + i * len(self.captcha_char_set)] = 1
            return vector
        count = 0
        for i in range(num):
            pre = vec2text(index2vec(max_idx_l[i]), self.idx_char)
            real = vec2text(index2vec(max_idx_p[i]), self.idx_char)
            if pre == real:
                count += 1
        print(num, count, (count/num))
        return (count / num), count

    def show_predict(self, num, max_idx_l, max_idx_p):
        def index2vec(index_tensor):
            vector = np.zeros(self.captcha_len * len(self.captcha_char_set))
            for i in range(self.captcha_len):
                # bug item()版本问题。
                vector[index_tensor[i].item() + i * len(self.captcha_char_set)] = 1
            return vector

        for i in range(num):
            print("real:'{}' predict:'{}'".format(vec2text(index2vec(max_idx_l[i]), self.idx_char),
                                                  vec2text(index2vec(max_idx_p[i]), self.idx_char)))

    def generate(self, epsilon=0.02, alpha=2 / 255, iteration=1):
        make_folder(self.output_dir)
        # 无目标攻击。
        images, labels = self.cus_data_loader(0, len(self.test_data), self.test_data)

        def pred_acc(input_x, real_y):
            input_x = Variable(cuda(input_x, self.cuda))
            real_y = Variable(cuda(real_y, self.cuda))
            output = self.net(input_x)
            predict = output.view([-1, self.captcha_len, len(self.captcha_char_set)])
            max_idx_p = predict.max(2)[1]

            real = real_y.view([-1, self.captcha_len, len(self.captcha_char_set)])
            max_idx_l = real.max(2)[1]
            accuracy = max_idx_p.eq(max_idx_l).float().mean()
            cost = self.loss_func(output, real_y)
            return accuracy, cost

        accuracy, cost = pred_acc(images, labels)  # 生成之前先做检测
        if self.fun == 'fgsm':
            x_adv = self.FGSM(images, labels, epsilon, alpha, iteration)
        elif self.fun == 'deepfool':
            x_adv = self.DF(images, epsilon)
        else:
            raise RuntimeError("generate fun input error")
        accuracy_adv, cost_adv = pred_acc(x_adv, labels)  # 再做检测
        save_perturbed_image(x_adv, os.path.join(self.output_dir, self.fun), self.captcha_w, self.captcha_h)
        print('[BEFORE] accuracy: %.4f' % accuracy, '| cost : %.4f' % cost)
        print('[AFTER] accuracy: %.4f' % accuracy_adv, '| cost : %.4f' % cost_adv)

    # 对抗样本生成算法
    def FGSM(self, x, y_true, eps=0.03, alpha=2 / 255, iteration=1):
        y_target = None
        x = Variable(cuda(x, self.cuda), requires_grad=True)
        y_true = Variable(cuda(y_true, self.cuda), requires_grad=False)
        targeted = False
        # 开始扰动
        if iteration == 1:
            if targeted:
                x_adv, h_adv, h = self.attack.fgsm(x, y_target, True, eps)
            else:
                x_adv, h_adv, h = self.attack.fgsm(x, y_true, False, eps)
        else:
            if targeted:
                x_adv, h_adv, h = self.attack.i_fgsm(x, y_target, True, eps, alpha, iteration)
            else:
                x_adv, h_adv, h = self.attack.i_fgsm(x, y_true, False, eps, alpha, iteration)

        return x_adv.data

    def DF(self, x, eps=0.03):
        images = list()
        for i in range(len(x)):
            r, loop_i, label_orig, label_pert, pert_image = \
                self.attack.deepfool(x[i], self.net, num_classes=self.dim, overshoot=eps)
            images.append(pert_image)
        return torch.stack(images, 0).float().squeeze(1)
