# -*- coding: utf-8 -*-
# @Time    : 18-12-25 下午8:39
# @Author  : MaxCentaur
# @Email   : ambition_x@163.com
# @File    : ceshi_2.py
# @Software: PyCharm

from PIL import Image
from out_utils import *
from torchvision import datasets
import torch.utils.data as Data


# # 自定义 loader
# def cus_loader(path):
#     return Image.open(path).convert('L')
#
#
# transform = transforms.Compose([transforms.ToTensor()])
# train_data = datasets.ImageFolder(root=os.path.join(os.path.dirname(__file__), 'data_sets', 'd_mnist', 'train'),
#                                   transform=transform,
#                                   loader=cus_loader)
# test_data = datasets.ImageFolder(root=os.path.join(os.path.dirname(__file__), 'data_sets', 'd_mnist', 'test'),
#                                  transform=transform,
#                                  loader=cus_loader)
# train_loader = Data.DataLoader(train_data, batch_size=64, shuffle=True)
#
# print(test_data[0][0].size())

# # 灰度图片转tensor  ToPILImage tensor转PIL image
# data = Image.open('/home/tianchaoxiong/LinuxData/code/pythonpro/MasterExp/IdentifiNetwork/data_sets/d_mnist/test/0/0.jpg')
# # transforms 中的 ToTensor()函数可以直接讲numpy对象或者PIL图像转为tensor
# # img_tensor = transforms.ToTensor()(data.convert('RGB'))  # 转换成tensor
# # torch.Size([3, 28, 28])
# img_tensor = transforms.ToTensor()(data)  # 转换成tensor
# # torch.Size([1, 28, 28])
# print(img_tensor.size())

# # 函数名作为参数调用
# def add(a,b):
#     return a+b+1
# def def_add(a,b):
#     return a+b
# def addd(a,b,fun=def_add):
#     return fun(a,b)
# print(addd(1,2,fun=def_add))
# print(addd(1,2,fun=add))

