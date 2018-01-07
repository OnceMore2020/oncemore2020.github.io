---
layout: post
title: OpenCV2 像素访问研究
modified: 2017-03-29
feature: true
description: OpenCV 的图像对象如何访问其像素值？可行的方法？哪种效率更高？
tags: [CV]
---

进行空域处理的第一步就是要访问图像某个位置的像素值，OpenCV2提供了几种访问图像像素的方法，主要包括**随机访问稀疏位置集合**和**遍历图像大面积连续区域**(甚至整幅图像)像素两类模式，本文对几种常用的方法进行总结。

**GOALS**:

* 随机访问像素
   * 实例：椒盐噪声
   * `.at`方法
* 遍历区域像素
   * 实例：色彩空间压缩
   * 采用指针访问
   * 采用迭代器访问
* 哪种方法更高效？

**Reference**:

*《OpenCV 2 Computer Vision Application Programming Cookbook》- Chapter 2*

## 1.随机访问

在某些应用场景，只需要对稀疏的点进行访问，在这种情况下采用随机访问方法效率更高。

### 1.1 实例:椒盐噪声

图像中的**椒盐噪声**通常是由通信过程中的错误(信息丢失)造成的，一些像素的值被随机替换为黑色或白色。使用椒盐噪声来描述OpenCV随机访问图像像素的方法比较合适。

### 1.2 方法

OpenCV提供`.at()`方法来随机访问像素值,先看具体实现:

```cpp
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

void salt(cv::Mat &image, int n) {
	int i,j;
	for (int k=0; k<n; k++) {
		i= rand()%image.cols;
		j= rand()%image.rows;
		if (image.channels() == 1) { // gray-level image
			image.at<uchar>(j,i)= 255;
		}
        else if (image.channels() == 3) { // color image
			image.at<cv::Vec3b>(j,i)[0]= 255;
			image.at<cv::Vec3b>(j,i)[1]= 255;
			image.at<cv::Vec3b>(j,i)[2]= 255;
		}
	}
}

int main()
{
	cv::Mat image= cv::imread("lena.bmp");
	salt(image,3000);
	cv::namedWindow("Image");
	cv::imshow("Image",image);
	cv::waitKey(0);
	return 0;
}
```

-------

运行结果如下：

![saltimage]({{ site.qnurl }}/media/opencv2scan/saltimage.jpg){:.img-responsive .img-rounded}

下面对一些细节加以说明。

-------

(1).**引用传递(pass-by-reference)**

图像是非常消耗存储空间的，使用引用传递来避免拷贝操作是必要的。关于引用传递，可以参考《C++ Primer 5th》6.2.2节。

-------

(2).**访问方法`.at()`**

因为`cv::Mat`可以作为不同数据类型的容器，而类方法返回类型需要在编译时指定，所以OpenCV采用采用模板方法来实现像素值访问。编程时需要给出返回值的类型。如对于灰度图像，无符号`uchar`类型可以表示0-255灰度级，所以访问此类图像采用`image.at<uchar>(j,i)`来实现。而对于RGB彩色图像，一个像素位置对应三个通道的值，OpenCV提供了`cv::Vec3b`来容纳３个８-bit值，访问此类图像采用`image.at<cv::Vec3b>(j,i)[0/1/2]`来实现。

