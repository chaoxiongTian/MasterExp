# -*- coding: utf-8 -*-
# @Time    : 18-12-27 下午9:39
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : core_net.py
# @Software: PyCharm

import torch.nn as nn


class SimpleCnn256(nn.Module):
    def __init__(self, channel=1, y_dim=10):
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
    def __init__(self, channel=1, y_dim=10):
        super(SimpleCnn3, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(channel, 16, 5, 1, 2),
            nn.ReLU(), nn.MaxPool2d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, 5, 1, 2),
            nn.ReLU(), nn.MaxPool2d(2),
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
    def __init__(self, channel=1, y_dim=10):
        super(SimpleCnn5, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(channel, 32, 3, 1, 1),
            nn.ReLU(), nn.MaxPool2d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, 3, 1, 1),
            nn.ReLU(), nn.MaxPool2d(2),
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 64, 3, 1, 1),
            nn.ReLU(), nn.MaxPool2d(2),
        )
        self.fully = nn.Linear(64 * 3 * 3, 1024)
        self.out = nn.Linear(1024, y_dim)

    def forward(self, x):  # torch.Size([64, 1, 28, 28])
        # print('1', x.shape)
        x = self.conv1(x)  # torch.Size([64, 32, 14, 14])
        # print('2', x.shape)
        x = self.conv2(x)  # torch.Size([64, 64, 7, 7])
        # print('3', x.shape)
        x = self.conv3(x)  # torch.Size([64, 64, 3, 3])
        # print('4', x.shape)
        x = x.view(x.size(0), -1)  # torch.Size([64, 64*3*3])
        # print('5', x.shape)
        x = self.fully(x)  # torch.Size([64, 1024])
        # print('6', x.shape)
        output = self.out(x)  # torch.Size([64, y_dim])
        # print('7', output.shape)
        return output

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
