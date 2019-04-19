---
layout: post
title: 齐次坐标系入门级思考
modified: 2017-03-29
feature: true
description: 关于齐次坐标系、透视投影变换成像的一些思考。
tags: [CV]
---

**齐次坐标系（Homogeneous Coordinates）** 是计算机视觉和图形学中的一个重要的数学工具。

## 1. 游戏名目

### 1.1. 齐次坐标引入

在欧式空间里，两条共面的平行线无法相交，然而在 **投影空间（Projective Space）** 内却不是这样，一个感性的理解是，如下图中的两条铁轨的间距随着视线变远而减小，直至在地平线处（无限远点）相交。

![railway]({{ site.qnurl }}/media/homogeneous/railway.jpg){:.img-fluid .rounded .mx-auto .d-block}

欧式空间采用 $$(x,y,z)$$ 来表示一个三维点，但是无穷远点 $$(\infty,\infty,\infty)$$ 在欧式空间里是没有意义的，在投影空间中进行图形和几何运算并不是一个简单的问题，为了解决这个问题，数学家 August Ferdinand Möbius[^mobius] 提出了齐次坐标系，采用 $$N+1$$ 个量来表示 $$N$$ 维坐标。例如，在二维齐次坐标系中，我们引入一个量 $$w$$，将一个二维点 $$(x,y)$$ 表示为 $$(X,Y,w)$$ 的形式，其转换关系是

