---
title: "Pybrain教程"
date: 2016-03-03 12:05:30
updated: 2016-12-30 14:44:00
categories: python
---



 easy_install scipy
$ easy_install matplotlib
pybrain把数据处理算法叫做Module，一个network本身也是一个Module，自由参数free parameters是通过Trainder来调整的，

pybrain
        structure
            FeedForwardNetwork
            LinearLayer
            SigmoidLayer
        datasets
            SupervisedDataSet：监督数据集
            ClassificationDataSet：分类数据集
        tools.shortcuts
            buildNetwork：快速构建神经网络
        pybrain.supervised.trainers：训练器
            BackpropTrainer
神经网络的构建
# 这里是快速使用网络
from pybrain.tools.shortcuts import buildNetwork
net = buildNetwork(2, 3, 1)  # 表示二维输入，3个隐藏层，1维输出

# Feed Forward Network 自己构建一个网络
from pybrain.structure import FeedForwardNetwork
n = FeedForwareNetwork()
# 接着构建那三层
from pybrain.structure import LinearLayer, SigmoidLayer
inLayer = LinearLayer(2)
hiddenLayer = SigmoidLayer(3)
outLayer = LinearLayer(1)
# 必须将几个层加入到网络中，为了网络能够前向传输输入和后向传输错误，必须指明哪一个是输入哪一个是输出
n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addOutputModule(outLayer)
# 必须明确他们该怎样连接，其中一个连接方式是FullConnection
from pybrain.structure import FullConnection
in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)
# 还得将模块与网络连接
n.addConnection(in_to_hidden)
n.addConnection(hidden_to_out)
# 最后为了让我们的MLP能使用，得
n.sortModules()    
# print n 查看该神经网络的结构
# 初始化一个神经网络
n.activate([1, 2]  # 初始化的时候给一组数据进去就行了
# 查看初始化后的一些参数
in_to_hidden.params
hidden_to_out.params
n.params
# 给自己的神经网络命名
LinearLayer(2, name="foo")

# 第二个例子构建Recurrent Networks递归神经网络    


# 不同的隐藏层：TanhLayer, SoftmaxLayer,

数据集
ds = SupervisedDataSet(2, 1)  # 表示二维输入，一维输出
ds.addSample(   (0, 0),  (0)  )   # 添加样本，第一个参数是输入，第二个参数是输出
# 对数据集的操作，inputs表示输入，targets表示目标(输出)
len(ds)  # 数据集的样本数
for inpt, target in ds:   # 对数据集进行遍历
ds['input'],   ds['target']  # 获取所有的输入样本和相应的输出样本
ds.clear()  # 清空数据集

# SupervisedDataSet，监督训练的数据集，使用的appendLinked
# sequential dataset, 监督序列回归训练数据集
# classification：分类训练数据集
# importance：加权监督数据集

训练器
from pybrain.supervised.trainers import BackpropTrainer
net = buildNetwork(2, 3, 1, bias=True, hiddenclass=TanhLayer)
trainer = BackpropTrainer(net, ds)
trainer.train() # 这就是在训练了，会输出错误的比例
trainer.trainUnitilConvergence()  # 输出每个数据的收敛情况


分类
使用前馈神经网络进行分类
http://pybrain.org/docs/tutorial/fnn.html   使用了pylab的

alldata = ClassificationDataSet(2, 1, nb_classes=3)  # 这种方式新建分类数据集
alldata.addSample(输入，类别)  # 这种方式添加数据
test, train = alldata.splitWithProportion(0.25)  # 使测试数据占0.25， 训练数据占75%
train._convertToOneOfMany()  # 建议一个类别一个类，这句话啥子意思哟
test._convertToOneOfMany()  # 这两个操作会将原始目标重复并且将他们存储在'class'字段
# 查看我们的数据
len(train)  # 输出训练数据的长度
train.indim, train.outdim  # 输出数据的inupt纬度和输出纬度
train['input'][0], train['target'][0], train['class'][0],   # 输出第一个样本的输入数据，输出数据和分类
# 构造神经网络
fnn = buildNetwork(train.indim, 5, train.outdim, outclass=SoftMaxLayer)
trainer = BackpropTrainer(fnn, dataset=train, momentum=0.1, verbose=True, weightdecay=0.01)# 设置一个训练器
trainer.trainEpochs(1) # 训练一次的结果，可以多次训练
trnresult= percentError(  trainer.testOnClassData(),  trandata['class'])
tstresult = percentError( trainer.testOnClassData(dataset=tstdata), tstdata'class']












黑盒优化

强化学习












