---
layout: post
title: OpenCV2 基础操作
modified: 2017-03-29
description: 关于 OpenCV 运算库的一些基础知识。
feature: true
tags: [CV]
---

快速了解 OpenCV2 基础操作，对于系统地开始阅读和学习文档有很大帮助。

## 数据结构

将获取的图像转码到数字设备时，采用一张数表(矩阵)来存储图像的每一像素强度[^stdmat]。如下图所示，每个位置的数字表示当前位置的像素强度。

![Mat Demo]({{ site.qnurl }}/media/opencv2basic/mat.jpg){:.img-responsive .img-rounded}

[^stdmat]: OpenCV2 的 `cv::Mat` 支持标准 I/O，可读入一副图像到 `image` 变量，然后使用 `std::cout << image << endl;` 一探究竟。

具体如何存储和获取这些像素值取决于具体需求，但是最终计算机内的所有的图像都是用各种矩阵来描述的。OpenCV2 采用 `cv::Mat` 类来存储图像，OpenCV2 提供的 C++ API 中定义的类和函数都定义在命名空间 `cv` 中，可用如下方式声明:

```cpp
using namespace cv;
```

创建一个变量来存储图像：

```cpp
cv::Mat image;
```

## 存储方法

存储像素值来表示图像涉及到 **色彩空间** 和 **数据类型**。**色彩空间** 是使用一组值来表示图像色彩的数学模型，最简单的是 **灰度值图像**，处理的颜色都是黑白的。对于彩色图像，可将每一个像素分解为若干个色彩成分通道，最流行的方式是 **RGB**，因为人眼就是这样构建色彩世界的，三基色为红，绿，蓝。有时会采用其它色彩空间，其对比如下：

* RGB：最常见的色彩系统，用红绿蓝三色光的比例叠加来表示颜色，与人眼视觉系统原理类似，通常的显示系统也有采用这种色彩系统；
* HSV/HLS：将色彩分解为色调、饱和度、强度/亮度等元素，这种描述更自然直观，艺术家常用的色彩空间；
* CMYK : 使用青、品红、黄、黑四种油墨叠加在白色纸张上来体现彩色图像，常见于打印设备

现实世界的像素强度值是连续的，而计算机只能直接对离散数据进行处理，因此需要将像素强度进行 **量化** 为离散数值，用相应 **数据类型** 存储，常采用与 `char` 数据类型相同的数据空间：1 字节或 8 比特，对应十进制为无符号(0~255)/带符号(-127~+127)。可以采用更大的数据类型来存储，会带来图像存储空间的增长。

## 历史问题

OpenCV 诞生于 2001 年，最初版本运算库是基于 C 接口设计的，采用的 C 数据结构 `IplImage` 来存储图像，此方法引入了所有的C缺陷，其中最主要的问题是手动管理内存，要求用户负责内存的分配和释放，这种情况在较小型的程序设计中影响并不大，当设计任务增长时用户可能会花
更多的时间来处理内存管理问题。如采用 C 接口来读入一个图像：

```cpp
IplImage* iplImage = cvLoadImage("c:\\img.jpg");
```

当不再使用变量时需要手动释放内存空间:

```cpp
cvReleaseImage(&iplImage);
```

OpenCV2 引入了 C++ 对象 `cv::Mat`，当然也包括 C++ 围绕着 **类(class)** 的设计模式的一种新概念：**自动内存管理**。

## 引用计数

`Mat` 从类的角度可分为两部分：**矩阵头**（矩阵大小、存储方法、初始地址）和一个指向数据单元的 **指针**。矩阵头的大小是固定的，但是矩阵的大小会随着存储图像的大小而改变。来看看 `Mat` 的部分类定义：

```cpp
class CV_EXPORTS Mat
{
public:
    // ... a lot of methods ...
    ...

    /*! includes several bit-fields:
         - the magic signature
         - continuity flag
         - depth
         - number of channels
     */
    int flags;
    //! the array dimensionality, >= 2
    int dims;
    //! the number of rows and columns or (-1, -1) when the array has more than 2 dimensions
    int rows, cols;
    //! pointer to the data
    uchar* data;

    //! pointer to the reference counter;
    // when array points to user-allocated data, the pointer is NULL
    int* refcount;

    // other members
    ...
};
```

