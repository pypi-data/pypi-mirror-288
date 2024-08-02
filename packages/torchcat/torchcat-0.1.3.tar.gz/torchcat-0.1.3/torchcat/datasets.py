'''
𝕋𝕠𝕣𝕔𝕙ℂ𝕒𝕥

:copyright: (c) 2024 by KaiYu.
:license: GPLv3, see LICENSE for more details.
'''

import torch
from torchvision import datasets
from torch.nn import functional as F


class ImageFolder(torch.utils.data.Dataset):
    '''
    用于加载图片数据集
    '''

    def __init__(self, path, one_hot=False, transform=None):
        '''
        初始化

        Parameters
        --------
        path : 数据集路径
        one_hot : 是否进行 one-hot 编码
        transform : 数据预处理
        '''
        # 定义 one-hot 编码表示
        self.one_hot = one_hot

        # 加载数据集
        self.data_set = datasets.ImageFolder(path, transform=transform)

        # 进行 one-hot 编码
        if one_hot:
            self.data_set.target_transform = lambda x: F.one_hot(torch.tensor(x), len(self.classes)).float()

    def __getitem__(self, index):
        '''获取数据'''
        return self.data_set[index]

    def __len__(self):
        '''获取数据集长度'''
        return len(self.data_set)

    @property
    def classes(self):
        '''获取数据集类别'''
        return self.data_set.classes

    @property
    def class_to_idx(self):
        '''获取数据集类别与编号'''
        return self.data_set.class_to_idx
