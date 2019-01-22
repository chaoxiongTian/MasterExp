# -*- coding: utf-8 -*-
# @Time    : 18-12-27 下午9:39
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : core_net.py
# @Software: PyCharm

import torch
import torch.nn as nn


class SimpleCnn256(nn.Module):
    def __init__(self, channel=1, y_dim=10, keep_prob=0.75):
        super(SimpleCnn256, self).__init__()
        self.conv1 = nn.Sequential(  # input shape
            nn.Conv2d(
                in_channels=channel,  # input height
                out_channels=16,  # n_filters
                kernel_size=5,  # filter size
                stride=1,  # filter movement/step
                padding=2,
                # if want same width and length of this image after Conv2d, padding=(kernel_size-1)/2 if stride=1
            ),  # output shape
            nn.ReLU(),  # activation
            nn.MaxPool2d(kernel_size=2),  # choose max value in 2x2 area, output shape (16, 14, 14)
        )
        self.conv2 = nn.Sequential(  # input shape
            nn.Conv2d(16, 32, 5, 1, 2),  # output shape
            nn.ReLU(),  # activation
            nn.MaxPool2d(2),  # output shape
        )
        self.out = nn.Linear(32 * 64 * 64, y_dim)  # fully connected layer, output 10 classes

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)  # flatten the output of conv2 to (batch_size, 32 * 7 * 7)
        output = self.out(x)
        return output  # return x for visualization

    def weight_init(self, _type='kaiming'):
        if _type == 'kaiming':
            for ms in self._modules:
                kaiming_init(self._modules[ms].parameters())


class SimpleCnn3(nn.Module):
    def __init__(self, channel=1, y_dim=10, keep_prob=0.75):
        super(SimpleCnn3, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(channel, 16, 5, 1, 2),
            nn.ReLU(), nn.MaxPool2d(kernel_size=2),
            nn.Dropout(keep_prob),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, 5, 1, 2),
            nn.ReLU(), nn.MaxPool2d(2),
            nn.Dropout(keep_prob),
        )
        self.out = nn.Linear(32 * 7 * 7, y_dim)

    def forward(self, x):  # torch.Size([64, 1, 28, 28])
        x = self.conv1(x)  # torch.Size([64, 16, 14, 14])
        x = self.conv2(x)  # torch.Size([64, 32, 7, 7])
        x = x.view(x.size(0), -1)  # torch.Size([64, 1568])
        output = self.out(x)  # torch.Size([64, 10])
        return output  # return x for visualization

    def weight_init(self, _type='kaiming'):
        if _type == 'kaiming':
            for ms in self._modules:
                kaiming_init(self._modules[ms].parameters())


class SimpleCnn5(nn.Module):
    def __init__(self, channel=1, y_dim=10, keep_prob=0.5):
        super(SimpleCnn5, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(channel, 32, 3, 1, 1),
            nn.ReLU(), nn.MaxPool2d(kernel_size=2),
            nn.Dropout(keep_prob),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, 3, 1, 1),
            nn.ReLU(), nn.MaxPool2d(2),
            nn.Dropout(keep_prob),
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 64, 3, 1, 1),
            nn.ReLU(), nn.MaxPool2d(2),
            nn.Dropout(keep_prob),
        )
        self.fully = nn.Linear(64 * 3 * 3, 1024)
        self.out = nn.Linear(1024, y_dim)

    def forward(self, x):  # torch.Size([64, 1, 28, 28])
        x = self.conv1(x)  # torch.Size([64, 32, 14, 14])
        x = self.conv2(x)  # torch.Size([64, 64, 7, 7])
        x = self.conv3(x)  # torch.Size([64, 64, 3, 3])
        x = x.view(x.size(0), -1)  # torch.Size([64, 64*3*3])
        x = self.fully(x)  # torch.Size([64, 1024])
        output = self.out(x)  # torch.Size([64, y_dim])
        return output

    def weight_init(self, _type='kaiming'):
        if _type == 'kaiming':
            for ms in self._modules:
                kaiming_init(self._modules[ms].parameters())


class LeNet5(nn.Module):  # 输入为 32*32 不过已经修改为 28*28
    def __init__(self, channel=1, y_dim=10, keep_prob=0.5):
        super(LeNet5, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(channel, 6, 5, padding=2),
            nn.ReLU(), nn.MaxPool2d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(6, 16, 5, 1, 0),
            nn.ReLU(), nn.MaxPool2d(2),
        )
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.out = nn.Linear(84, y_dim)

    def forward(self, x):  # torch.Size([64, 1, 32, 32])
        # print('input: ', x.shape)
        x = self.conv1(x)  # torch.Size([64, 6, 14, 14])
        # print('conv1: ', x.shape)
        x = self.conv2(x)  # torch.Size([64, 16, 5, 5])
        # print('conv2: ', x.shape)
        x = x.view(x.size(0), -1)  # torch.Size([64, 16*5*5])
        # print('view: ', x.shape)
        x = self.fc1(x)  # torch.Size([64, 120])
        # print('fc1: ', x.shape)
        x = self.fc2(x)  # torch.Size([64, 84])
        # print('fc2: ', x.shape)
        output = self.out(x)  # torch.Size([64, y_dim])
        # print('output: ', x.shape)
        return output

    def weight_init(self, _type='kaiming'):
        if _type == 'kaiming':
            for ms in self._modules:
                kaiming_init(self._modules[ms].parameters())