当设定一个处理任务时，系统输入图像需要通过 `Mat` 传递，图像处理的计算量是庞大的，在传递图像时我们不能随意地创建不必要的图像拷贝，因为这会影响程序的效率。为了解决这个问题，OpenCV 采用 **引用计数系统（Reference Counting System）**，主要思想是每个矩阵对象采用各自的矩阵头，但是矩阵的数据存储单元能被多个对象共享。这样在拷贝操作时只需要拷贝矩阵头和指针即可，不会拷贝存储单元数据。

```cpp
Mat A, C;   //只创建矩阵头
A = imread(argv[1], CV_LOAD_IMAGE_COLOR);   //分配存储单元
Mat B(A);   //拷贝操作(通过构造函数)
C = A;  //赋值操作
```

以上示例代码中`A`、`B`、`C`最终都只指向同一个矩阵数据，但是它们的矩阵头不一样，所以修改其中任何一个对象都会影响其它对象。实际应用中常采用这种方式，不同的对象共享一个图像数据存储空间，甚至共享图像存储空间的一部分，如创建 **ROI**（Region of Interest）

```cpp
Mat D(A,Rect(10,10,100,100)); //矩形ROI
Mat E = A(Range:all(),Range(1,3));  //行列范围ROI
```

返回到内存管理问题上，当矩阵数据被多个对象共享时，谁负责释放它？答案是最后一个引用它的对象，这就要用到引用计数机制，`Mat` 类内设置了一个指向引用计数器的指针 `refcount`,当一个 `Mat` 对象的头部被拷贝时，引用计数器会自增，当一个 `Mat` 对象头部被释放时，引用计数器会自减，当计数器清零时矩阵数据被释放。共享数据存储空间的拷贝称为 **软拷贝**。

另外OpenCV提供了 `clone()` 和 `copyTo()` 方法用于 **硬拷贝**，即复制图像的同时复制数据矩阵。

```cpp
Mat F = A.clone();  //硬拷贝
Mat G;
A.copyTo(G);    //硬拷贝
```

## 类型转换

同时，OpenCV2 提供了将 `IplImage` 类型转换为 `cv::Mat` 类的方法：

```cpp
cv::Mat image4(iplImage,false);
```

其中默认参数`false`表示软拷贝，设置为`true`表示硬拷贝。这时特别需要注意软拷贝时内存管理的问题。OpenCV2同样提供了对C接口的数据结构进行引用计数的指针类`Ptr<IplImage>`：

```cpp
cv::Ptr<IplImage> iplImage = cvLoadImage("c:\\img.jpg");
```

这可以规避C API的手动内存管理，但是应该尽量使用OpenCV2提供的C++ API `cv::Mat`类。

## 注意事项

引用计数规则允许函数返回`Mat`类型,例如：

```cpp
cv::Mat function() {
    // create image
    cv::Mat ima(240,320,CV_8U,cv::Scalar(100));
    // return it
    return ima;
}

int main(void)
{
    //get a gray-level image
    cv::Mat gray =function();
}
```

在主函数内调用函数`function()`后，`gray`存储了返回的图像，虽然在`function()`执行完毕后局部变量`ima`会被释放，但是仍存在`gray`对数据空间的引用，故图像对应的内存空间并不会被释放。

然而，应当注意**不能**直接返回`Mat`类型的类属性，如下典型错误示例：


```cpp
class Test {
    //image attribute
    cv::Mat ima;

    public:
        //constructor creating a gray-level image
        Test()  :   ima(240, 320, CV_8U, cv::Scalar(100)) {}
        //method return a class attribute, not a good idea...
        cv::Mat method()    {return ima;}
}
```

如果调用类方法`method()`进行赋值操作，变量将创建类属性`ima`的软拷贝，如果这个变量在之后被修改，类属性同样会被修改，从而造成类行为的变化。为了避免这个问题，**总是**创建类属性的硬拷贝。不难发现，这是由于**类**和**函数**的作用机制上的区别造成的。

## 图像I/O

OpenCV将包括图像输入/存储/输出等功能封装进`core`模块中，使用前需要包含头文件：

```cpp
#include <opencv2/core/core.hpp>
```

### 构造函数

首先看看一种常见的`Mat()`构造函数[^matcons]：

