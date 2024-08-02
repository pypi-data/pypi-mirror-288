# TorchCat 🐱

# 简介

TorchCat 是用于封装 PyTorch 模型的工具

提供以下功能：

- 封装模型
  - 简化模型训练
  - 简化模型评估
  - 记录训练日志
- 加载数据集

# 封装模型

使用 `torchcat.Cat` 封装你的模型。如果不进行训练，也可以忽略 `loss_fn`、`torchcat` 参数

```python
net = nn.Sequential(
    nn.Flatten(),
    nn.Linear(28*28, 128),
    nn.ReLU(),
    nn.Linear(128, 10),
)

net = torchcat.Cat(model=net,
                   loss_fn=nn.CrossEntropyLoss(),
                   optimizer=torch.optim.Adam(net.parameters(), lr=0.0003))
```

| 参数      | 说明     |
| --------- | -------- |
| model     | 你的模型 |
| loss_fn   | 损失函数 |
| optimizer | 优化器   |

## 查看架构

在封装模型后，使用 **net.summary()**，可以查看模型的架构。**input_size** 参数需填写模型的输入形状，如：`net.summary(1, 28, 28)`

## 训练模型

使用 `net.train()`，可以开始模型的训练。训练结束后会返回训练日志

```python
log = net.train(train_set=train_set, epochs=5, valid_set=test_set)
```

`log` 记录了训练时的日志，包括以下内容

* 训练集损失（**log['train** **loss']**）
* 训练集准确率（**log['train** **acc']**）
* 验证集损失（**log['valid** **loss']**）
* 验证集准确率（**log['validacc']**）

| 参数      | 说明                |
| --------- | ------------------- |
| train_set | 训练集              |
| epochs    | 训练轮次            |
| valid_set | 验证集（默认 None） |

## 评估模型

使用 `net.valid(valid_set, show=True, train=False)`，能够验证模型在给定验证集上的性能，包括损失值、准确率。验证后模型将切换为推理模式

| 参数      | 说明                                           |
| --------- | ---------------------------------------------- |
| valid_set | 验证集                                         |
| show      | 是否输出验证集损失值、准确率（默认 True）      |
| train     | 验证后，模型是否且切换为训练模式（默认 False） |

## 其他

### 切换计算设备

TorchCat 提供了方法 `to_cpu()`、`to_cuda()` 用于切换计算设备（CPU 或 GPU🚀）

### 检查模型当前模式

使用 `training` 方法，模型当前是否处于训练模式。返回 `True` 表示处于训练模式，`False` 表示处于推理模式

### 模型推理

* 方法名：`__call__`
* 功能描述：执行模型的前向推理过程
* 参数：`x` - 输入数据
* 返回值：模型对输入数据 `x` 的推理结果

# 加载数据集

使用 `torchcat.ImageFolder` 用于加载图片数据集

```python
# 图像预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# 加载数据集
dataset = torchcat.ImageFolder(path='train image', one_hot=True, transform=transform)
```

| 参数      | 说明                                |
| --------- | ----------------------------------- |
| path      | 数据集路径                          |
| one_hot   | 是否进行 One-Hot 编码（默认 False） |
| transform | 图像预处理方案（默认 None）         |
