# -*- coding: utf-8 -*-
# @Time    : 18-12-20 上午9:53
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : load_mnist.py
# @Software: PyCharm

import torch
import torchvision
import torch.nn.functional as F


def restore_net():
    net = torch.load('net.pkl')
    print("Net info:")
    print(net)
    print("Net info end \n")
    return net


net = restore_net()
test_data = torchvision.datasets.MNIST(root='./mnist/', train=False)
test_x = test_data.test_data.unsqueeze(dim=1).float()[:10] / 255.
test_y = test_data.test_labels[:10]

output = net(test_x)[0]
pred_y = output.max(1)[1]

accuracy = pred_y.eq(test_y).float().mean()
cost = F.cross_entropy(output, test_y)
print('预测结果', pred_y.data.numpy())
print('真实结果', test_y.data.numpy())
print(accuracy.item())
print(cost.item())