[^matcons]:完整的构造函数列表参考文档[Basic Structures](http://docs.opencv.org/modules/core/doc/basic_structures.html?highlight=mat#Mat::Mat())部分。

```cpp
Mat::Mat(int rows, int cols, int type, const Scalar& s)
```

很容易看出参数意义：

* rows: 2维图像矩阵行数
* cols: 2维图像矩阵列数
* type: 矩阵类型
* Scalar& s: 初始化参数

OpenCV2在创建`cv::Mat`对象时可指定图像尺寸以及存储方式，如：

```cpp
cv::Mat ima(240,320,CV_8UC3,cv::Scalar(100));
```

其中前两个参数表示尺寸，`CV_8U`中`8`表示采用8位来存储一个像素强度，也可指定为`16`甚至是`32`，`U`表示用无符号类型，也可以使用带符号类型`S`或浮点类型`F`(`32F`或`64F`)，`C3`表示采用三个通道(处理彩色图像)。总结起来，矩阵类型特定的语法规则如下：


```cpp
CV_[The Number of bite per item][Signed or Unsigned][Type Profix]C[The Channel number]
```

需要注意，Mat作为图像容器表现优秀，同时，当其作为一个通用矩阵类时，也可用于创建和处理多维矩阵。但更多的时候，我们只需要采用`Mat varname`来创建一个图像容器。

### 输入图像

OpenCV采用`imread()`函数来输入图像。其C++接口如下：

```C++
Mat imread(const string& filename, int flags=1 )
```

`filename`为文件名及其路径，可使用绝对路径和相对路径，视应用场景而定。`flags`指定加载图像的色彩方式：

* CV_LOAD_IMAGE_ANYDEPTH : 输入图像采用16位/32位编码是返回16位/32位编码方式，否则转换为8位编码
* CV_LOAD_IMAGE_COLOR : 默认载入彩色图像
* CV_LOAD_IMAGE_GRAYSCALE ： 默认转换为灰度图像
* 大于0 : 返回3通道图像
* 等于0 : 返回灰度图像
* 小于0 : 保留原始图像通道数

从前面`Mat`类定义里可以找到成员变量`data`，当成功读取图像时，它指向数据空间地址，当读取错误时，对其赋值`0`，于是可以采用下面的方法验证图像是否被正确读入并进行相应处理：

```cpp
if (!image.data) {
    // handle the failure
}
```

更多输入图像的细节包括支持的图像格式等请参考[imread文档](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html?highlight=imread#imread)。

### 输出图像

OpenCV采用`imwrite()`来输出图像到文件，其接口如下：


```cpp
bool imwrite(const string& filename, InputArray img, const vector<int>& params=vector<int>() )
```

除了需要指定输出文件名`filename`和需要保存的图像矩阵`img`外，`params`根据输出文件名后缀类型决定输出文件的质量和压缩比等，详细请参考[imwrite文档](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html?highlight=imwrite#imwrite)。

### 可视化

将读入的图像显示到屏幕虽然对计算机没什么用，但是方便编程人员直观地评估结果和调试。OpenCV将可视化功能封装在`highgui`模块中，使用时需要包含头文件：


```cpp
#include <opencv2/highgui/highgui.hpp>
```

OpenCV显示图像前需要采用`namedWindow()`创建窗口。`namedWindow()`的接口如下：


```cpp
void namedWindow(const string& winname, int flags=WINDOW_AUTOSIZE )
```

`winname`为窗口ID，`flags`支持`WINDOW_NORMAL`(可缩放)，`WINDOW_AUTOSIZE`(自适应)，`WINDOW_OPENGL`(OpenGL)。

创建了窗口后，可采用`imshow()`函数将图像输出到显示器，使用方式如下：


```cpp
void imshow(const string& winname, InputArray mat)
```

一个完整的窗口创建和图像显示示例如下：

```cpp
cv::namedWindow("Output Image");
cv::imshow("Output Image", result);
```

常用于管理窗口显示的函数是`int waitKey(int delay=0)`，当传递参数大于零时，等待指定毫秒后关闭窗口，若小于等于零，一直保持窗口，返回值为监听到的按键码。在激活窗口后使用`waitKey(0);`可使窗口在监听到回车按下时关闭。
