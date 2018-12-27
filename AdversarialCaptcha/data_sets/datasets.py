"""datasets.py"""
import os

from PIL import Image
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
from torchvision import datasets
import torch.utils.data as Data


class UnknownDatasetError(Exception):
    def __str__(self):
        return "unknown datasets error"


# datasets.ImageFolder中自定义的class loader
def cus_loader(path):
    return Image.open(path).convert('L')


def return_data(args):
    name = args.model_name
    data_set = args.data_set_folder
    batch_size = args.batch_size
    transform = transforms.Compose([transforms.ToTensor()])
    loader = dict()
    if 'MNIST' in name:
        root = os.path.join(data_set, 'MNIST')
        train_kwargs = {'root': root, 'train': True, 'transform': transform, 'download': True}
        test_kwargs = {'root': root, 'train': False, 'transform': transform, 'download': False}
        dset = MNIST
        train_data = dset(**train_kwargs)
        train_loader = DataLoader(train_data,
                                  batch_size=batch_size,
                                  shuffle=True,
                                  num_workers=1,
                                  pin_memory=True,
                                  drop_last=True)

        test_data = dset(**test_kwargs)
        test_loader = DataLoader(test_data,
                                 batch_size=batch_size,
                                 shuffle=False,
                                 num_workers=1,
                                 pin_memory=True,
                                 drop_last=False)

        loader['train'] = train_loader
        loader['test'] = test_loader
        return loader, test_data
    else:
        train_folder = os.path.join(os.path.dirname(__file__), name, 'train')
        test_folder = os.path.join(os.path.dirname(__file__), name, 'test')
        train_data = datasets.ImageFolder(root=train_folder, transform=transform, loader=cus_loader)
        test_data = datasets.ImageFolder(root=test_folder, transform=transform, loader=cus_loader)
        train_loader = Data.DataLoader(train_data, batch_size=batch_size, shuffle=True)
        test_loader = Data.DataLoader(test_data, batch_size=batch_size, shuffle=False)
        loader['train'] = train_loader
        loader['test'] = test_loader
        return loader, test_data


if __name__ == '__main__':
    import argparse

    os.chdir('..')

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_set_folder', type=str, default='data_sets')
    parser.add_argument('--model_name', type=str, default='d_mnist')
    parser.add_argument('--batch_size', type=int, default=64)
    args = parser.parse_args()

    data_loader, test_data = return_data(args)
    test_data_loader = data_loader['test']
    print(type(test_data[0][0]))
    print(type(test_data[0][1]))

