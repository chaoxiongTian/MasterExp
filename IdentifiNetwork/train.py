# -*- coding: utf-8 -*-
# @Time    : 18-12-19 下午10:34
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : mnist.py
# @Software: PyCharm

import torch
import torch.nn as nn
from IdentifiNetwork.Net import CNN
from torchvision import datasets
from out_utils import *
import torch.utils.data as Data

torch.manual_seed(1)  # reproducible

# 超参数
EPOCH = 20
BATCH_SIZE = 50
LR = 0.001

transform = transforms.Compose([transforms.ToTensor(), transforms.Gray()])
train_data = datasets.ImageFolder(root=os.path.join(data_folder, 'train'), transform=transform)
test_data = datasets.ImageFolder(root=os.path.join(data_folder, 'test'), transform=transform)
train_loader = Data.DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)


def combine_tensor(data):
    num = len(data)
    sequence_x = [data[i][0] for i in range(num)]
    sequence_y = [torch.LongTensor([test_data[i][1]]) for i in range(num)]
    return torch.stack(sequence_x, 0), torch.stack(sequence_y, 0).squeeze()


test_x, test_y = combine_tensor(test_data)

cnn = CNN()
print(cnn)  # net architecture

optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)
loss_func = nn.CrossEntropyLoss()

for epoch in range(EPOCH):
    for step, (b_x, b_y) in enumerate(train_loader):
        output = cnn(b_x)[0]
        loss = loss_func(output, b_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # 50个batch做一个测试
        if step % 50 == 0:
            test_output, last_layer = cnn(test_x)
            pred_y = test_output.max(1)[1]
            accuracy = pred_y.eq(test_y).float().mean()
            print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.numpy(), '| test accuracy: %.2f' % accuracy)