在处理图像前，判断图像的通道数可以采用`image.channels()`方法，如果是２通道或是４通道图像，可分别采用`cv::Vec2b`和`cv::Vec4b`来实现。另外一方面，返回值是`float`或`double`类型时，把`b`替换成`f`或`d`即可。为了便于处理多类通道和数据类型的组合，其实用于容纳返回像素值的`Vec`也是采用模板实现的，详见[OpenCV-Vec](http://docs.opencv.org/modules/core/doc/basic_structures.html?highlight=vec#Vec).

-------

(3).**可选方法`()`**

一种直观的方法是使用`(i,j)`来访问，OpenCV提供了这种方法，使用前只需将图像存储在`cv::Mat_`类而不是`cv::Mat`类中，例如：

```cpp
cv::Mat_<uchar> image2=image;
image2(50,100)=0;
```

这种方法在创建图像时就把可以容纳的像素值类型都规定好了，访问像素值时不再需要指定返回类型。

-------


## 2.遍历区域像素

在更多的时候，需要对图像某个子区域(ROI)甚至整幅图像进行访问，采用随机访问需要大量的运算消耗而**没有用到图像存储区域的连续性**来提高效率，
这个时候需要用到**遍历(或扫描)**。

### 2.1实例:色彩空间压缩

对于一幅RGB图像，可以将其视为3维色彩空间，每个通道256个灰度级，则色彩空间可以表示的色彩有256^3种，这个数量是相当庞大的，
所以在某些分析场景需要用到**色彩空间压缩**。最简单的色彩空间压缩算法就是把色彩空间分成等大小的正方体区域，
取每个正方体区域的中心点所表示的色彩来表示该正方体区域内的所有色彩。用N表示每个正方体的边长，可以用N来衡量压缩程度(即N越大，压缩级别越高)。
用P表示某一像素值，下面来讨论几种该算法的具体实现:

-------

(1).**利用整型除法截断特性**


$$
\begin{align*}
P/N*N+N/2
\end{align*}
$$

原因是在整型除法时截断了小数部分，乘以N再加上N/2后则获取了色彩空间压缩后的值。

-------

(2).**求模运算**

$$
\begin{align*}
P=P-P\%N + N/2;
\end{align*}
$$

需要注意的是，几乎每个人介绍采用求模运算实现的某一算法时都会附上一句"求模运算很慢"，这个也不例外。;-)

-------

(3).**位操作**

首先要把N限制为2的某次(n)幂。

$$
\begin{align*}
mask=0xFF<<n;
P=(P\&mask)+N/2
\end{align*}
$$

与求模操作不一样，几乎每一个人介绍位操作算法时都会炫耀它的高效，当然这个也不例外。;-)

-------

### 2.2采用指针

一种典型的遍历访问方法是采用指针。


```cpp
void colorReduce(cv::Mat &image, int div=64) {
    int nl= image.rows; // number of lines
    int nc= image.cols * image.channels(); // total number of elements per line
    for (int j=0; j<nl; j++) {
        uchar* data= image.ptr<uchar>(j);
        for (int i=0; i<nc; i++) {
            // process each pixel ---------------------
            data[i]= data[i]/div*div + div/2;
            // end of pixel processing ----------------
        } // end of line
    }
}
```

注意采用的是整型除法算法。

-------

运行结果(N=64):

![reducedimage]({{ site.qnurl }}/media/opencv2scan/reducedimage.jpg){:.img-responsive .img-rounded}

-------

(1). **OpenCV通道顺序**

OpenCV内通道顺序不是R->G->B,而是B->G->R,这对所有通道"一视同仁"的操作不影响，但是在需要区分对各个通道不同操作的时候需要注意。

-------

(2).**宽度填充(padding)**

处理器在处理行宽度为４或者８的倍数的图像的时候表现更高效，所以在处理一些图像时，每一行会填充一些额外的像素，但是这些像素**不会**显示或存储。

-------

(3).**图像的几个属性**

* `step`:以字节为单位的**有效宽度**
* `elemSize()`:一个像素(所有通道)占的空间
* `channels()`:通道数
* `total()`:像素总数

注意图像的`cols`和`step`属性的区别，如果一幅三通道图像`cols`是512, 不需要填补像素，则其`step`为1536(=512x3).

-------

(4).**高效技巧一:更多的指针操作**

注意上面的程序处理过程是采用`[]`操作，如果将其改为指针操作，会得到进一步的速度提升。

```cpp
**data=*data/div*div+div2;
data++;
```

-------

(5).**高效技巧二:采用位操作算法**

```cpp
int n= static_cast<int>(log(static_cast<double>(div))/log(2.0));
char mask= 0xFF<<n;

*data= *data&mask + div/2;
data++;
```

求**掩码**的操作很容易理解，无非是old-school math，注意前两句要放在循环体外，这好像也是一种高效技巧.

-------

(6).**高效技巧三:利用图像连续性**

一些图像在存储单元中是连续存储的，i.e.,可以把他们看做一个行向量(一行接一行),OpenCV采用`isContinuous()`方法来判断图像是否连续。在程序中加入一个分支用来处理连续图像，可以针对特定图像提高效率。

