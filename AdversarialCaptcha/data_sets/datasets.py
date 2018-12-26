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
    data_set_folder = args.data_set_folder
    batch_size = args.batch_size
    transform = transforms.Compose([transforms.ToTensor()])
    loader = dict()
    if 'MNIST' in name:
        root = os.path.join(data_set_folder, 'MNIST')
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
        return loader
    elif 'd_mnist' in name:
        train_data_folder = os.path.join(data_set_folder, str(name), 'train')
        test_data_folder = os.path.join(data_set_folder, str(name), 'test')
        train_data = datasets.ImageFolder(root=train_data_folder, transform=transform, loader=cus_loader)
        test_data = datasets.ImageFolder(root=test_data_folder, transform=transform, loader=cus_loader)
        train_loader = Data.DataLoader(train_data, batch_size=batch_size, shuffle=True)
        test_loader = Data.DataLoader(test_data, batch_size=batch_size, shuffle=False)
        loader['train'] = train_loader
        loader['test'] = test_loader
        return loader
    else:
        raise UnknownDatasetError()


if __name__ == '__main__':
    import argparse

    os.chdir('..')

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_set_folder', type=str, default='data_folder')
    parser.add_argument('--dset_dir', type=str, default='datasets')
    parser.add_argument('--batch_size', type=int, default=64)
    args = parser.parse_args()

    data_loader = return_data(args)
    data_loader_iter = data_loader['test']
    for batch_idx, (images, labels) in enumerate(data_loader_iter):
        print(images.size())
        print(labels.size())
        if batch_idx == 1:
            break