[^mobius]:中文音译名莫比乌斯，德国数学家，[Wikipedia](http://en.wikipedia.org/wiki/August_Ferdinand_M%C3%B6bius)

$$
\begin{array}{l}
x=\frac{X}{w}\\
y=\frac{Y}{w}
\end{array}
$$

例如，在欧式坐标中的一个二维点 $$(1,2)$$ 可以在齐次坐标中表示为 $$(1,2,1)$$，如果点逐渐移动向无穷远处，其欧式坐标变为 $$(\infty,\infty)$$，而齐次坐标变为 $$(1,2,0)$$，注意到在齐次坐标下不需要 $$\infty$$ 就可以表示无限远处的点。

### 1.2. “齐次”之名？

如果我们要将欧式坐标的一个二维点 $$(1,2)$$ 转换为齐次坐标，根据规则，我们可以选择刚才用到的 $$(1,2,1)$$，也可以选择 $$(2,4,2)$$，还可以选择 $$(4,8,4),(8,16,8)...$$，即 $$(k,2k,k),k\in\mathbb{R}$$ 都是“合法”的齐次坐标表示，这些点都映射到欧式空间中的一点，即这些点具有 **尺度不变性（Scale Invariant）**，是“齐性的”(同族的)，所以称之为齐次坐标。

同样的，线性系统的齐次性是指在输入量倍乘的情况下，输出同时倍乘同一因子。以及齐次函数的定义等，都和倍乘某一个常数因子有关。

### 1.3. 平行线相交:不太严格的证明

考虑两条平行线：

$$
\left\{ \begin{array}{l}
Ax+By+C=0\\
Ax+By+D=0
\end{array} \right.
$$

在欧式空间中，$$C=D$$ 时两条线重合，否则不相交。尝试用 $$\frac{x}{w},\frac{y}{w}$$ 替换 $$x,y$$（如前面提到的，用 $$N+1$$ 个量表示 $$N$$ 维坐标，这里增加了一个量 $$w$$），可以得到：

$$
\left\{ \begin{array}{l}
Ax+By+Cw=0\\
Ax+By+Dw=0
\end{array} \right.
$$

可以得到解 $$(x,y,0)$$，即两条平行线在 $$(x,y,0)$$ 处相遇，称之为无穷点（注意这里不要用欧式空间的思维去想象这个点在哪里）。

### 1.4.重要性

《计算机图形学(OpenGL版)》的作者F.S. Hill Jr. 写到：

> “齐次坐标表示是计算机图形学的重要手段之一，它既能够用来明确区分向量和点，同时也更易用于进行仿射（线性）几何变换。”

于是我们知道，其重要性，主要有二：其一，是区分向量和点；其二，是易于进行 **仿射变化（Affine Transformation）**，但是这两点内部的原因又是什么呢？吹牛逼要吹到家，总不能说是大牛说的就是对的吧，要理解这两点，需要进行更细致一些的了解，请往下看。

## 2. 深入理解

首先，我们需要对齐次坐标系的形式化表达更明了，为了简化说明，主要以 2 维点做之后的说明。

### 2.1. 平面点

欧式坐标表示：

$$\textbf{x}=(x,y) \in \mathbb{R}^2$$

齐次坐标表示：

$$\tilde{x}=(\hat{x},\hat{y},w) \in \mathbb{P}^2 $$

$$w=0$$ 时称为 **无穷点（points at infinity）**，其中 $$\mathbb{P}^2=\mathbb{R}^3-(0,0,0)$$ 为 **2D投影空间**。**齐次矢量** $$\tilde{x}$$ 可转换为欧式表示：

$$\tilde{x}=(\hat{x},\hat{y},w)=w(x,y,1)=w\bar{\textbf{x}}$$

$$\bar{\textbf{x}}$$ 称为 **增广矢量(augmented vector)**。

### 2.2. 平面线

齐次表示：

$$\tilde{l}=(a,b,c)$$

对应欧式空间直线方程：

$$\bar{\textbf{x}}\cdot\tilde{l}=ax+by+c=0$$

例外是在 $$\tilde{l}=(0,0,1)$$ 时为 **无穷线**，包含了所有的2维无穷点。

可将 $$\tilde{l}$$ 标准化为 $$l=(\hat{n}_x,\hat{n}_y,d)=(\hat{\textbf{n}},d),\parallel\hat{\textbf{n}}\parallel=1$$，$$\hat{\textbf{n}}$$ 称为 **法向量**，与直线 $$\tilde{l}$$ 垂直，$$d$$ 为原点到直线的距离，下图给出了比较形象的解释：

![railway]({{ site.qnurl }}/media/homogeneous/2dline.png){:.img-fluid .rounded .mx-auto .d-block}

采用齐次坐标系时，可求得两条直线的交点的齐次表达：

$$\tilde{x}=\tilde{l}_1\times\tilde{l}_2$$

$$\times$$ 表示叉积。同时，两个点确定的直线方程的齐次表达为：

$$\tilde{l}=\tilde{x}_1\times\tilde{x}_2$$

以上结论的严格的证明是很容易的，最粗暴简单的思路就是在欧式空间内计算出结果后转化为齐次表达，并与采用齐次表达计算结果进行对比，这里略过。

### 2.3. 更易用于仿射变换？

对于一个 2 维点 $$p=(x,y)$$，仿射变换（$$T$$）是线性变换（$$Ap$$）和平移变换（$$+t$$）的叠加:

$$
T(p)=Ap+t
$$

线性变换在欧式空间中可以表示为矩阵乘积形式，如旋转变换和缩放变换：

$$
\left[ \begin{array}{l}
\grave{x}\\
\grave{y}
\end{array} \right]=
\left[ \begin{array}{cc}
cos(\theta) & -sin(\theta)\\
sin(\theta) & cos(\theta)
\end{array}
\right]
\left[ \begin{array}{l}
x\\
y
\end{array}
\right]
$$

$$
\left[ \begin{array}{l}
\grave{x}\\
\grave{y}
\end{array} \right]=
\left[ \begin{array}{cc}
S_x & 0\\
0 & S_y
\end{array}
\right]
\left[ \begin{array}{l}
x\\
y
\end{array}
\right]
$$

而平移变换

$$
\left[ \begin{array}{l}
\grave{x}\\
\grave{y}
\end{array} \right]=
\left[ \begin{array}{c}
x\\
y
\end{array}
\right]
+\left[ \begin{array}{l}
t_x\\
t_y
\end{array}
\right]
$$

却不能用矩阵相乘的形式表达。现在引入齐次坐标系表达 $$\tilde{p}=(x,y,1)$$，（尺度不变性，实际上在高一维的空间映射到 $$w=1$$ 平面, 这样计算后结果直接可导出到欧式空间）。可以将旋转变换和尺度变换表示为：

$$
\left[ \begin{array}{l}
\grave{x}\\
\grave{y}\\
1
\end{array} \right]=
\left[ \begin{array}{ccc}
cos(\theta) & -sin(\theta) & 0 \\
sin(\theta) & cos(\theta) & 0 \\
0 & 0 & 1
\end{array}
\right]
\left[ \begin{array}{l}
x\\
y\\
1
\end{array}
\right]
$$

$$
\left[ \begin{array}{l}
\grave{x}\\
\grave{y}\\
1
\end{array} \right]=
\left[ \begin{array}{ccc}
S_x & 0 & 0\\
0 & S_y & 0\\
0 & 0 & 1
\end{array}
\right]
\left[ \begin{array}{l}
x\\
y\\
1
\end{array}
\right]
$$

平移变换表示为：

$$
\left[ \begin{array}{l}
\grave{x}\\
\grave{y}\\
1
\end{array} \right]=
\left[ \begin{array}{ccc}
1 & 0 & t_x\\
0 & 1 & t_y\\
0 & 0 & 1
\end{array}
\right]
\left[ \begin{array}{l}
x\\
y\\
1
\end{array}
\right]
$$

然后我们可以导出仿射变换的矩阵形式，

$$
T=\left[
\begin{array}{cc}
\textbf{A} & \textbf{t}\\
\textbf{O}_{1\times2} & 1
\end{array}
\right]
\left[ \begin{array}{l}
x\\
y\\
1
\end{array}
\right]
$$

其中 $$\textbf{O}_{1\times2}=[0~~0]$$，仿射变换保留了点的共线/面性质及比例（可以参考一些图形学资料），这在图形处理中非常重要，比如对于平面上的一个几何形状进行变换，只需要对其顶点进行变换就可实现（在 2 维线上的点变换后一定与变换后的端点共线）。而齐次坐标系的引入使仿射变换能以紧凑统一的矩阵形式表达和计算，这体现了其对仿射变换的重要性。

### 2.4. 能够区分向量和点？

当我们在坐标系 $$xOy$$ 中用 $$(a,b)$$ 定义一个向量 $$\vec{v}$$ 时，表示 $$\vec{v}=a\vec{x}+b\vec{y}$$，当我们在同样的坐标系中用 $$(a,b)$$ 表示一个点 $$p$$ 时，表示 $$p-o=a\vec{x}+b\vec{y}$$，假若写下 $$(2,1)$$，如无附加说明，不能区别出它是向量还是点。将点的表示重写为：

$$
p=[a~~b~~1]\left[
\begin{array}{c}
\vec{x}\\
\vec{y}\\
o
\end{array}
\right]
$$

将向量的表示写为:

$$
p=[a~~b~~0]\left[
\begin{array}{c}
\vec{x}\\
\vec{y}\\
o
\end{array}
\right]
$$

这样能够清晰地区分向量和点，用 3 个量表示 2 维点，这即是齐次坐标的思想。

## 3. 下一步

文章为了便于思考，讨论的都是简单的情形，还有很多问题都没有严格的证明，比如，3 维点表达是否还适用？面表达，线表达呢？还有仿射变换为什么保留了共线/面信息？更深入的了解建议找一本计算机图形学的资料，能够了解到更多关于投影空间，2D变换，3D变换，3D到2D变换的形式化表示，以及更严格的证明和表述。

参考资料：《Computer Vision: Algorithms and Applications》- Richard Szeliski - Chapter 2. Image Formation
