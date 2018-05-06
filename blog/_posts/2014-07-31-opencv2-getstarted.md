---
layout: post
title: 快速上手 OpenCV
modified: 2014-07-31
description: 介绍如何使用 CMake 快速配置 OpenCV 工程。
feature: false
tags: [CV]
---

安装好 OpenCV2 后，如何快速开始使用或学习 OpenCV 是首要问题。如何编译一个使用了 OpenCV 运算库的程序呢？有下面几种不同的思路：

1. 使用 gcc 进行编译（复杂度高）;
2. 使用 IDE 配置头文件和库文件路径，（复杂度适中）;
3. 使用构建工具 CMake （复杂度低）。

本文介绍使用 CMake 快速配置项目的方法。开始之前，建议参考 [编译安装OpenCV2](http://oncemore2020.github.io/blog/opencv2compile) 编译 OpenCV 并安装 CMake 等构建工具。

## 工作目录

使用CMake构建工程，工作目录应该具有如下结构：

```bash
    |-CMakeLists.txt
    |-main.cpp
```

其中 `CMakeLists.txt` 是 CMake 配置文件，`main.cpp` 是源程序文件。

## CMake 设定

这里给出一种简单可复制的工程设定文件，在应用到其它源程序时只需要进行少量修改。

```bash
cmake_minimum_required(VERSION 2.8)
project( main )
find_package( OpenCV REQUIRED )
add_executable( main main.cpp )
target_link_libraries( main ${OpenCV_LIBS} )
```

设置文件规定了工程文件名、程序包依赖、源文件、目标文件、以及链接库对象和库路径。

## 示例

采用一个简单的程序进行演示，程序用到`core.hpp` 和 `highgui.hpp` 头文件，实现读入一个图像，进行水平翻转后输出到文件。代码如下：

```bash
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main(){
    Mat image = imread("test.jpg");
    if ( !image.data ){
        cout << "No image LOADED!" << endl;
    }
    namedWindow("Original Image");
    cout << "size: " << image.size().height << " , "
        << image.size().width << endl;
    imshow("Original Image", image);
    Mat result;
    flip(image, result, 1);
    namedWindow("Output Image");
    imshow("Output Image", result);
    waitKey(0);
    imwrite("output.jpg", result);
    return 0;
}
```

### 构建

在工作目录里命令行输入以下指令进行构建：

```Bash
cmake .
make
```

构建过程终端输出如图

![CLI codes]({{ site.qnurl }}/media/opencv2-getstarted/code.png){:.img-responsive .img-rounded}

构建完成后则可以运行`./test`程序

![CLI codes]({{ site.qnurl }}/media/opencv2-getstarted/out.png){:.img-responsive .img-rounded}

## 总结

在学习 OpenCV2 的过程中，往往是模块化地了解各个库内的接口，这样单一源程序即可完成，采用上面的设定，可以快速的尝试模块接口。更多关于 CMake 的细节，参考 [CMake指南](http://www.cmake.org/cmake/help/cmake_tutorial.html)。
