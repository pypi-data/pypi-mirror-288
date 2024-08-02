'''
𝕋𝕠𝕣𝕔𝕙ℂ𝕒𝕥

:copyright: (c) 2024 by KaiYu.
:license: GPLv3, see LICENSE for more details.
'''

from .metrics import Loss

import numpy as np
import pandas as pd
from torchsummary import summary


class Cat:
    '''
    这只猫🐱能够封装你的模型
    '''

    def __init__(self, model, loss_fn=None, optimizer=None, metrics=None, scheduler=None):
        '''
        初始化

        Parameters
        --------
        model: 模型
        loss_fn: 损失函数
        optimizer: 优化器
        metrics: 评价指标
        scheduler: 学习率调度器
        '''
        # 定义模型
        self.model = model

        # 定义损失函数
        self.loss_fn = loss_fn

        # 定义优化器
        self.optimizer = optimizer

        # 定义评价指标
        self.metrics = metrics
        self.loss_list = Loss()
        self.metrics_list = {i.__name__: i for i in metrics}

        # 定义学习率调度器
        self.scheduler = scheduler

        # 定义 GPU 标志
        self.GPU_FLAG = next(model.parameters()).is_cuda

        # 训练日志
        self.log = {'train loss': [], 'valid loss': []}
        for metrics in self.metrics_list:
            self.log[f'train {metrics}'] = []
            self.log[f'valid {metrics}'] = []

        # 当未定义损失函数或优化器时，打印提示
        if (loss_fn and optimizer) is None:
            print('未检测到损失函数或优化器，这将会影响到你的模型训练🙂')

    def train(self, epochs, train_set, valid_set=None):
        '''
        训练模型

        Parameters
        --------
        epochs : 训练轮数
        train_set : 训练集数据
        valid_set : 验证集数据

        Returns
        --------
        log : 训练日志
        '''
        self.model.train()
        for epoch in range(1, epochs + 1):
            ######## 模型训练 ########
            for x, y in train_set:
                if self.GPU_FLAG:
                    x, y = x.cuda(), y.cuda()
                self.optimizer.zero_grad()
                pred = self.model(x)
                loss = self.loss_fn(pred, y)
                loss.backward()
                self.optimizer.step()

                # 计算 loss
                self.loss_list.update_state(loss.item())  # 更新 loss
                # 计算各项 metrics
                for metrics in self.metrics_list:
                    value = self.metrics_list[metrics].update_state(pred.cpu().detach().numpy(), y.cpu().numpy())  # 更新 metrics

            train_output = {}  # 构造输出日志
            ######## 训练部分 ########
            # 计算每个 epoch 的平均 loss
            loss = self.loss_list.result()  # 获取 loss
            self.loss_list.reset_state()  # 重置 loss
            train_output['Loss'] = loss   # 输出 loss
            self.log['train loss'].append(loss)  # 记录 loss

            # 计算每个 epoch 的平均 metrics
            for metrics in self.metrics_list:
                value = self.metrics_list[metrics].result()  # 获取 metrics
                self.metrics_list[metrics].reset_state()  # 重置 metrics
                train_output[metrics] = value   # 输出 metrics
                self.log[f'train {metrics}'].append(value)  # 记录 metrics

            ######## 验证部分 ########
            if valid_set is not None:
                valid_output = self.valid(valid_set, show=False, train=True)
                for key, value in valid_output.items():
                    self.log[f'valid {key}'].append(value)
                print(f'Epoch {epoch}/{epochs}',
                      f'Train-<{" ".join([f"{key}: {value:.6f}" for key,value in train_output.items()])}>',
                      f'Valid-<{" ".join([f"{key}: {value:.6f}" for key,value in valid_output.items()])}>')
            else:
                print(f'Epoch {epoch}/{epochs}',
                      f'Train-<{" ".join([f"{key}: {value:.6f}" for key,value in train_output.items()])}>')

        return pd.DataFrame(self.log)

    def valid(self, valid_set, show=True, train=False):
        '''
        验证模型

        Parameters
        --------
        valid_set : 验证集
        show : 是否输出损失值、评价指标
        train : 验证完毕后是否切换为训练模式

        Returns
        --------
        log : 在验证集上的的损失值、评价指标
        '''
        self.model.eval()
        loss_list = Loss()
        metrics_list = {i.__name__: i for i in self.metrics}
        for x, y in valid_set:
            if self.GPU_FLAG:
                x, y = x.cuda(), y.cuda()
            pred = self.model(x)
            loss = self.loss_fn(pred, y).item()
            loss_list.update_state(loss)  # 计算验证集 loss
            for metrics in metrics_list:  # 计算验证集 metrics
                metrics_list[metrics].update_state(pred.cpu().detach().numpy(), y.cpu().numpy())

        # 构造输出日志
        log = {'loss': loss_list.result()}
        for metrics, value in metrics_list.items():
            log[metrics] = value.result()

        if train:
            self.model.train()
        if show:
            for key, value in log.items():
                print(f'{key}: {value:.6f}')

        return log

    def summary(self, *input_size):
        '''
        查看架构

        Parameters
        --------
        input_size : 模型输入的形状
        '''
        # 判断GPU是否可用
        if self.GPU_FLAG:
            device = 'cuda'
        else:
            device = 'cpu'
        summary(self.model, input_size, device=device)

    def clear_log(self):
        '''清空训练日志'''
        self.log = {'train loss': [], 'valid loss': []}
        for metrics in self.metrics_list:
            self.log[f'train {metrics}'] = []
            self.log[f'valid {metrics}'] = []

    @property
    def training(self):
        '''查看模型是否处于训练模式'''
        return self.model.training

    def to_train(self):
        '''切换到训练模式'''
        self.model.train()

    def to_eval(self):
        '''切换到推理模式'''
        self.model.eval()

    def to_cpu(self):
        '''切换到 CPU 运行'''
        self.model.cpu()
        self.GPU_FLAG = False

    def to_cuda(self):
        '''切换到 GPU 运行'''
        self.model.cuda()
        self.GPU_FLAG = True

    def __call__(self, x):
        '''模型推理'''
        return self.model(x)
