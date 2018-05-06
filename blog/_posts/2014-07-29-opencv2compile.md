---
layout: post
title: 编译安装 OpenCV2
modified: 2014-07-29
feature: false
description: 在 Ubuntu 下编译安装 OpenCV 2.4.x 版本
tags: [CV]
---

在 Ubuntu 12.04 LTS 版本下编译成功且正常使用了很长时间，在 Ubuntu 14.04 LTS 版本下安装成功但是没有长期使用，不过应该没有问题。

## 构建工具

```bash
sudo apt-get -y install build-essential cmake pkg-config
```

## 图像 I/O 库

```bash
sudo apt-get -y install libjpeg62-dev
sudo apt-get -y install libtiff4-dev libjasper-dev
```

## GTK 库

```bash
sudo apt-get -y install  libgtk2.0-dev
```

## 视频 I/O 库

```bash
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
```

## 可选安装包

### FireWire(IEEE 1394) 支持

```bash
sudo apt-get -y install libdc1394-22-dev
```

### 视频流库

```bash
sudo apt-get -y install libxine-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
```

### Python 接口

```bash
sudo apt-get -y install python-dev python-numpy
```

### Intel TBB 库

```bash
sudo apt-get -y install libtbb-dev
```

### Qt 库

```bash
sudo apt-get -y install libqt4-dev
```

## 编译

下载 2.4.x 版本，目前（2014-7.31）最新版本为 2.4.9，注意 3.0 以后的版本可能会不适用。解压到工作目录下。

```bash
cd opencv-2.4.*
mkdir build
cd build
```

配置 CMake 参数

```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_OPENGL=ON ..
```

编译（此步耗时最长）

```bash
make
```

安装完成

```bash
sudo make install
```

## 基本说明

按照以上步骤安装完成后，可以在 `/usr/local/lib` 下找到动态链接库文件，在 `/usr/local/include` 下找到 `opencv` 和 `opencv2`，里面是头文件，在 `/usr/local/share` 下找到 `OpenCV` 文件夹，里面有预训练的Haar级联器和LBP级联器文件，以及例程文件夹（`samples`）。
