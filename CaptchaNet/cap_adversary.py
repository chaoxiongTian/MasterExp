"""adversary.py"""

import torch
from torch.autograd import Variable
import numpy as np
import copy
from torch.autograd.gradcheck import zero_gradients


def where(cond, x, y):
    """
    code from :
        https://discuss.pytorch.org/t/how-can-i-do-the-operation-the-same-as-np-where/1329/8
    """
    cond = cond.float()
    return (cond * x) + ((1 - cond) * y)


class Attack(object):
    def __init__(self, net, criterion):
        self.net = net
        self.criterion = criterion

    def fgsm(self, x, y, targeted=False, eps=0.03, x_val_min=-1, x_val_max=1):
        print('i_fgsm', eps, targeted)
        x_adv = Variable(x.data, requires_grad=True)
        h_adv = self.net(x_adv)
        if targeted:
            cost = self.criterion(h_adv, y)
        else:
            cost = -self.criterion(h_adv, y)

        self.net.zero_grad()
        if x_adv.grad is not None:
            x_adv.grad.data.fill_(0)
        cost.backward()

        x_adv.grad.sign_()
        x_adv = x_adv - eps * x_adv.grad
        x_adv = x_adv.clamp(x_val_min, x_val_max)

        h = self.net(x)
        h_adv = self.net(x_adv)

        return x_adv, h_adv, h

    def i_fgsm(self, x, y, targeted=False, eps=0.03, alpha=1, iteration=1, x_val_min=-1, x_val_max=1):
        print('i_fgsm', eps, alpha, iteration, targeted)
        x_adv = Variable(x.data, requires_grad=True)
        for i in range(iteration):
            h_adv = self.net(x_adv)
            if targeted:
                cost = self.criterion(h_adv, y)
            else:
                cost = -self.criterion(h_adv, y)

            self.net.zero_grad()
            if x_adv.grad is not None:
                x_adv.grad.data.fill_(0)
            cost.backward()

            x_adv.grad.sign_()
            x_adv = x_adv - alpha * x_adv.grad
            x_adv = where(x_adv > x + eps, x + eps, x_adv)
            x_adv = where(x_adv < x - eps, x - eps, x_adv)
            x_adv = x_adv.clamp(x_val_min, x_val_max)
            x_adv = Variable(x_adv.data, requires_grad=True)

        h = self.net(x)
        h_adv = self.net(x_adv)

        return x_adv, h_adv, h

    def deepfool(self, image, net, num_classes=2, overshoot=0.02, max_iter=50):
        """
           :param image: Image of size HxWx3
           :param net: network (input: images, output: values of activation **BEFORE** softmax).
           :param num_classes: num_classes (limits the number of classes to test against, by default = 10)
           :param overshoot: used as a termination criterion to prevent vanishing updates (default = 0.02).
           :param max_iter: maximum number of iterations for deepfool (default = 50)
           :return: minimal perturbation that fools the classifier, number of iterations that it required, new estimated_label and perturbed image
        """

        if torch.cuda.is_available():
            # print("Using GPU")
            image = image.cuda()
            net = net.cuda()
        else:
            pass
            # print("Using CPU")

        # print(image.shape)  # torch.Size([3, 224, 224])
        # print(Variable(image[None, :, :, :]).shape)  # torch.Size([1, 3, 224, 224])

        f_image = net.forward(Variable(image[None, :, :, :], requires_grad=True)).data.cpu().numpy().flatten()
        # print(type(f_image))  # <class 'numpy.ndarray'>
        # print('f_image', f_image.shape)  # (1000,)
        # print(f_image)
        I = (np.array(f_image)).flatten().argsort()[::-1]
        # print('I', I.shape)
        # print(I)
        I = I[0:num_classes]
        label = I[0]

        input_shape = image.cpu().numpy().shape
        pert_image = copy.deepcopy(image)
        w = np.zeros(input_shape)
        r_tot = np.zeros(input_shape)

        loop_i = 0

        x = Variable(pert_image[None, :], requires_grad=True)
        fs = net.forward(x)
        fs_list = [fs[0, I[k]] for k in range(num_classes)]
        k_i = label

        while k_i == label and loop_i < max_iter:

            pert = np.inf
            fs[0, I[0]].backward(retain_graph=True)
            grad_orig = x.grad.data.cpu().numpy().copy()

            for k in range(1, num_classes):
                zero_gradients(x)

                fs[0, I[k]].backward(retain_graph=True)
                cur_grad = x.grad.data.cpu().numpy().copy()

                # set new w_k and new f_k
                w_k = cur_grad - grad_orig
                f_k = (fs[0, I[k]] - fs[0, I[0]]).data.cpu().numpy()

                pert_k = abs(f_k) / np.linalg.norm(w_k.flatten())

                # determine which w_k to use
                if pert_k < pert:
                    pert = pert_k
                    w = w_k

            # compute r_i and r_tot
            # Added 1e-4 for numerical stability
            r_i = (pert + 1e-4) * w / np.linalg.norm(w)
            r_tot = np.float32(r_tot + r_i)

            if torch.cuda.is_available():
                pert_image = image + (1 + overshoot) * torch.from_numpy().cuda()
            else:
                pert_image = image + (1 + overshoot) * torch.from_numpy(r_tot)

            x = Variable(pert_image, requires_grad=True)
            fs = net.forward(x)
            k_i = np.argmax(fs.data.cpu().numpy().flatten())

            loop_i += 1

        r_tot = (1 + overshoot) * r_tot

        return r_tot, loop_i, label, k_i, pert_image
