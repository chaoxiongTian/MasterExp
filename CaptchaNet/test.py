# -*- coding: utf-8 -*-
# @Time    : 19-1-22 上午11:13
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : test.py
# @Software: PyCharm
import torch
import time
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch import optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision.transforms import ToPILImage

show = ToPILImage()
import numpy as np
import matplotlib.pyplot as plt

#
batchSize = 128

##load data
transform = transforms.Compose(
    [transforms.Resize(96), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.MNIST(root='./mnist', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batchSize, shuffle=True, num_workers=0)

testset = torchvision.datasets.MNIST(root='./mnist', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batchSize, shuffle=False, num_workers=0)

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


def imshow(img):
    img = img / 2 + 0.5
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))


####network
def conv_relu(in_channels, out_channels, kernel, stride=1, padding=0):
    layer = nn.Sequential(
        nn.Conv2d(in_channels, out_channels, kernel, stride, padding),
        nn.BatchNorm2d(out_channels, eps=1e-3),
        nn.ReLU(True))
    return layer


class Inception(nn.Module):
    def __init__(self, in_channel, c1, c2, c3, c4):
        super(Inception, self).__init__()
        self.norm1_1 = nn.BatchNorm2d(in_channel, eps=1e-3)
        self.p1_1 = nn.Conv2d(in_channels=in_channel, out_channels=c1, kernel_size=1)
        self.norm2_1 = nn.BatchNorm2d(in_channel, eps=1e-3)
        self.p2_1 = nn.Conv2d(in_channels=in_channel, out_channels=c2[0], kernel_size=1)
        self.norm2_2 = nn.BatchNorm2d(c2[0], eps=1e-3)
        self.p2_2 = nn.Conv2d(in_channels=c2[0], out_channels=c2[1], kernel_size=3, padding=1)
        self.norm3_1 = nn.BatchNorm2d(in_channel, eps=1e-3)
        self.p3_1 = nn.Conv2d(in_channels=in_channel, out_channels=c3[0], kernel_size=1)
        self.norm3_2 = nn.BatchNorm2d(c3[0], eps=1e-3)
        self.p3_2 = nn.Conv2d(in_channels=c3[0], out_channels=c3[1], kernel_size=5, padding=2)
        self.p4_1 = nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        self.norm4_2 = nn.BatchNorm2d(in_channel, eps=1e-3)
        self.p4_2 = nn.Conv2d(in_channels=in_channel, out_channels=c4, kernel_size=1)

    def forward(self, x):
        p1 = self.p1_1(F.relu(self.norm1_1(x)))
        p2 = self.p2_2(F.relu(self.norm2_2(self.p2_1(F.relu(self.norm2_1(x))))))
        p3 = self.p3_2(F.relu(self.norm3_2(self.p3_1(F.relu(self.norm3_1(x))))))
        p4 = self.p4_2(F.relu(self.norm4_2(self.p4_1(x))))
        return torch.cat((p1, p2, p3, p4), dim=1)


# Test Inception block
# test_net = Inception(3, 64, (48, 64), (64, 96), 32)
# test_x = Variable(torch.zeros(1, 3, 96, 96))
# print('input shape: {} x {} x {}'.format(test_x.shape[1], test_x.shape[2], test_x.shape[3]))
# test_y = test_net(test_x)
# print('output shape: {} x {} x {}'.format(test_y.shape[1], test_y.shape[2], test_y.shape[3]))


class GoogleNet(nn.Module):
    def __init__(self, in_channel, num_classes):
        super(GoogleNet, self).__init__()
        layers = []
        layers += [nn.Conv2d(in_channels=in_channel, out_channels=64, kernel_size=7, stride=2, padding=3),
                   nn.ReLU(),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1)]
        layers += [nn.Conv2d(in_channels=64, out_channels=64, kernel_size=1),
                   nn.Conv2d(in_channels=64, out_channels=192, kernel_size=3, padding=1),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1)]
        layers += [Inception(192, 64, (96, 128), (16, 32), 32),
                   Inception(256, 128, (128, 192), (32, 96), 64),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1)]
        layers += [Inception(480, 192, (96, 208), (16, 48), 64),
                   Inception(512, 160, (112, 224), (24, 64), 64),
                   Inception(512, 128, (128, 256), (24, 64), 64),
                   Inception(512, 112, (144, 288), (32, 64), 64),
                   Inception(528, 256, (160, 320), (32, 128), 128),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1)]
        layers += [Inception(832, 256, (160, 320), (32, 128), 128),
                   Inception(832, 384, (192, 384), (48, 128), 128),
                   nn.AvgPool2d(kernel_size=2)]
        self.net = nn.Sequential(*layers)
        self.dense = nn.Linear(1024, num_classes)

    def forward(self, x):
        x = self.net(x)
        x = x.view(-1, 1024 * 1 * 1)
        x = self.dense(x)
        return x


# Test GoogleNet
# test_net = GoogleNet(3, 10)
# test_x = Variable(torch.zeros(1, 3, 96, 96))
# test_y = test_net(test_x)
# print('output: {}'.format(test_y.shape))


net = GoogleNet(1, 10).cuda()
print(net)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.1, momentum=0.9)

# train
print("training begin")
for epoch in range(3):
    start = time.time()
    running_loss = 0
    for i, data in enumerate(trainloader, 0):
        # print (inputs,labels)
        image, label = data

        image = image.cuda()
        label = label.cuda()
        image = Variable(image)
        label = Variable(label)

        # imshow(torchvision.utils.make_grid(image))
        # plt.show()
        # print (label)
        optimizer.zero_grad()

        outputs = net(image)
        # print (outputs)
        loss = criterion(outputs, label)

        loss.backward()
        optimizer.step()

        running_loss += loss.data

        if i % 100 == 99:
            end = time.time()
            print('[epoch %d,imgs %5d] loss: %.7f  time: %0.3f s' % (
                epoch + 1, (i + 1) * batchSize, running_loss / 100, (end - start)))
            start = time.time()
            running_loss = 0
print("finish training")

# test
net.eval()
correct = 0
total = 0
for data in testloader:
    images, labels = data
    images = images.cuda()
    labels = labels.cuda()
    outputs = net(Variable(images))
    _, predicted = torch.max(outputs, 1)
    total += labels.size(0)
    correct += (predicted == labels).sum()
print('Accuracy of the network on the %d test images: %d %%' % (total, 100 * correct / total))