```cpp
if (image.isContinuous())  {
    nc= nc*nl;
    nl= 1;
}
```

注意这种情况下就不存在宽度填充了(因为没必要).

另外`nl=1`时外面的循环语句实际上消失了，一种更极端的方式是采用`reshape()`方法来改变图像的连续性，然后彻底消除外循环。`reshape()`方法可以在不拷贝数据的前提下改变图像的行列数和通道数，没有像素被删除或添加，即`rows*cols*channels()`始终保持不变。实质上是把2维图像转换为1维序列来处理。

```cpp
image.reshape(1,image.cols*image.rows);
```

-------

(7).**高效技巧四:老板，再来更多的指针**

使用更多的低级指针操作，可以进一步提速：

* 数据单元首地址获取：`uchar *data = image.data;`
* 换行：`data +=iamge.step;`
* 访问第j行第i列：`data = image.data + j*image.step +i*image.elemSize();`

这种风格的程序实际没有充分遵循C++的思想，虽然速度快，但是**容易出错**。在处理图像的情景下，还**不能处理ROI**。

-------

(8).**增加一个参数**

上面程序的函数原型都是只接收一个图像参数，将输出结果也保存在这个参数中，称为**in-place**操作。可以增加一个参数用来放输出图像，让输入图像完好如初。

```cpp
void colorReduce(const cv::Mat &image, // input image
                    cv::Mat &result,      // output image
                    int div=64) {
    int nl= image.rows; // number of lines
    int nc= image.cols ; // number of columns
    // allocate output image if necessary
    result.create(image.rows,image.cols,image.type());
    nc= nc*nl;
    nl= 1;  // it is now a 1D array
    int n= static_cast<int>(log(static_cast<double>(div))/log(2.0));
    // mask used to round the pixel value
    uchar mask= 0xFF<<n; // e.g. for div=16, mask= 0xF0
    for (int j=0; j<nl; j++) {
        uchar* data= result.ptr<uchar>(j);
        const uchar* idata= image.ptr<uchar>(j);
        for (int i=0; i<nc; i++) {
            // process each pixel ---------------------
            *data++= (*idata++)&mask + div/2;
            *data++= (*idata++)&mask + div/2;
            *data++= (*idata++)&mask + div/2;
            // end of pixel processing ----------------
        } // end of line
    }
}
```

上面的程序首先要保证存储输出结果的图像和输入图像在尺寸和数据类型上匹配，用`.creat()`操作来创建一个新`cv::Mat`对象，`.type()`方法返回的是类似于`CV_8UC3`之类的东西。注意`.create()`操作创建的图像总是连续图像，所以按照序列来处理它就行了。

-------

### 2.3 采用迭代器

在面向对象设计(OOP)中，在数据集合上进行遍历通常使用**迭代器(iterator)**，这是一种"**information hiding principle**"，所有访问都**不会**与存储单元面对面打交道，这样可以让程序更安全。

```cpp
void colorReduce(cv::Mat &image, int div=64) {
    int n= static_cast<int>(log(static_cast<double>(div))/log(2.0));
    uchar mask= 0xFF<<n;
    cv::Mat_<cv::Vec3b>::iterator it= image.begin<cv::Vec3b>();
    cv::Mat_<cv::Vec3b>::iterator itend= image.end<cv::Vec3b>();
    for ( ; it!= itend; ++it) {
        // process each pixel ---------------------
        (*it)[0]= (*it)[0]&mask + div/2;
        (*it)[1]= (*it)[1]&mask + div/2;
        (*it)[2]= (*it)[2]&mask + div/2;
        // end of pixel processing ----------------
    }
}
```

-------

(1).**OpenCV迭代器对象**

OpenCV提供了`cv::MatIterator_`和`cv::Mat_::iterator`两种迭代器类型，前者需要指定返回值类型，后者是在`Mat_`模板内指定数据类型后提供的迭代器。`.begin()`和`.end()`表示开始和结束迭代位置。注意使用它们都需要说明返回类型(要让编译器知道，而不是运行时才知道)。

另外，`.end()`位置实际不在图像内，在迭代到这个位置之前就要终止操作，这在处理其他数据集合的情况下也是这样。有关**迭代器范围**的概念可以参考《C++ Primer-5th》9.2.1节。