class AlexNet(nn.Module):  # 输入为227*227
    def __init__(self, channel=1, y_dim=10, keep_prob=0.5):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(channel, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, y_dim),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), 256 * 6 * 6)
        x = self.classifier(x)
        return x

    def weight_init(self, _type='kaiming'):
        if _type == 'kaiming':
            for ms in self._modules:
                kaiming_init(self._modules[ms].parameters())


class Inception(nn.Module):
    def __init__(self, in_planes, n1x1, n3x3red, n3x3, n5x5red, n5x5, pool_planes):
        super(Inception, self).__init__()
        # 1x1 conv branch
        self.b1 = nn.Sequential(
            nn.Conv2d(in_planes, n1x1, kernel_size=1),
            nn.BatchNorm2d(n1x1),
            nn.ReLU(inplace=True),
        )

        # 1x1 conv -> 3x3 conv branch
        self.b2 = nn.Sequential(
            nn.Conv2d(in_planes, n3x3red, kernel_size=1),
            nn.BatchNorm2d(n3x3red),
            nn.ReLU(inplace=True),
            nn.Conv2d(n3x3red, n3x3, kernel_size=3, padding=1),
            nn.BatchNorm2d(n3x3),
            nn.ReLU(inplace=True),
        )

        # 1x1 conv -> 5x5 conv branch
        self.b3 = nn.Sequential(
            nn.Conv2d(in_planes, n5x5red, kernel_size=1),
            nn.BatchNorm2d(n5x5red),
            nn.ReLU(inplace=True),
            nn.Conv2d(n5x5red, n5x5, kernel_size=3, padding=1),
            nn.BatchNorm2d(n5x5),
            nn.ReLU(inplace=True),
            nn.Conv2d(n5x5, n5x5, kernel_size=3, padding=1),
            nn.BatchNorm2d(n5x5),
            nn.ReLU(inplace=True),
        )

        # 3x3 pool -> 1x1 conv branch
        self.b4 = nn.Sequential(
            nn.MaxPool2d(3, stride=1, padding=1),
            nn.Conv2d(in_planes, pool_planes, kernel_size=1),
            nn.BatchNorm2d(pool_planes),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        y1 = self.b1(x)
        y2 = self.b2(x)
        y3 = self.b3(x)
        y4 = self.b4(x)
        return torch.cat([y1, y2, y3, y4], 1)


class GoogLeNet(nn.Module):  # 输入为96×96
    def __init__(self, channel=1, y_dim=10, keep_prob=0.5):
        super(GoogLeNet, self).__init__()
        self.pre_layers = nn.Sequential(
            nn.Conv2d(channel, 192, kernel_size=3, padding=1),
            nn.BatchNorm2d(192),
            nn.ReLU(inplace=True),
        )

        self.a3 = Inception(192, 64, 96, 128, 16, 32, 32)
        self.b3 = Inception(256, 128, 128, 192, 32, 96, 64)

        self.maxpool = nn.MaxPool2d(3, stride=2, padding=1)

        self.a4 = Inception(480, 192, 96, 208, 16, 48, 64)
        self.b4 = Inception(512, 160, 112, 224, 24, 64, 64)
        self.c4 = Inception(512, 128, 128, 256, 24, 64, 64)
        self.d4 = Inception(512, 112, 144, 288, 32, 64, 64)
        self.e4 = Inception(528, 256, 160, 320, 32, 128, 128)

        self.a5 = Inception(832, 256, 160, 320, 32, 128, 128)
        self.b5 = Inception(832, 384, 192, 384, 48, 128, 128)

        self.avgpool = nn.AvgPool2d(kernel_size=8, stride=1)
        self.linear = nn.Linear(1024, y_dim)

    def forward(self, inputs):
        network = self.pre_layers(inputs)
        network = self.a3(network)
        network = self.b3(network)
        network = self.maxpool(network)
        network = self.a4(network)
        network = self.b4(network)
        network = self.c4(network)
        network = self.d4(network)
        network = self.e4(network)
        network = self.maxpool(network)
        network = self.a5(network)
        network = self.b5(network)
        network = self.avgpool(network)
        network = network.view(network.size(0), -1)
        out = self.linear(network)
        return out, network

    def weight_init(self, _type='kaiming'):
        if _type == 'kaiming':
            for ms in self._modules:
                kaiming_init(self._modules[ms].parameters())

# 反向传导的时候还是用kaiming优化
def kaiming_init(ms):
    for m in ms:
        if isinstance(m, (nn.Linear, nn.Conv2d)):
            nn.init.kaiming_uniform(m.weight, a=0, mode='fan_in')
            if m.bias.data:
                m.bias.data.zero_()
        if isinstance(m, (nn.BatchNorm2d, nn.BatchNorm1d)):
            m.weight.data.fill_(1)
            if m.bias.data:
                m.bias.data.zero_()
