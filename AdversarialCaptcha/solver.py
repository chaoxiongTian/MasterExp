"""solver.py"""

import torch.optim as optim
import torch.nn.functional as F
from torchvision.utils import save_image

import torch.utils.data as Data

from models.net import CNN
from data_sets.datasets import return_data
from adversarial_utils import *
from adversary import Attack
from out_utils import *


class Solver(object):
    def __init__(self, args):
        self.args = args

        # Basic
        self.cuda = (args.cuda and torch.cuda.is_available())
        self.epoch = args.epoch
        self.batch_size = args.batch_size
        self.lr = args.lr
        self.model_name = args.model_name
        self.data_type = args.data_type
        self.data_set_folder = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                             args.data_set_folder,
                                                             args.model_name))
        self.y_dim = return_y_dim(self.data_set_folder)  # 分类的类别数
        self.target = args.target  # 目标生成的时候使用
        self.data_loader, self.test_data = return_data(args)  # 返回data_loader

        self.global_epoch = 0
        self.global_iter = 0
        self.print_ = not args.silent

        # 标签和类别 和类别到标签的两个对应字典
        test_data_folder = os.path.join(self.data_set_folder, 'train')
        _, self.class_to_idx, self.idx_to_class = find_classes(test_data_folder)

        self.tensorboard = args.tensorboard
        self.visdom = args.visdom

        # 模型路径
        self.ckpt_dir = os.path.join(os.path.dirname(__file__), args.ckpt_dir, args.model_name)
        if not os.path.exists(self.ckpt_dir):
            make_folder(self.ckpt_dir)

        # 输出路径
        # self.output_dir = os.path.join(os.path.dirname(__file__), args.output_dir, args.model_name)
        # if not os.path.exists(self.output_dir):
        #     make_folder(self.output_dir)

        # 可视化工具
        self.visualization_init(args)

        # Histories 创建字典
        self.history = dict()
        self.history['acc'] = 0.
        self.history['epoch'] = 0
        self.history['iter'] = 0

        # Models & Optimizers
        self.model_init(args)
        self.load_ckpt = args.load_ckpt
        # 没有指明调用用的模型 则调用 best_acc.tar
        if self.load_ckpt != '':
            self.load_checkpoint(self.load_ckpt)

        # Adversarial Perturbation Generator
        # criterion = cuda(torch.nn.CrossEntropyLoss(), self.cuda)
        criterion = F.cross_entropy
        self.attack = Attack(self.net, criterion=criterion)

    def visualization_init(self, args):
        # Visdom
        if self.visdom:
            from utils.visdom_utils import VisFunc
            self.port = args.visdom_port
            self.vf = VisFunc(enval=self.model_name, port=self.port)
        if self.visdom:
            from utils.visdom_utils import VisFunc
            self.port = args.visdom_port
            self.vf = VisFunc(enval=self.model_name, port=self.port)

        # TensorboardX
        if self.tensorboard:
            from tensorboardX import SummaryWriter
            self.summary_dir = Path(args.summary_dir).joinpath(args.model_name)
            if not self.summary_dir.exists():
                self.summary_dir.mkdir(parents=True, exist_ok=True)

            self.tf = SummaryWriter(log_dir=str(self.summary_dir))
            self.tf.add_text(tag='argument', text_string=str(args), global_step=self.global_epoch)

    # 网络参数的初始化过程。
    def model_init(self, args):
        # Network 初始化网络 初始化优化器 初始化参数（凯明）
        self.net = cuda(CNN(y_dim=self.y_dim), self.cuda)
        self.net.weight_init(_type='kaiming')  # 对net中的参数进行初始化
        print(self.net)
        # Optimizers 初始化优化器
        self.optim = optim.Adam([{'params': self.net.parameters(), 'lr': self.lr}],
                                betas=(0.5, 0.999))

    # 训练
    def train(self):
        print(self.model_name)
        for epoch_idx in range(self.epoch):
            self.global_epoch += 1
            for batch_idx, (images, labels) in enumerate(self.data_loader['train']):
                self.global_iter += 1
                x = Variable(cuda(images, self.cuda))
                y = Variable(cuda(labels, self.cuda))
                output = self.net(x)
                prediction = output.max(1)[1]
                # 求准确率
                accuracy = prediction.eq(y).float().mean().item()
                cost = F.cross_entropy(output, y)

                self.optim.zero_grad()
                cost.backward()
                self.optim.step()

                if batch_idx % 4 == 0:
                    print('Epoch:', epoch_idx,
                          '| iter:', batch_idx * self.batch_size,
                          '| train loss: %.4f' % cost.item(),
                          '| train accuracy: %.3f' % accuracy)

                    if self.tensorboard:
                        self.tf.add_scalars(main_tag='performance/acc',
                                            tag_scalar_dict={'train': accuracy},
                                            global_step=self.global_iter)
                        self.tf.add_scalars(main_tag='performance/error',
                                            tag_scalar_dict={'train': 1 - accuracy},
                                            global_step=self.global_iter)
                        self.tf.add_scalars(main_tag='performance/cost',
                                            tag_scalar_dict={'train': cost.data[0]},
                                            global_step=self.global_iter)

            self.test()

        if self.tensorboard:
            self.tf.add_scalars(main_tag='performance/best/acc',
                                tag_scalar_dict={'test': self.history['acc']},
                                global_step=self.history['iter'])
        print(" [*] Training Finished!")

    # 批量测试（使用loader）
    def test(self):
        correct = 0.
        cost = 0.
        total = 0.
        for batch_idx, (images, labels) in enumerate(self.data_loader['test']):
            x = Variable(cuda(images, self.cuda))
            y = Variable(cuda(labels, self.cuda))

            output = self.net(x)
            prediction = output.max(1)[1]

            correct += prediction.eq(y).float().sum().item()
            cost += F.cross_entropy(output, y, reduction='mean').item()
            total += x.size(0)
        accuracy = correct / total
        cost /= total

        if self.tensorboard:
            self.tf.add_scalars(main_tag='performance/acc', tag_scalar_dict={'test': accuracy},
                                global_step=self.global_iter)

            self.tf.add_scalars(main_tag='performance/error', tag_scalar_dict={'test': (1 - accuracy)},
                                global_step=self.global_iter)

            self.tf.add_scalars(main_tag='performance/cost', tag_scalar_dict={'test': cost},
                                global_step=self.global_iter)

        if self.history['acc'] < accuracy:
            self.history['acc'] = accuracy
            self.history['epoch'] = self.global_epoch
            self.history['iter'] = self.global_iter
            self.save_checkpoint('best_acc.tar')

        print('test loss: %.4f' % cost,
              '| test accuracy: %.3f' % accuracy,
              '| bast accuracy: %.3f\n' % self.history['acc'])

    # 对抗样本生成
    def generate(self, num_sample, target=-1, epsilon=0.03, alpha=2 / 255, iteration=1):

        test_loader = Data.DataLoader(self.test_data, batch_size=len(self.test_data), shuffle=False)

        x_true, x_adv, values = None, None, None
        accuracy, cost, prediction, accuracy_adv, cost_adv, prediction_adv = None, None, None, None, None, None

        for (images, labels) in test_loader:
            x_true = images
            y_target = self.get_target_tensor(target, len(self.test_data))
            # TODO:先做预测，然后返回修改的tensor，再做预测
            # 做预测
            accuracy, cost, prediction = self.acc_pre(images, labels)
            # 修改tensor
            x_adv = self.FGSM(images, labels, y_target, epsilon, alpha, iteration)
            # 做周末的预测
            accuracy_adv, cost_adv, prediction_adv = self.acc_pre(x_adv, labels)

        predictions = list(prediction.numpy())
        prediction_adv = list(prediction_adv.numpy())
        logs = make_dataset(os.path.join(self.data_set_folder, 'test'), self.class_to_idx)
        detail = []
        # 创建字典 [路径:(正确标签，预测标签，对抗样本预测标签)]
        for i, (image_path, real_class, real_class_idx) in enumerate(logs):
            detail.append((image_path, real_class,
                           self.idx_to_class[predictions[i]],
                           self.idx_to_class[prediction_adv[i]]))
        log_dict = {'before_accuracy': (accuracy, cost), 'after_accuracy': (accuracy_adv, cost_adv), 'detail': detail}

        import json
        j = json.dumps(log_dict)
        save_string_2_file(os.path.join(self.data_set_folder, 'ad.json'), j)

        self.save_ad_image(x_adv, logs)
        if self.visdom:
            self.vf.imshow_multi(x_true.cpu(), title='legitimate', factor=1.5)
            self.vf.imshow_multi(x_adv.cpu(), title='perturbed(e:{},i:{})'.format(epsilon, iteration), factor=1.5)
        print('[BEFORE] accuracy : {:.4f} cost : {:.4f}'.format(accuracy, cost))
        print('[AFTER] accuracy : {:.4f} cost : {:.4f}'.format(accuracy_adv, cost_adv))

    # 预测（batch_size等于test长度的时候）
    def acc_pre(self, x_tensor, y_tensor):
        x = Variable(cuda(x_tensor, self.cuda), requires_grad=True)
        y_true = Variable(cuda(y_tensor, self.cuda), requires_grad=False)
        # 预测
        h = self.net(x)
        prediction = h.max(1)[1]
        accuracy = prediction.eq(y_true).float().mean()
        cost = F.cross_entropy(h, y_true)
        return accuracy.item(), cost.item(), prediction

    # 保存生成对抗样本
    def save_ad_image(self, tensor, logs):
        def get_path(p):
            file_folder, file_name = os.path.split(p)
            _, parent_dir = os.path.split(file_folder)
            target_folder = os.path.join(self.data_set_folder, 'perturbed', parent_dir)
            make_folder(target_folder)
            target_path = os.path.join(target_folder, file_name)
            return target_path

        # 根据log顺序把tensor保存起来。
        index = tensor.size()[0]
        for i in range(index):
            path = get_path(logs[i][0])
            save_image(tensor[i], path, padding=0)
        pass

    # 目标攻击的时候 tensor生成
    def get_target_tensor(self, target, batch):
        # 类别class和对应class_idx进行转换
        if target == -1:  # 表示没有目标
            y_target = None
        else:  # 有目标 根据输入转换成为类别
            if str(target) in self.class_to_idx:
                # y_target = torch.LongTensor([self.class_to_idx[str(target)]])
                y_target = torch.LongTensor(batch).fill_(self.class_to_idx[str(target)])
            else:
                raise ('target in put error')
        return y_target

    # 对抗样本生成算法
    def FGSM(self, x, y_true, y_target=None, eps=0.03, alpha=2 / 255, iteration=1):
        x = Variable(cuda(x, self.cuda), requires_grad=True)
        y_true = Variable(cuda(y_true, self.cuda), requires_grad=False)

        if y_target is not None:
            targeted = True
            y_target = Variable(cuda(y_target, self.cuda), requires_grad=False)
        else:
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

    # 保存模型
    def save_checkpoint(self, file_name='ckpt.tar'):
        model_states = {
            'net': self.net.state_dict(),
        }
        optim_states = {
            'optim': self.optim.state_dict(),
        }
        states = {
            'iter': self.global_iter,
            'epoch': self.global_epoch,
            'history': self.history,
            'args': self.args,
            'model_states': model_states,
            'optim_states': optim_states,
        }

        file_path = os.path.join(self.ckpt_dir, file_name)
        torch.save(states, open(file_path, 'wb+'))
        print("=> saved checkpoint '{}' (iter {})".format(file_path, self.global_iter))

    # 加载模型
    def load_checkpoint(self, file_name='best_acc.tar'):
        file_path = os.path.join(self.ckpt_dir, file_name)
        if os.path.exists(file_path):
            print("=> loading checkpoint '{}'".format(file_path))
            checkpoint = torch.load(open(file_path, 'rb'))
            self.global_epoch = checkpoint['epoch']
            self.global_iter = checkpoint['iter']
            self.history = checkpoint['history']

            self.net.load_state_dict(checkpoint['model_states']['net'])
            self.optim.load_state_dict(checkpoint['optim_states']['optim'])

            print("=> loaded checkpoint '{} (iter {})'".format(file_path, self.global_iter))

        else:
            print("=> no checkpoint found at '{}'".format(file_path))
