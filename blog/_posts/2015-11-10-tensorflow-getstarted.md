---
layout: post
title: "TensorFlow上手"
modified: 2015-11-10
feature: false
description: tensorflow 不负责任胡扯试水贴
tags: [Machine Learning]
---

## 简介
在几十个小时之前，Google开源了其“深度学习引擎” - [TensorFlow](http://tensorflow.org/)，其网站上对自身的定位是

> TensorFlow is an Open Source Software Library for Machine Intelligence

根据其简介，TensorFlow最初由 Google Brain 部门的专家和工程师开发用来做机器学习和神经网络研究。TensorFlow 采用 **数据流图(data flow graphs)** 进行数值计算。数据流图中的节点表示数学运算，数据流图中的连线表示多维数组(tensors)，用于节点之间的数据通信。其弹性架构允许将计算部署到桌面计算机、服务器甚至是移动设备上的多个CPU或者GPU。

TensorFlow在Github上的地址是[tensorflow/tensorflow](https://github.com/tensorflow/tensorflow)。

## 游戏名目

![tf00]({{ site.qnurl }}/media/tf-gs/tf00.gif){:.img-responsive}

数据流图用 **有向图(directed graph)** 中的 **节点(nodes)** 和 **连线(edges)** 来描述数学运算，节点表示数学运算，或是输入数据和运算结果的I/O；连线描述节点之间的I/O，承载 **动态多维数据阵列(dynamically-sized multidimensional data arrays)**, 开发人员称为 **Tensors**。TensorFlow的起名也来源于此。节点可以分配或部署给承载了计算资源的设备，进行异步并行计算。

## 主要特性
说实话下面几个特性看起来很屌，但是并不能具体把握到底是什么概念，这大概是一个需要开脑洞的过程(RTFM)。

* **高度灵活(Deep Flexibility)**: 使用起来非常灵活，可自定义数据流图和运算符（没看出来哪里屌）
* **真·可移植(True Portability)**: 不改变一行代码，在不同运算能力的平台上运行，并且将训练好的分类器部署到移动设备和云端或docker容器中。(这一点听起来真的好屌)
* **连通研究和生产(Connect Research and Production)**: Google 表示其研究人员在TensorFlow上做实验，然后产品部门的人用TensorFlow来训练并为用户提供服务，采用TensorFlow可以更快地将研究转化为产品，并方便了同行之间的协作和再创新。（这一点也好屌啊）
* **自动微分(Auto-Differentiation)**: 因为目前的很多机器学习算法都是基于梯度下降的，TensorFlow 将偏导数的计算简化了(说实话这点没看懂哪里屌)
* **编程接口(Language Options)**: 目前支持Python和C++接口，提供[IPython notebook](http://ipython.org/notebook.html)用于交互式计算，后期预计会增加Go、Java、Lua、JavaScript、R的接口。
* **性能最大化(Maximize Performance)**: 声称对线程、队列和异步计算提供了"first-class support"，号称可以自由地将计算单元部署到不同的设备。（屌屌屌屌屌）。

## 开源协议
采用[Apache 2.0 open source license](http://www.apache.org/licenses/LICENSE-2.0)，懂的人都知道，这个协议相对来说放得很开，参考[五种开源协议的比较(BSD,Apache,GPL,LGPL,MIT) – 整理](http://www.awflasher.com/blog/archives/939)。

**为什么Google要开源这么屌的东西？**

Google给的理由简单得难以置信

> If TensorFlow is so great, why open source it rather than keep it proprietary?

Google表示要在机器学习领域搞一套标准化的工具，促进学术研究和产品研发的业内交流，并且希望TensorFlow能造福开发者和用户。最后Google也说了，自家工程师的学术文章今后都打算用TensorFlow来做程序实现和实验研究。

话说到这里，除了承认自己想立标准外，实在也看不出谷爷寓意何在。等业界评论和分析吧。

## 安装TensorFlow
比较讨人喜欢的是，普通的计算机也可以轻松地安装TensorFlow，因为其本身就表示可以运行在不同计算能力的设备上，故对GPU硬件无强制要求。安装TensorFlow是一个非常愉快的过程，因为如果你是一个Python用户，安装TensorFlow和安装其它Python包一样简单无比。

### 二进制安装
目前官方文档表示支持Linux和OS X上方便地安装编译好的二进制文件，倒也不是不照顾Windows，而是这个我们要安装的TensorFlow说白了就是一个Python的包，用pip就可以安装。TensorFlow提供了三种安装方式:

1. 直接使用pip安装
2. 用Python的VirtualEnv安装
3. 直接下载一个配置好的Docker镜像

**使用pip安装**：有CPU和GPU两个版本


```bash
# CPU 版本
$ pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.5.0-cp27-none-linux_x86_64.whl
# GPU版本(需要CUDA sdk)
$ pip install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.5.0-cp27-none-linux_x86_64.whl
```

**使用VirtualEnv安装**: 使用Python的VirtualEnv包安装，更容易维护，感觉不对把文件夹删了再重新安装就行了，下面说说怎么安装:

* 首先安装依赖的Python包

```bash
    $ sudo apt-get install python-pip python-dev python-virtualenv
```
* 创建一个文件夹作为虚拟环境

```bash
    $ mkdir tensorflow
```
* 为创建的文件夹配置VirtualEnv

```bash
    $ virtualenv --system-site-packages ~/tensorflow
```
* 激活VirtualEnv(激活完成会看到命令行提示符)

```bash
    $ cd tensorflow && source bin/activate
```
* 安装TensorFlow

```bash
    (tensorflow)$ pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.5.0-cp27-none-linux_x86_64.whl
```

注意输入`deactivate`可以退出VirtualEnv。

**下载Docker镜像安装**: 首先需要确保系统安装了较新版本的docker(`sudo apt-get install docker`)，然后只需要下载提供的镜像就可以了

```bash
$ docker run -it b.gcr.io/tensorflow/tensorflow
```
或者这个镜像

```bash
$ docker run -it b.gcr.io/tensorflow/tensorflow-full
```
后者提供了一些附加的源代码和tutorial性质的示例程序。

**注意** : 亲测目前需要翻墙才能较顺利地下载TensorFlow的Docker镜像。

### 测试
打开终端运行Python，输一下以下代码，没报错基本就对了。注意一定要用Python2.7版本的，对于某些比较激进地已经把Python3作为默认Python的Linux发行版，需要做格外设置。


```Python
$ python
>>> import tensorflow as tf
>>> hello = tf.constant('Hello, TensorFlow!')
>>> sess = tf.Session()
>>> print sess.run(hello)
Hello, TensorFlow!
>>> a = tf.constant(10)
>>> b = tf.constant(32)
>>> print sess.run(a+b)
42
```

注意上面的代码已经体现出TensorFlow的一些思想了，比如注意那个`.Session()`，正好体现了之前所说的真·可移植性。事实上TensorFlow正是使用Session来将数据流图部署到不同的设备上(CPU、GPU)，和前序步骤的数据流图定义可以相互独立，这一点显得非常炫酷。

## 基础使用
使用TensorFlow前首先需要了解TensorFlow是如何完成下面这几件事的：

* 将计算表示成数据流图
* 在Session中执行数据流图
* 将数据表示为Tensors
* 使用变量(Variables)来维护状态
* 对任意的计算(节点)进行数据I/O(TensorFlow称为"feeds and fetches")

正如之前所说，TensorFlow是用于将计算表示成数据流图的编程系统，数据流图中的节点称为ops(Operations)，一个op接收0个或多个Tensors，运行计算，并生成0个或多个Tensors。一个Tensor是某种数据类型的多维阵列，如对于一个图像数据的[mini-batch](https://class.coursera.org/ml-003/lecture/106)，可以用一个浮点类型的4维阵列来表示，即`[batch, height, width, channels]`。TensorFlow是对计算的描述，其运行需要依赖Session，Session将ops部署到设备上，并提供运算方法，运算结果在Python上是[Numpy](http://www.numpy.org/)的[ndarray类型](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)，在C++上是`tensorflow::Tensor`，也就是本质上的Tensor。

可以看出，TensorFlow主要包括两个步骤:数据流图的构建、Session部署。官方文档建议用Python来进行数据流图的构建，因为Python接口提供了很多C++接口没有的helper function。

### 构建数据流图
TensorFlow默认提供了单一的数据流图容器来容纳数据流图的节点，当然也支持使用多个数据流图容器。我们从单容器开始了解，不需要手动地进行数据流图层面的操作。


```python
import tensorflow as tf

matrix1 = tf.constant([[3., 3.]])
matrix2 = tf.constant([[2.],[2.]])
product = tf.matmul(matrix1, matrix2)
```

上面的代码首先创建一个 **常量(Constant)** 节点`matrix1`，存储了一个$$1\times2$$矩阵，以及另一个常量节点`matrix2`，存储了一个$$2\times1$$矩阵。注意这里使用“存储”并不恰当，因为我们知道节点只进行数据的I/O，定义的是计算操作而不是变量。所以实际上这两个节点不接收输入数据，输出矩阵数据，这样理解才符合TensorFlow的设计思想。常量节点不接收输入数据。然后`product`节点定义了矩阵乘法运算，接收`matrix1`和`matrix2`的输出数据流。

注意！这里实际上都是构建操作，一丁点计算操作都没有发生，这容易和我们传统的编程思维冲突。要进行实际的计算，我们必须要借助于Session!截至目前，我们不过定一个两种类型(constant()和matmul())的三个节点(ops)而已，它们都在默认的数据流图中(脑中很容易画出这个数据流图吧，哈哈哈)。

### 部署节点
构建完成数据流图后，首先需要创建Session对象，Session可接收参数，如果不指定参数，则加载默认数据流图。


```python
sess = tf.Session()
result = sess.run(product)
print result
sess.close()
```

上面的代码首先加载默认数据流图，然后使用`.run()`启动节点`product`上的计算操作，会自动调用`matrix1`和`matrix2`的输出并进行矩阵运算(实际上是求内积)。最后使用`.close()`关闭Session。

和Python的文件操作符一样，不想手动关闭的话，就用`with...as...`语法，就是这么方便：

```python
with tf.Session() as sess:
    result = sess.run([product])
    print result
```

当具有多个处理单元时，可以使用`with...Device`来指定节点部署到哪个单元上，例如

```python
with tf.Session() as sess:
  with tf.device("/gpu:1"):
    matrix1 = tf.constant([[3., 3.]])
    matrix2 = tf.constant([[2.],[2.]])
    product = tf.matmul(matrix1, matrix2)
    ...
```

一般`/cpu:0`表示CPU，`/gpu:0`表示第一个GPU，`/gpu:1`表示第二个GPU。

### 交互运行
用过IPython的都知道`.eval()`，TensorFlow使用`InteractiveSession`来支持交互式运行，这样可以避免前面那样用一个变量来保持Session。示例


```python
# Enter an interactive TensorFlow Session.
import tensorflow as tf
sess = tf.InteractiveSession()

x = tf.Variable([1.0, 2.0])
a = tf.constant([3.0, 3.0])

# Initialize 'x' using the run() method of its initializer op.
x.initializer.run()

# Add an op to subtact 'a' from 'x'.  Run it and print the result
sub = tf.sub(x, a)
print sub.eval()
# ==> [-2. -1.]
```

## 变量
Tensors和我们熟悉的变量具有本质上的不同，在TensorFlow的思考领域里，变量用于在数据流图 **执行** 时 **维护状态**，注意是在执行的时候！

```python
state = tf.Variable(0, name="counter")
one = tf.constant(1)
new_value = tf.add(state, one)
update = tf.assign(state, new_value)
init_op = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init_op)
    print sess.run(state)
    for _ in range(3):
        sess.run(update)
        print sess.run(state)
```

所谓维护状态，即保存某些节点的运行现场。比如上例，创建的`state`节点的输出即是变量类型，注意变量类型节点使用前需要初始化，通过`init_op`节点来完成。在`for`循环内，首先执行`update`节点：`update`节点会调用`state`节点和`new_value`节点，给`state`节点的变量用`new_value`节点的输出赋值，`new_value`节点又会调用`state`节点和`one`节点，进行加1操作；然后执行`state`节点并打印节点的变量值。

因为变量保存现场的特性，在机器学习里，常用于存储权值，例如神经网络的权值矢量，就可以作为变量存储在一个Tensor中。

### Fetches(抓取节点输出)
之前我们用`.run()`时实际上就是一个获取节点输出的过程，TensorFlow还支持一次性对多个节点进行抓取，只需要用方括号括起来就行了，示例

```python
input1 = tf.constant(3.0)
input2 = tf.constant(2.0)
input3 = tf.constant(5.0)
intermed = tf.add(input2, input3)
mul = tf.mul(input1, intermed)

with tf.Session():
  result = sess.run([mul, intermed])
  print result

# output:
# [array([ 21.], dtype=float32), array([ 7.], dtype=float32)]
```

### Feeds(给节点输入数据)
之前介绍的操作都没有涉及到给节点输入数据，TensorFlow使用`placeholder`来描述等待输入的节点，只需要指定类型即可，然后在执行节点的时候用一个字典来“喂食”这些节点即可，示例

```python
input1 = tf.placeholder(tf.types.float32)
input2 = tf.placeholder(tf.types.float32)
output = tf.mul(input1, input2)

with tf.Session() as sess:
  print sess.run([output], feed_dict={input1:[7.], input2:[2.]})

# output:
# [array([ 14.], dtype=float32)]
```

## 然后呢？
因为TensorFlow这货设计确实还蛮先进的(意思就是好多东西都还需要时间理解)，下面提供相关的资料链接:

1. [Github仓库](https://github.com/tensorflow/tensorflow)
2. [官方Tutorial](http://tensorflow.org/tutorials)
3. [TensorFlow机制](http://tensorflow.org/how_tos)
4. [API文档](http://tensorflow.org/api_docs)
5. [FAQ](http://tensorflow.org/resources/faq.md)

其中\[2\]中从Softmax讲到CNN，RNN，word2vec，是最佳的实战教程。\[3\]对理解TensorFlow的思想有帮助，在下认为[TensorBoard: Visualizing Learning](http://tensorflow.org/how_tos/summaries_and_tensorboard/index.md)非常有趣！

## 手感
接触TensorFlow的第一天，总体感受:

1. 文档健全，除了官方的文档页，到Github仓库的子文件夹下面还有许多README.md页，讲得很详细，对初学者还专门提供了教程，非常友好；
2. 接口友好，使用很直观;
3. 工具先进，比如TensorBoard;
4. 思想超前;
5. 期待其进一步开源!
