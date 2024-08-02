'''
𝕋𝕠𝕣𝕔𝕙ℂ𝕒𝕥

:copyright: (c) 2024 by KaiYu.
:license: GPLv3, see LICENSE for more details.
'''

import numpy as np


# 计算准确率
def accuracy(pred, label):
    return np.equal(np.argmax(pred, axis=1), np.argmax(label, axis=1)).mean()


# 计算准确率（当损失函数使用 CrossEntropyLoss 时）
def crossentropy_accuracy(pred, label):
    return np.equal(np.argmax(pred, axis=1), label).mean()


# 计算混淆矩阵
def confusion_matrix(pred, label):
    cm = np.zeros((max(label)+1, max(label)+1), dtype='int32')
    for y, x in zip(pred, label):
        cm[y, x] += 1
    return cm


# 计算损失
class Loss:
    __name__ = 'Loss'

    def __init__(self):
        self.loss = []

    def update_state(self, loss):
        self.loss.append(loss)

    def reset_state(self):
        self.loss = []

    def result(self):
        loss = np.mean(self.loss)

        return loss


# 计算准确率
class Accuracy:
    __name__ = 'Accuracy'

    def __init__(self):
        self.accuracy = []
        self.weight = []

    def update_state(self, pred, label):
        acc = np.equal(np.argmax(pred, axis=1), np.argmax(label, axis=1)).mean()
        self.accuracy.append(acc)
        self.weight.append(len(label))

    def reset_state(self):
        self.weight = []
        self.accuracy = []

    def result(self):
        weight = np.divide(self.weight, np.sum(self.weight))
        accuracy = np.dot(weight, self.accuracy)

        return accuracy


# 计算准确率（当损失函数使用 CrossEntropyLoss 时）
class CrossEntropyAccuracy:
    __name__ = 'CrossEntropyAccuracy'

    def __init__(self):
        self.weight = []
        self.accuracy = []

    def update_state(self, pred, label):
        acc = np.equal(np.argmax(pred, axis=1), label).mean()
        self.accuracy.append(acc)
        self.weight.append(len(label))

    def reset_state(self):
        self.weight = []
        self.accuracy = []

    def result(self):
        weight = np.divide(self.weight, np.sum(self.weight))
        accuracy = np.dot(weight, self.accuracy)

        return accuracy