-------

(2).**常量迭代器**

既然要让输入图像"完好如初"，可以采用`cv::MatConstIterator_`或是`cv::Mat_::const_iterator`来声明输入参数，这样可以减小出错的几率。

-------

### 2.4使用重载运算符

OpenCV2采用C++接口后，对一些二元运算符进行重载，这样可以把整幅图像看做操作数，直接进行修改：

```cpp
void colorReduce(cv::Mat &image, int div=64) {
    int n= static_cast<int>(log(static_cast<double>(div))/log(2.0));
    uchar mask= 0xFF<<n;
    image=(image&cv::Scalar(mask,mask,mask))+cv::Scalar(div/2,div/2,div/2);
}
```
这样的好处是程序的可读性指数级增长，瞄一眼就知道它想干什么。

## 3. 性能比较

上面介绍的算法除了重载运算符之外，可以归纳为**指针**和**迭代器**两大类，**指针**操作中又包含**连续与否**X**整型除法/求模/位运算**X**[]/指针**几种组合情况，下面来比较他们的性能。(性能排序没什么悬念，具体差多少值得研究。)

### 3.1 计时方法

OpenCV提供了`cv::getTickCount()`和`cv::getTickFrequency()`来实现计时。前者返回开机后CPU经历的时钟周期数，后者是每**秒**多少个周期。则可以算出计算消耗时间：

```cpp
double init_time;
init_time=static_cast<double>(cv::getTickCount());
colorReduce(image);
double duration=static_cast<double>(cv::getTickCount())-init_time;
duration /= cv::getTickFrequency();
```

注意单位是**秒**.

### 3.2 对比结果

采用一幅大图(2500x1700)的彩色图像测试，各个方法对比结果如下(把计时结果乘以1000以便对比，即单位为ms)：

![]({{ site.qnurl }}/media/opencv2scan/perf.png){:.img-responsive .img-rounded}

> 相同组合在不同对比实验中都有些差异，是因为我每个对比中分别只实验了一次，没有进行多次实验取平均值，没必要。

-------

(1).**到底哪家强？**

从结果中可以看出，结果和理论上分析的结果吻合，即采用指针更快，采用位运算更快。注意到采用**重载运算符配合位运算，效率是很高的**。
采用低级指针操作在这么大尺寸上的图上的**优势并不明显**，所以还是**不要**用了。

-------

(2).**Tip1:预计算频繁使用的变量**

比如图像的尺寸数据会频繁使用，`nc`和`nl`变量也在循环体中出现，这种情况下预先把值计算好存进一个变量，要比每次用到的时候再计算要快很多。

-------

(3).**Tip2:使用迭代器减少错误率**

虽然结果中可以看出迭代器慢很多，但是对于地球居民来说，100多毫秒和30多毫秒的差别根本体会不到(除非很多个过程累加起来)。另一方面，使用迭代器使程序简单明了，且安全而不容易出错。所以**在一开始就使用迭代器，在后期程序需要优化的时候再考虑使用指针**是比较好的一种思路。

-------

(4).**Tip3:在遍历时别用随机访问**

从结果中也看到了，使用随机访问轰炸一片密集区域的效率比迭代器还差很多。

-------

(5).**Tip4:尽量精简循环次数**

在色彩空间压缩算法中，对每个像素三个通道的操作是完全一样的，完全可以在一次循环内换成，而不需要每个通道用一个循环。这种思想即是，**把能放在一起处理的操作放到一个循环体内而不要分开处理**。采用这种思想，还可以优化程序：


```cpp
void colorReduce(cv::Mat &image, int div=64) {
    int nl=image.rows;
    int nc=image.cols;
    int n=static_cast<int>(log(static_cast<double>(div))/log(2.0));
    uchar mask=0xFF<<n;
    for(int j=0;j<nl;j++){
        uchar* data=image.ptr<uchar>(j);
        for(int i=0;i<nc;i++){
            *data=*data&mask+div/2;
            data++;
            *data=*data&mask+div/2;
            data++;
            *data=*data&mask+div/2;
            data++;
        }
    }
}
```
这个版本能把时间降到30ms，在特别需要效率的情况下可以考虑这种方式。

-------
