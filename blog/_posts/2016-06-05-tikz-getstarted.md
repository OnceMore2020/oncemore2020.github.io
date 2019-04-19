---
layout: post
title: PGF/TikZ快速上手
modified: 2016-06-05
hidden: false
feature: tikz.png
description: 闭眼绘图神器 PGF/TikZ 快速上手
tags: [Valyria Steel]
---

## 游戏名目

PGF/TikZ 是用于矢量绘图的一套语言，与 MS Visio 等所见即所得的绘图工具不同，可以使用几何/代数描述来生成图形对象。**PGF(Portable Graphics Format)** 为底层语言（指令），**TikZ(TikZ ist kein Zeichenprogramme[^name])** 是PGF的前端，即封装了PGF指令的高级语言（宏），通常我们更多地使用 TikZ 调用底层的 PGF 绘图命令。PGF/TikZ 的作者是 [Till Tantau](http://www.tcs.uni-luebeck.de/mitarbeiter/tantau/)，最初 Till Tantau 为了准备博士答辩的 slides，开发了 [Beamer](https://zh.wikipedia.org/zh/Beamer_(LaTeX))，在CTAN上流行开来后从 Beamer 项目中分离出了 PGF 作为一个独立的宏包用于绘图。TikZ 在 PGF 1.10 版本中作为其前端公之于众。

[^name]: "TikZ is not a drawing program"

PGF/TikZ 的一个可行的替代是 [PSTricks](https://en.wikipedia.org/wiki/PSTricks)，其优点是绘制曲线的命令更强，但是兼容性不如 TikZ。

## 基础入门

在开始之前，确保已经安装了较新的 $$\TeX$$ 发行版，如 [TexLive](https://www.tug.org/texlive/) 或 [MikTeX](http://miktex.org/)。

### 使用宏包

在序言部分使用 `\usepackage{tikz}` 来引入宏包，TikZ 图形的环境为

```tex
\begin{tikzpicture}
code
\end{tikzpicture}
```

`code` 部分为目标图形的几何和代数描述（TikZ语法），`tikzpicture` 环境还可以嵌套到 `figure` 环境中。

另外一种简写方式是使用`\tikz code`，`code`为绘图命令。

### 绘制直线

TikZ 默认的度量单位为厘米(cm)，语句中出现的数值一般是几何度量。如要绘制一条直线，使用 `\draw` 命令，并给出起点和终点，以 `--` 连接。如绘制一条连接 $$(0,0)$$ 和 $$(1,2)$$ 点的直线：

```tex
\begin{tikzpicture}
\draw (0,0) -- (1,2);
\end{tikzpicture}
```

![single_line]({{ site.qnurl }}/media/tikz-getstarted/single_line.png){:.img-fluid}

也可以顺序地连接多个点绘制折线或闭合多边形：

```tex
\begin{tikzpicture}
\draw (-1,0) -- (0,1) -- (1,0) -- (0,-1) -- (-1,0);
%\draw (-1,0) -- (0,1) -- (1,0) -- (0,-1) -- cycle;
\end{tikzpicture}
```

![multi_line]({{ site.qnurl }}/media/tikz-getstarted/multi_line.png){:.img-fluid}

也可以在最后使用 `cycle` 避免重复输入起点。

句末的 `;` 表示一条语句的结束，可以放置多条语句在 `tikzpicture` 环境中，如重叠上面两条语句

```tex
\begin{tikzpicture}
\draw (-1,0) -- (0,1) -- (1,0) -- (0,-1) -- (-1,0);
\draw (0,0) -- (1,2);
\end{tikzpicture}
```

![multi_stats]({{ site.qnurl }}/media/tikz-getstarted/multi_stats.png){:.img-fluid}


### 网格

使用 `grid` 放在两个点之间，可以在正方形中绘制一个网格，如

```tex
\begin{tikzpicture}
\draw (-1,0) -- (0,1) -- (1,0) -- (0,-1) -- (-1,0);
\draw [help lines] (-2,-2) grid (2,2);
\end{tikzpicture}
```

![multi_stats]({{ site.qnurl }}/media/tikz-getstarted/help_grid.png){:.img-fluid}

其中 `help lines` 选项表示绘制的网格为辅助线，会变淡显示。

### 缩放图形

在使用 `tikzpicture` 环境的时候可以加上 `scale=` 选项来设置图形的缩放

```tex
\begin{tikzpicture}[scale=1]
\draw (-1,0) -- (0,1) -- (1,0) -- (0,-1) -- (-1,0);
\end{tikzpicture}
\begin{tikzpicture}[scale=3]
\draw (-1,0) -- (0,1) -- (1,0) -- (0,-1) -- (-1,0);
\end{tikzpicture}
```

![scale]({{ site.qnurl }}/media/tikz-getstarted/scale.png){:.img-fluid}

还可以使用 `xscale=` 和 `yscale=` 选项分别对X轴和Y轴进行缩放。

### 线型

给直线绘制语句添加不同的选项，可以控制线型。如添加 **箭头**：

```tex
\begin{tikzpicture}
\draw [->] (0,0) -- (4,0);
\draw [<-] (0, -2) -- (4,-2);
\draw [|->] (0,-4) -- (4,-4);
\draw [<->] (-1,1) -- (-1,-5) -- (5,-5);
\end{tikzpicture}
```

![arrow]({{ site.qnurl }}/media/tikz-getstarted/arrow.png){:.img-fluid}

**控制线宽**:

```tex
\begin{tikzpicture}
\draw [very thin, ->] (0,0) -- (4,0);
\draw [thin, ->] (0,-1) -- (4, -1);
\draw [semithick, ->] (0,-2) -- (4,-2);
\draw [thick, ->] (0,-3) -- (4,-3);
\draw [very thick, ->] (0,-4) -- (4,-4);
\draw [ultra thick, ->] (0,-5) -- (4,-5);
\draw [line width=1cm, ->] (0,-6) -- (4,-6);
\end{tikzpicture}
```

注意到多个选项之间用 `,` 隔开。

![linewidth]({{ site.qnurl }}/media/tikz-getstarted/line_width.png){:.img-fluid}

**虚线和点划线**：

```tex
\begin{tikzpicture}
\draw [dashed, ultra thick] (0,1) -- (2,1);
\draw [dashed] (0, 0.5) -- (2,0.5);
\draw [dotted] (0,0) -- (2,0);
\end{tikzpicture}
```

![dash_dot]({{ site.qnurl }}/media/tikz-getstarted/dash_dot.png){:.img-fluid}

除了 `dashed` 和 `dotted`，可选的线型还包括 `densely dotted`、`loosely dotted`、`densely dashed` 和 `loosely dashed`。

**颜色**：

```tex
\Huge red~\begin{tikzpicture}\draw [red, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge green~\begin{tikzpicture}\draw [green, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge blue~\begin{tikzpicture}\draw [blue, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge cyan~\begin{tikzpicture}\draw [cyan, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge magenta~\begin{tikzpicture}\draw [magenta, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge yellow~\begin{tikzpicture}\draw [yellow, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge black~\begin{tikzpicture}\draw [black, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge gray~\begin{tikzpicture}\draw [gray, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge darkgray~\begin{tikzpicture}\draw [darkgray, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge lightgray~\begin{tikzpicture}\draw [lightgray, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge brown~\begin{tikzpicture}\draw [brown, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge lime~\begin{tikzpicture}\draw [lime, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge olive~\begin{tikzpicture}\draw [olive, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge orange~\begin{tikzpicture}\draw [orange, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge pink~\begin{tikzpicture}\draw [pink, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge purple~\begin{tikzpicture}\draw [purple, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge teal~\begin{tikzpicture}\draw [teal, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge violet~\begin{tikzpicture}\draw [violet, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
\Huge white~\begin{tikzpicture}\draw [white, line width=0.5cm] (0,0) -- (1,0);\end{tikzpicture}
```

![color]({{ site.qnurl }}/media/tikz-getstarted/color.png){:.img-fluid}

**圆角**:

```tex
\begin{tikzpicture}
\draw [rounded corners] (0,0) rectangle (4,4);
\end{tikzpicture}
```

![rounded]({{ site.qnurl }}/media/tikz-getstarted/rounded.png){:.img-fluid}

### 更多形状

除了直线外，还可以绘制矩形、椭圆、圆、弧等形状：

```tex
\begin{tikzpicture}
\draw [blue] (0,0) rectangle (4,4);
\draw [red, ultra thick] (2,2) circle [radius=2];
\draw (2,2) ellipse (3 and 5);
\draw [green] (4,4) arc [radius=4, start angle=45, end angle= 120];
\end{tikzpicture}
```

![shapes]({{ site.qnurl }}/media/tikz-getstarted/shapes.png){:.img-fluid}

还可以绘制两点之间的曲线

```tex
\begin{tikzpicture}
\draw[very thick] (0,0) to [out=90,in=195] (2,1.5);
\end{tikzpicture}
```

使用 `to` 替换 `--`，`out` 和 `in` 分别表示出射角和入射角。

![curve]({{ site.qnurl }}/media/tikz-getstarted/curve.png){:.img-fluid}

### 绘制函数

除了给定确定的点来绘制线条外，还可以直接给出一个函数，绘制出函数在指定的域内的图像：

```tex
\begin{tikzpicture}
\draw [help lines, <->] (0,5) -- (0,0) -- (5,0);
\draw[ultra thick, domain=0:1.5] plot (\x, {0.025+\x+\x*\x});
\draw[ultra thick, domain=0:2*pi] plot (\x, {sin(\x r)});
\draw[ultra thick, domain=0:5] plot (\x, {floor(\x)});
\end{tikzpicture}
```

![func]({{ site.qnurl }}/media/tikz-getstarted/func.png){:.img-fluid}

注意到使用了 `plot` 语法，函数使用 `(\x, {function})` 语法，支持的常用函数包括 `factorial(\x)`、`sqrt(\x)`、`pow(\x, y)`、`exp(\x)`、`ln(\x)`、`log10(\x)`、`log2(\x)`、`abs(\x)`、`mod(\x,y)`、`round(\x)`、`floor(\x)`、`ceil(\x)`、`sin(\x)`、`cos(\x)`、`tan(\x)`、`min(\x,y)`、`max(\x,y)`、`rnd`，以及两个重要的常数 `e` 和 `pi`。注意到三角函数的参数有弧度和度两种方式，在参数后面加一个 `r` 表示使用弧度。

### 填充

使用`fill`语法可以填充任意闭合的路径。

```tex
\begin{tikzpicture}
\draw [fill=red,ultra thick] (0,0) rectangle (2,2);
\draw [fill=red,ultra thick,red] (3,0) rectangle (5,2);
\draw [blue, fill=blue] (6,0) -- (6,2) -- (8,0) -- (6,0);
\draw [fill] (2,-2) circle [radius=0.5];
\draw [fill=orange] (9,0) rectangle (11,1);
\draw [fill=white] (9,0.25) rectangle (10,1.5);
\draw [ultra thick, fill=purple] (5,-2) to [out=87,in=150] (7,-1) -- (7,-1.5) -- (5,-2);
\end{tikzpicture}
```

![fill]({{ site.qnurl }}/media/tikz-getstarted/fill.png){:.img-fluid}

### 标注

使用 `node` 可以在指定点区域加上标注文字，可以使用 `below`、`above`、`left`、`right` 及其组合来控制相对位置。标注的文字允许使用 $$\LaTeX$$ 语法来控制文字样式。

```tex
\begin{tikzpicture}
\draw [thick, <->] (0,4) -- (0,0) -- (4,0);
\draw[fill] (2,3) circle [radius=0.05];
\node [below] at (2,3) {below};
\node [above] at (2,3) {above};
\node [left] at (2,3) {left};
\node [right] at (2,3) {right};

\draw[fill] (2,1) circle [radius=0.05];
\node [below right, red] at (2,1) {below right};
\node [above left, green] at (2,1) {above left};
\node [below left, purple] at (2,1) {below left};
\node [above right, magenta] at (2,1) {above right};

\node [below right] at (4,0) {$\mathrm{x}$};
\node [left] at (0,4) {$\mathrm{y}$};
\end{tikzpicture}
```

![label]({{ site.qnurl }}/media/tikz-getstarted/label.png){:.img-fluid}

## 进阶使用

### 样式定义

TikZ 可以对单个`tikzpicture`环境定义样式

```tex
\begin{tikzpicture}[
    myline/.style={line width=2pt},
    myblueline/.style={myline, blue}]
\draw [myline] (0,0) -- (4,0);
\draw [myblueline] (0,1) -- (4,1);
\end{tikzpicture}
```

或者使用`tikzset`定义全局样式，如

```tex
\tikzset{
    myline/.style={line width=2pt},
    myblueline/.style={myline, blue}
}
\begin{tikzpicture}
\draw [myline] (0,0) -- (4,0);
\draw [myblueline] (0,1) -- (4,1);
\end{tikzpicture}
```

![style]({{ site.qnurl }}/media/tikz-getstarted/style.png){:.img-fluid}


### 几何变换

除了使用 `scale` 控制尺寸缩放外，TikZ还支持 **平移**(`shift`)、**倾斜**(`slant`)、**旋转**(`rotate`)、**旋转**(`rotate around`) 等几何变换。

```tex
\begin{tikzpicture}
\draw (0,0) rectangle (2,2);
\draw[shift={(3,0)},scale=1.5] (0,0) rectangle (2,2);
\draw[xshift=70pt,xscale=1.5] (0,0) rectangle (2,2);
\draw[xshift=125pt,rotate=45] (0,0) rectangle (2,2);
\draw[xshift=140pt,xslant=1] (0,0) rectangle (2,2);
\draw[xshift=175pt,rotate around={45:(2,2)}] (0,0) rectangle (2,2);
\end{tikzpicture}
```

![transform]({{ site.qnurl }}/media/tikz-getstarted/transform.png){:.img-fluid}


## 一点思考

做了这么多笔记，还是感觉不如 MS Visio 画流程图、结构框图那样顺手。对于函数绘制，还是感觉 [matplotlib](http://matplotlib.org/) 功能更完备一些，操作上也更可控。不过说到这里，不知不觉又走到了 **排版与编程的交叉路口**，TikZ 过于受制于 $$\LaTeX$$ 的 **标记语言属性**，而现在的样式控制早已引入了一般编程语言的特性（变量、继承等）。所以到底如何，才能绘制好一张图？

## 参考资料

> If it is not in these notes, it is most probably somewhere in the manual.

1. [TikZ and PGF Manual](http://mirror.lzu.edu.cn/CTAN/graphics/pgf/base/doc/pgfmanual.pdf)
2. [CTAN - PGF](http://www.ctan.org/tex-archive/graphics/pgf/)
4. [A very minimal introduction to TikZ](http://cremeronline.com/LaTeX/minimaltikz.pdf)
3. [PGF/TikZ - Wikipedia](https://en.wikipedia.org/wiki/PGF/TikZ)
