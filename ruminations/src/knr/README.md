#《The C Programming Language - 2nd Edition》

![cover](https://omjqdrs7d.qnssl.com/knr/knr.png)


Brian W. Kernighan 先生和 Dennis M. Ritchie 先生的著作。此笔记以课后习题为主线。

## 编译和运行环境:
* gcc 5.3.0
* Archlinux

## 读引言

C语言适当地保持了语言的规模。
> Although the absence of some of these features may seem like a grave deficiency ("You mean I have to call a function to compare two character strings?"), keeping the language down to modest size has real benefits.

C语言包含的特性：

* 字符、整型、浮点数等基本类型以及指针、数组、结构和联合派生等数据类型
* 基本的控制流接口：语句组、条件判断(`if-else`)、多路选择(`switch`)、循环语句(`while`、`for`)、跳出循环(`break`)
* 函数、递归
* 预编译器

C语言**不**包含的特性：

* 直接处理字符串、集合、列表或数组等复合对象的操作
* 存储器分配工具
* 堆和无用内存回收工具
* 输入/输出
* 并行、同步和协程

## 此话怎讲？
这是第n次拿起K&R了，争取能从头读到尾吧。

```bash
$ date
2016年 03月 01日 星期二 21:01:07 CST
```
