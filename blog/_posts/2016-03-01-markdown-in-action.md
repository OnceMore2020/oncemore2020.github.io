---
layout: post
title: "Markdown快速上手"
modified: 2016-03-01
feature: markdown.png
description: Markdown 是目前很流行的轻量级标记语言，其使用方便，上手容易。本文介绍快速上手 Markdown 的方法。
tags: [Valyria Steel]
---
Markdown 是一种[**轻量级标记语言**](http://zh.wikipedia.org/wiki/%E8%BD%BB%E9%87%8F%E7%BA%A7%E6%A0%87%E8%AE%B0%E8%AF%AD%E8%A8%80)，由 [**John Gruber**](http://en.wikipedia.org/wiki/John_Gruber) 和 [**Aaron Swartz**](http://en.wikipedia.org/wiki/Aaron_Swartz)最初设计。Markdown 在 MS Office 类文本处理器和 TeX 排版系统(算是两个派系)之间取了一个折中，同时保留了**易读性**和**易写性**。本文尝试记录快速上手 Markdown 的过程。

## 文本编辑器
推荐使用在线Markdown编辑器 [**StackEdit**](https://stackedit.io/)，推荐的原因包括：

* WYSIWYG，实时预览，适合上手
* 基于Web，跨平台
* 界面友好
* 自带一份语法教程

当然也可以使用熟手的任意一款代码编辑器用于编辑 Markdown，比如 [Atom](https://atom.io)，使用 `Ctrl+Shift+M` 即可实现预览。

Markdown 在预览的时候，本质上是转换成了带格式的 html 文档。

## 基本语法 {#start}

### 段落
一个段落是不包含空行的文本片段，当出现一个空行时，表示空行下面的是新段落。

### 转义字符
Markdown 语法自带一些关键字（主要是符号），对应于不同的格式。要在预览时显示这些符号，需要用到转义字符。和一般的编程语言一样，反斜杠 `\ ` 后面加关键字符号表示转义字符，主要包括下面这些标号

{:.table .table-bordered .table-hover .table-striped}
|标号|含义|
|:---|:---|
|\   |反斜线|
|\`   |反引号|
|*   |星号|
|_   |底线|
|{}  |花括号|
|[]  |方括号|
|()  |括弧|
|#   |井字号|
|+   |加号|
|-   |减号|
|.   |英文句点|
|!   |惊叹号|

### 标题
Markdown 最流行的标题分级方式是采用`#`符号(**类Atx形式**)，最高可分级到六级标题。

```
# 一级标题

## 二级标题

### 三级标题

#### 四级标题

##### 五级标题

###### 六级标题
```

---

![header-atx]({{ site.qnurl }}/media/markdown-in-action/header.PNG){:.img-fluid}

---

为了增强可读性，可在标题后面增加任意数量的`#`，但是标题分级由前面的`#`数量决定。

另外一种方法是**类Setext形式**，用`=`表示一级标题，`-`表示二级标题。

```
一级标题
========

二级标题
--------
```

---

![header-atx]({{ site.qnurl }}/media/markdown-in-action/header-setext.PNG){:.img-fluid}

---

注意`=`和`-`的数量是任意的，一般的习惯是写到与标题长度对齐。


### 引用
Markdown采用`>`符号标记引用的内容，引用允许采用嵌套，这时需要采用`>>`，`>`的数量表示
嵌套的层次。同时，引用内允许嵌入其他 Markdown 语法。

```
> 张三丰道
>
>> 用意不用力，太极圆转，无使断绝。
>
> 当得机得势，令对手其根自断。一招一式，务须节节贯串，如长江大河，滔滔不绝。
> 他适才见张无忌临敌使招，已颇得太极三昧，只是他原来武功太强，拳招中棱角分
> 明，未能体会太极拳那“圆转不断”之意。
```

---

> 张三丰道
>
> > 用意不用力，太极圆转，无使断绝。
>
> 当得机得势，令对手其根自断。一招一式，务须节节贯串，如长江大河，滔滔不绝。
> 他适才见张无忌临敌使招，已颇得太极三昧，只是他原来武功太强，拳招中棱角分
> 明，未能体会太极拳那“圆转不断”之意。

---

### 列表
支持无序列表和有序列表。无序列表使用`*`、`+`、`-`进行标记，他们的作用是等效的。

```
* 苹果
+ 番茄
- 板蓝根
```

---

* 苹果
+ 番茄
- 板蓝根

---

有序列表需要使用数字标号。

```
1. 草莓
2. 黄瓜
3. 金银花
```

---

1. 草莓
2. 黄瓜
3. 金银花

---

注意，在`*`、`+`、`-`、`1.` 后面，需要有一个空格。更有趣的是，有序列表前面的数字标号实际上并不需要是正确的(也就是想看起来的样子)，这完全是给懒人设计的，比如采用：

```
9. 鬼
5. 舞
2. 日
7. 决
```
得到的是下面的效果：

---

9. 鬼
5. 舞
2. 日
7. 决

---

列表也支持较长的文本(段落)，这时只需要列表标号和段落起始之间要保留空格就好，段落换行后的行缩进与否并不重要，但是保持整齐的缩进是比较好的风格。


```
* 张无忌道：“人家高兴，你也高兴，那才是真高兴啊。”那少女
  冷笑道：“哼！我跟你说在前头，这时候我心里高兴，就不来害
  你。哪一天心中不高兴了，说不定会整治得你死不了，活不成，
  到时候你可别怪我。”
* 张无忌摇头到：“我从小给坏人整治到大，越是整治，越是硬朗。”
  那少女冷笑道：“别把话说得满了，咱们走着瞧吧。“
```

---

* 张无忌道：“人家高兴，你也高兴，那才是真高兴啊。”那少女
  冷笑道：“哼！我跟你说在前头，这时候我心里高兴，就不来害
  你。哪一天心中不高兴了，说不定会整治得你死不了，活不成，
  到时候你可别怪我。”
* 张无忌摇头到：“我从小给坏人整治到大，越是整治，越是硬朗。”
  那少女冷笑道：“别把话说得满了，咱们走着瞧吧。“

---

如果一个列表项内包含多个段落，那么每个段落开头都必须缩进,不然会出现奇怪的格式错误，比如识别不出下一项列表项。


```
* 张无忌道：“人家高兴，你也高兴，那才是真高兴啊。”

  那少女冷笑道：“哼！我跟你说在前头，这时候我心里高兴，就不来害
  你。哪一天心中不高兴了，说不定会整治得你死不了，活不成，
  到时候你可别怪我。”
* 张无忌摇头到：“我从小给坏人整治到大，越是整治，越是硬朗。”
  那少女冷笑道：“别把话说得满了，咱们走着瞧吧。“
```

---

* 张无忌道：“人家高兴，你也高兴，那才是真高兴啊。”

  那少女冷笑道：“哼！我跟你说在前头，这时候我心里高兴，就不来害
  你。哪一天心中不高兴了，说不定会整治得你死不了，活不成，
  到时候你可别怪我。”
* 张无忌摇头到：“我从小给坏人整治到大，越是整治，越是硬朗。”
  那少女冷笑道：“别把话说得满了，咱们走着瞧吧。“

---

### 分隔线
在同一行中使用三个以上的`*`,`-`,`_`来建立一个分隔线，分隔线标号之间允许出现空格。

```
***

---

___

* * *

```

### 代码块
一小段语句或是表达式可以用`` ` ``号括起来，称为 **Backtick** 风格的代码块。

```
A single backtick in a code span: `` ` ``

A backtick-delimited string in a code span: `` `foo` ``
```

---

A single backtick in a code span: `` ` ``

A backtick-delimited string in a code span: `` `foo` ``

---

若是涉及到较长的多行代码片段，简单的代码块可以采用缩进来实现。


```
下面是代码示例：

	#include<stdio.h>
	int main(void)
	{
		printf("旮那边的朋友你们好!\n");
		return 0;
	}
```

---

下面是代码示例：

		#include<stdio.h>
		int main(void)
		{
			printf("旮那边的朋友你们好!\n");
			return 0;
		}

---

[GitHub Flavored Markdown](https://help.github.com/categories/writing-on-github/) 扩展了 backtick 风格的代码块，使用三个连续的\`\`\`单独放在一行，用于包围代码块。

<pre><code>```python
#!/usr/bin/env python
# encoding: utf-8

def main():
    pass

if __name__ == '__main__':
    main()
```
</code></pre>

可指定代码的类型，这一附加功能的好处是使得代码的高亮更加容易实现。代码高亮的功能一般由转换器定义，也有一些转换器（如Jekyll）不会处理代码高亮，这时如果需要代码语法高亮功能，需要配合相应插件来使用，目前（2016-03）推荐使用 [Rouge](http://rouge.jneen.net/)。开头说了，Markdown 预览本质上是转换成了 html 文档，因此高亮代码这个功能本质上是给 html 文件外部链接了一个 CSS 文档，Rouge 转换时会给目标代码的文本加上不同的 class 属性，CSS 文档负责对不同的 class 进行样式定义。更多细节，参考：[Github Pages 更新到 Jekyll 3.0](http://oncemore2020.github.io/blog/upgrade-jekyll/)。


### 文本风格
Markdown 可以方便地实现加粗、加斜等文本风格。

使用`*`和`_`用于加斜强调，`**`或是`__`用于加粗强调

```
**滚粗**

__滚粗__

*黄药师*

_郭襄_
```

---

**滚粗**

__滚粗__

*黄药师*

_郭襄_

---

若要同时加粗加斜，在`**`中使用`_`来实现

```
**_如意金箍棒_**
```

---

**_如意金箍棒_**

---

### 链接
Markdown支持两种形式的链接标记，其一是行内式，链接文字用`[]`括起来，链接地址用`()`括起来。

```
这是我的[主页](http://oncemore2020.github.io "Title").
```

---

这是我的[主页](http://oncemore2020.github.io "Title").

---

如果链接地址需要多次使用，每一次都输入地址难免过于麻烦，这时候适合采用参考式。参考式可以把链接地址内容在文章的任何地方用一个标记来表示，然后在其它地方引用这个标记。如下面这个栗子，使用第一行的参考式时，`homepage`标号在第二行定义。

```
这是我的[主页][homepage]。
[homepage]: http://oncemore2020.github.io  "TEMPORA MUTANTUR NOS ET MUTAMUR IN ILLIS"
```

---

这是我的[主页][homepage]。

[homepage]: http://oncemore2020.github.io  "TEMPORA MUTANTUR NOS ET MUTAMUR IN ILLIS"

---

也可以省略第二个`[]`里的标记，这时会默认把链接文字就当成是标号。下面提供两种比较好的范例。

```
I get 10 times more traffic from [Google] [1] than from
[Yahoo] [2] or [MSN] [3].

  [1]: http://google.com/        "Google"
  [2]: http://search.yahoo.com/  "Yahoo Search"
  [3]: http://search.msn.com/    "MSN Search"
```
或是

```
I get 10 times more traffic from [Google][] than from
[Yahoo][] or [MSN][].

  [google]: http://google.com/        "Google"
  [yahoo]:  http://search.yahoo.com/  "Yahoo Search"
  [msn]:    http://search.msn.com/    "MSN Search"
```
都会产生下面的效果。

---

I get 10 times more traffic from [Google][] than from
[Yahoo][] or [MSN][].

  [google]: http://google.com/        "Google"
  [yahoo]:  http://search.yahoo.com/  "Yahoo Search"
  [msn]:    http://search.msn.com/    "MSN Search"

---

还有一种称为**自动链接**的方式，将地址直接放进`<>`中，支持网址和邮件地址。

```
<address@example.com>

<http://example.com/>
```

---

<address@example.com>

<http://example.com/>

---

### 图片
Markdown嵌入图片的方法和链接类似，也分为**行内式**和**参考式**。

**行内式**

```
![Vim]({{ site.qnurl }}/media/markdown-in-action/vim.png "vim logo")
```

**参考式**

```
![Vim][id]

[id]: /blog/media/markdown-in-action/vim.png "vim logo"
```

都能嵌入如下的图片。

---

![Vim][id]{:.img-fluid}

[id]: /blog/media/markdown-in-action/vim.png "vim logo"

---

图片地址可以采用网址或是本地路径。


## 扩展
下面介绍的一些语法虽然不属于 Markdown 标准语法，但通常被大多数的转换器所支持。推荐使用 [kramdown](http://kramdown.gettalong.org/) 作为转换器，其用 Ruby 实现，目前是 github Pages 钦点的转换器。

### 自定义样式
既然是转换为 html 文档，那如果能够给 html 标签加上 class 属性，就可以通过外部链接的 CSS 文件来自定义样式了。 kramdown 支持使用`{: .class}`的方式来给目标标签加上一个 class 属性。参考下面的表格语法，加上了 [Bootstrap](http://getbootstrap.com/) 的四个表格组件类。

### 表格
Markdown采用下面的语法来实现表格。无对齐格式的方法：

```
{:.table .table-bordered .table-hover .table-striped}
Item      | Value
--------- | -----
Computer  | 1600 USD
Phone     | 12 USD
Pipe      | 1 USD
```

---

{:.table .table-bordered .table-hover .table-striped}
Item      | Value
--------- | -----
Computer  | 1600 USD
Phone     | 12 USD
Pipe      | 1 USD

---

以及设置对齐的方法,`:`在若干数量的`-`左边表示左对齐，`:`在若干数量的`-`右边表示右对齐，若干数量的`-`位于两个`:`中间表示中间对齐：

```
{:.table .table-bordered .table-hover .table-striped}
| Item      |    Value | Qty  |
| :-------- | --------:| :--: |
| Computer  | 1600 USD |  5   |
| Phone     |   12 USD |  12  |
| Pipe      |    1 USD | 234  |
```

---

{:.table .table-bordered .table-hover .table-striped}
| Item      |    Value | Qty  |
| :-------- | --------:| :--: |
| Computer  | 1600 USD |  5   |
| Phone     |   12 USD |  12  |
| Pipe      |    1 USD | 234  |

---

### 脚注
kramdown 使用下面的方法来设置脚注。

```
You can create footnotes like this[^footnote].

  [^footnote]: Here is the *text* of the **footnote**.
```

---

You can create footnotes like this[^footnote].

  [^footnote]: Here is the *text* of the **footnote**.

---

### 交叉引用
在需要引用的分级标题后设置一个`{#id}`，然后在其它任何地方使用这个唯一的标识符来进行引用以方便文章内的跳转。比如在本文源文件的**入门-基本语法**后面进行标识。

```
#入门-基本语法 {#start}
```
然后进行引用：

```
[入门-基本语法](#start)
```
点击下面的链接会跳转到相应的部分。

---

[入门-基本语法](#start)

---

除了手动设置标题标识符之外，kramdown还支持自动生成各章节的标识符，通常是这一节的标题。


### 自动生成目录
kramdown规定`toc`为目录的引用名，将其放置在一个列表项目中会自动替换为当前文章的目录结构。

```
# 文章目录
{:.no_toc}

* 这段文字会被替换为文章目录，但目录内不包括 "文章目录" 自身
{:toc}
```

# 文章目录
{:.no_toc}

* 这段文字会被替换为文章目录，但目录内不包括 "文章目录" 自身
{:toc}

`{:.no_toc}`告诉kramdown不要将文章目录包含到自身之中。


### 数学环境-Mathjax
Mathjax 支持在 html 文档中显示 $$\LaTeX$$ 语法 （AMS）的数学公式，要使用MathJax，需要在html的`script`段中添加如下代码，开启通过动态加载MathJax CDN来实现转换。

```
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
```

配置好MathJax以后，数学环境需要使用`$$`来包围，支持LaTeX ams宏包中的数学符号。
例如：

```
$$
\begin{align*}
  & \phi(x,y) = \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right)
  = \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j) = \\
  & (x_1, \ldots, x_n) \left( \begin{array}{ccc}
      \phi(e_1, e_1) & \cdots & \phi(e_1, e_n) \\
      \vdots & \ddots & \vdots \\
      \phi(e_n, e_1) & \cdots & \phi(e_n, e_n)
    \end{array} \right)
  \left( \begin{array}{c}
      y_1 \\
      \vdots \\
      y_n
    \end{array} \right)
\end{align*}
$$
```

将得到如下数学环境：

---

$$
\begin{align*}
  & \phi(x,y) = \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right)
  = \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j) = \\
  & (x_1, \ldots, x_n) \left( \begin{array}{ccc}
      \phi(e_1, e_1) & \cdots & \phi(e_1, e_n) \\
      \vdots & \ddots & \vdots \\
      \phi(e_n, e_1) & \cdots & \phi(e_n, e_n)
    \end{array} \right)
  \left( \begin{array}{c}
      y_1 \\
      \vdots \\
      y_n
    \end{array} \right)
\end{align*}
$$

---

## 参考文章

1. [Markdown Syntax](https://daringfireball.net/projects/markdown/syntax#backslash)
2. [Github - Basic writing and formatting syntax](https://help.github.com/articles/basic-writing-and-formatting-syntax/)
3. [kramdown Syntax](http://kramdown.gettalong.org/syntax.html)

---

