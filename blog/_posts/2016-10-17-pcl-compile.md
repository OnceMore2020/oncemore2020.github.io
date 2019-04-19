---
layout: post
title: Windows 编译 PCL 1.8.0
modified: 2016-10-17
hidden: false
feature: pcl.png
tags: [Computer Vision]
description: Windows 平台下使用 Visual Studio 编译 PCL 1.8.0 源码
---

**PCL(Point Cloud Library)** 1.8.0 版本发布了，相对 1.7.x 版本，带来了大量的 [更新](https://github.com/PointCloudLibrary/pcl/blob/pcl-1.8.0/CHANGES.md#-180-14062016-)，其源码可以从 [pcl 1.8.0 release](https://github.com/PointCloudLibrary/pcl/releases/tag/pcl-1.8.0) 下载。本文记录如何在 Windows 上使用 Visual Studio C++ 编译器编译和配置 PCL 1.8.0 版本。

## tl; dr

预编译好的 PCL 1.8.0 版本，包含了第三方程序库。

下载地址：[Point Cloud Library 1.8.0](http://unanancyowen.com/?p=2009&lang=en)

## 准备工作

首先确保安装了以下工具：

1. [Visual Studio Community 2015](https://www.visualstudio.com/zh-hans/vs/community/)
2. [CMake](https://cmake.org/)
3. [Microsoft MPI v7](https://www.microsoft.com/en-us/download/details.aspx?id=49926)
4. [Qt 5.7.0 for Windows 64-bit(VS 2015)](http://mirrors.ustc.edu.cn/qtproject/archive/qt/5.7/5.7.0/qt-opensource-windows-x86-msvc2015_64-5.7.0.exe)
5. [OpenNI 2.2.0.33 Beta](http://com.occipital.openni.s3.amazonaws.com/OpenNI-Windows-x64-2.2.0.33.zip)

注意在 Microsoft MPI v7 的下载页面需要选定 **msmpisdk.msi** 和 **MSMpiSetup.exe**，两个软件都需要安装。

下载以下软件/库的源代码：

1. [PCL 1.8.0](https://github.com/PointCloudLibrary/pcl/releases/tag/pcl-1.8.0)
2. [Boost 1.61.0](http://www.boost.org/users/history/version_1_61_0.html)
3. [Eigen 3.2.8](https://bitbucket.org/eigen/eigen/get/3.2.8.tar.bz2)
4. [FLANN 1.8.4](http://www.cs.ubc.ca/research/flann/uploads/FLANN/flann-1.8.4-src.zip)
5. [VTK 7.0.0](http://www.vtk.org/files/release/7.0/VTK-7.0.0.zip)
6. [Qhull 2015.2](http://www.qhull.org/download/qhull-2015.2.zip)

## 避错贴士

由于编译过程繁杂，很容易碰到错误，目前提供如下贴士：

1. Windows 10 系统不能安装 Windows Driver Kit，否则会导致编译 Boost 时出错
2. 系统不能安装 Anaconda 2/3，否则编译 FLANN 时 HDF 相关设置会导致编译出错
3. 编译时尽量不要选择编译例程(examples)和测试(global test)，否则很容易出问题

另外，本文均使用 Visual Studio C++ 14.0 win64 编译源码，也可以使用默认的 32 位编译器，当然使用 Visual Studio 2013 版本配套的 C++ 12.0 编译器理论上也是可以的。后文用到的工具以及编译选项均假定为 64 位编译器，如使用其他版本或 32 位的编译器，注意替换。

## 编译Boost

Boost 库提供标准库兼容的 C++ 运算库，许多特性逐渐加入到新的 C++ 标准中(C++11、C++14、C++17)。

解压 Boost 源码到 `boost_1_61_0`，如 `D:\lib\boost_1_61_0`。

{:.well}
**注意**: 下文均将源代码解压到 `D:\lib` 目录中，不做另外说明。

使用文本编辑器编辑 `D:\lib\boost_1_61_0\tools\build\src\tools\mpi.jam` 文件（使用以下代码替换指定行数的代码）：

{:.well}
**注意**: Windows 下推荐 Nodepad++ 或者其他代码编辑器（Visual Studio(Code)、Sublime Text、Atom等），**不要** 使用记事本。

249-251 行

```
local microsoft_mpi_sdk_path = "C:\\Program Files (x86)\\Microsoft SDKs\\MPI" ;
local microsoft_mpi_path = "C:\\Program Files\\Microsoft MPI" ;
if [ GLOB $(microsoft_mpi_sdk_path)\\Include : mpi.h ]
```

260-262 行

```
options = <include>$(microsoft_mpi_sdk_path)/Include
<address-model>64:<library-path>$(microsoft_mpi_sdk_path)/Lib/x64
<library-path>$(microsoft_mpi_sdk_path)/Lib/x86
```

268 行

```
.mpirun = "\"$(microsoft_mpi_path)\\Bin\\mpiexec.exe"\" ;
```

保存文件后关闭。

使用管理员权限启动 **VS2015 x64 Native Tools Command Prompt**，进入到 Boost 源代码解压目录，然后运行其中的 `bootstrap.bat` 脚本。

```
D:
cd lib\boost_1_61_0
bootstrap.bat
```

{:.well}
**说明**: 第一行切换到 `D:\`，第二行切换到 Boost 源代码目录，第三行运行 `bootstrap.bat`。

将会在目录中生成 `project-config.jam` 文件，使用文本编辑器打开，在第 4 行添加

```
using mpi ;
```

继续在 **VS2015 x64 Native Tools Command Prompt** 中输入

```
b2.exe toolset=msvc-14.0 address-model=64 --build-dir=build\x64 install --prefix="D:\lib\Boost" -j8
```

{:.well}
**说明**: `--prefix=` 设置编译输出目录，默认也在 `D:\lib` 中，Boost 对应的为 `D:\lib\Boost`，其他库的编译输出目录命名类似。

等待编译完成。编译成功后添加用户变量 `BOOST_ROOT` 为 `D:\lib\Boost`。

## 编译Eigen

Eigen 主要用于矩阵运算。

解压 Eigen 源码压缩包到 `D:\lib\eigen-eigen-07105f7124f9`。

启动 CMake，设定源码目录和构建目录

* **Where is the source code**: `D:\lib\eigen-eigen-07105f7124f9`
* **Where to build the binaries**: `D:\lib\eigen-eigen-07105f7124f9\build`

点击 **Configure**，在弹出的对话框中将 **Specify the generator for this project** 修改为 **Visual Studio 14 2015 Win64**，然后点击 **Finish** 完成第一次配置。

检查以下配置项：

* **CMAKE\_INSTALL\_PREFIX**: `D:\lib\Eigen`

再次 **Configure** 后点击 **Generate** 在 `build` 目录中生成 VS 解决方案。

使用管理员权限启动 Visual Studio，通过 **File \| Open \| Project/Solution** 菜单打开 `D:\lib\eigen-eigen-07105f7124f9\build\Eigen.sln` 解决方案，在 **Solution Explorer** 中选定 **ALL\_BUILD**，右键选择 **Build** 开始构建源码，构建完成后，再选定 **INSTALL**，然后右键选择 **Build** 完成二进制文件的安装。

构建成功后生成的文件在 `D:\lib\Eigen` 文件夹中。

添加用户变量 `EIGEN_ROOT` 为 `D:\lib\Eigen`。

## 编译FLANN

FLANN 用于快速最近邻运算，在点云图像的处理过程中会涉及到大量的邻域计算。

解压 FLANN 源码压缩包到 `D:\lib\flann-1.8.4-src`。

启动 CMake，设定源码目录和构建目录

* **Where is the source code**: `D:\lib\flann-1.8.4-src`
* **Where to build the binaries**: `D:\lib\flann-1.8.4-src\build`

点击 **Configure**，在弹出的对话框中将 **Specify the generator for this project** 修改为 **Visual Studio 14 2015 Win64**，然后点击 **Finish** 完成第一次配置。

检查以下配置项（☐ 表示取消选定，☑ 表示选定）:

* **BUILD\_MATLAB\_BINDINGS**: ☐
* **BUILD\_PYTHON\_BINDINGS**: ☐
* **CMAKE\_CONFIGURATION\_TYPES**: `Debug;Release`
* **CMAKE\_INSTALL\_PREFIX**: `D:/lib/FLANN`

再次点击 **Configure** 后，点击 **Add Entry** 添加一个配置项，该配置项的值如下：

* Name: CMAKE\_DEBUG\_POSTFIX
* Type: STRING
* Value: -gd

再次点击 **Configure** 后点击 **Generate** 生成VS解决方案。

使用文本编辑器修改源文件 `D:\lib\flann-1.8.4-src\src\cpp\flann\util\serialization.h`，在第 92 行下面添加

```cpp
#ifdef _MSC_VER
    BASIC_TYPE_SERIALIZER( unsigned __int64 );
#endif
```

使用管理员权限启动 Visual Studio，通过 **File \| Open \| Project/Solution** 菜单打开 `D:\lib\flann-1.8.4-src\build\flann.sln` 解决方案。

在 **Debug** 模式下，在 **Solution Explorer** 中选定 **ALL\_BUILD**，右键选择 **Build** 开始构建源码，构建完成后选定 **INSTALL**，再右键选择 **Build** 将编译生成的文件安装到指定目录（**CMAKE\_INSTALL\_PREFIX**）。

然后再切换到 **Release** 模式，在 **Solution Explorer** 中选定 **ALL\_BUILD**，右键选择 **Build** 开始构建源码，构建完成后选定 **INSTALL**，再右键选择 **Build** 将编译生成的文件安装到指定目录。

这样将生成 Release 版本和 Debug 版本的库文件和动态链接库。

编译成功后添加用户变量 `FLANN_ROOT` 为 `D:\lib\FLANN`，在变量 **Path** 中添加 `%FLANN_ROOT%\bin`。

## 编译VTK

VTK 主要用于三维点云数据的可视化，PCL 的可视化组件依赖于 VTK。

解压 VTK 源代码到 `D:\lib\VTK-7.0.0`。

启动 CMake，设定源码目录和构建目录

* **Where is the source code**: `D:\lib\VTK-7.0.0`
* **Where to build the binaries**: `D:\lib\VTK-7.0.0\build`

点击 **Configure**，在弹出的对话框中将 **Specify the generator for this project** 修改为 **Visual Studio 14 2015 Win64**，然后点击 **Finish** 完成第一次配置。

检查以下配置项:

* **VTK\_Group\_Qt**: ☑
* **VTK\_QT\_VERSION**: 5
* **CMAKE\_CONFIGURATION\_TYPES**: `Debug;Release`
* **CMAKE\_CXX\_MP\_FLAG**: ☑
* **CMAKE\_INSTALL\_PREFIX**: `D:\lib\VTK`

点击 **Add Entry** 添加一个配置项，配置项的值如下：

* Name: CMAKE\_DEBUG\_POSTFIX
* Type: STRING
* Value: -gd

再次点击 **Configure** 后点击 **Generate** 生成 VS 解决方案。

使用管理员权限启动 Visual Studio，通过 **File \| Open \| Project/Solution** 菜单打开 `D:\lib\VTK-7.0.0\build\VTK.sln` 解决方案。

在 Debug 模式下开始构建之前，编辑 `D:\lib\VTK-7.0.0\GUISupport\Qt\PluginInstall.cmake.in` 文件，在第 5 行的 `QVTKWidgetPlugin` 后面添加 `-gd`，然后保存文件。
在 **Solution Explorer** 中选定 **ALL\_BUILD**，右键选择 **Build** 构建源代码，构建完成后 选定 **INSTALL**，再右键选择 **Build** 将编译生成的文件安装到指定位置。

切换为 Release 形式，注意此时需要撤销对 `PluginInstall.cmake.in` 文件的更改，即去掉之前添加的 `-gd`，然后保存并退出编辑。然后在 **Solution Explorer** 中选定 **ALL\_BUILD**，右键选择 **Build** 构建源代码，构建完成后，选定 **INSTALL**，再右键选择 **Build** 将编译生成的文件安装到指定位置。

这样将生成 Release 版本和 Debug 版本的库文件和动态链接库。

构建成功后，添加用户变量 `VTK_DIR` 为 `D:\lib\VTK`，在变量 **Path** 中添加 `%VTK_DIR%\bin`。

## 编译Qhull

Qhull 用于凸包计算。

解压 Qhull 源代码到 `D:\lib\qhull-2015.2`。

删除源代码目录中的 `build` 目录中的内容，然后启动 CMake，设定源码目录和构建目录

* **Where is the source code**: `D:\lib\qhull-2015.2`
* **Where to build the binaries**: `D:\lib\qhull-2015.2\build`

点击 **Configure**，在弹出的对话框中将 **Specify the generator for this project** 修改为 **Visual Studio 14 2015 Win64**，然后点击 **Finish** 完成第一次配置。

检查以下配置项:

* **CMAKE\_CONFIGURATION\_TYPES**: `Debug;Release`
* **CMAKE\_INSTALL\_PREFIX**: `D:/lib/Qhull`

点击 **Add Entry** 添加一个配置项，配置项的值如下：

* Name: CMAKE\_DEBUG\_POSTFIX
* Type: STRING
* Value: \_d

使用管理员权限启动 Visual Studio，通过 **File \| Open \| Project/Solution** 菜单打开 `D:\lib\qhull-2015.2\build\qhull.sln` 解决方案。

在 **Debug** 模式下，从 **Solution Explorer** 中选定 **ALL\_BUILD**，右键选择 **Build** 构建源代码，构建完成后选定 **INSTALL**，再右键选择 **Build** 将构建生成的文件安装到指定位置。

切换为 **Release** 模式，在 **Solution Explorer** 中选定 **ALL\_BUILD**，右键选择 **Build** 构建源代码，构建完成后选定 **INSTALL**，再右键选择 **Build** 将构建生成的文件安装到指定位置。

这样将生成 Release 版本和 Debug 版本的库文件和动态链接库。

编译成功后添加用户变量 `QHULL_ROOT` 为 `D:\lib\Qhull`。

## 编译PCL

解压 PCL 源代码到 `D:\lib\PCL-1.8.0` 目录。

{:.well}
**注意**： 下面的修改是一个 bug，在 Github 仓库里已经修复（[#1635](https://github.com/PointCloudLibrary/pcl/pull/1635)），但是 PCL 1.8.0 版本的源代码还没有更新。所以可能更新版本的 PCL 1.8.x 就不存在以下的问题了。

-----------------------
使用文本编辑器编辑 `D:\lib\PCL-1.8.0\visualization\src\pcl_visualizer.cpp`:

将第 1495 行替换为：

```cpp
if (!pcl::visualization::getColormapLUT (static_cast<LookUpTableRepresentationProperties>(static_cast<int>(value)), table))
```

将第 1741 行替换为：

```cpp
getColormapLUT (static_cast<LookUpTableRepresentationProperties>(static_cast<int>(value)), table);
```

-----------------------

启动 CMake，设定源码目录和构建目录

* **Where is the source code**: `D:\lib\PCL-1.8.0`
* **Where to build the binaries**: `D:\lib\PCL-1.8.0\build`

点击 **Configure**，在弹出的对话框中将 **Specify the generator for this project** 修改为 **Visual Studio 14 2015 Win64**，然后点击 **Finish** 完成第一次配置。

将 **Grouped** 和 **Advanced** 选定，然后检查以下配置项：

**Ungrouped Entries**

* **EIGEN\_INCLUDE\_DIR**: `D:/lib/Eigen/include/eigen3`
* **VTK\_DIR**: `D:/lib/VTK/lib/cmake/vtk-7.0`

**BUILD**

* **BUILD\_2d**: ☑(check)
* **BUILD\_CUDA**: ☐(uncheck)
* **BUILD\_GPU**: ☐(uncheck)
* **BUILD\_all\_in\_one\_installer**: ☑(check)
* **BUILD\_apps**: ☐(uncheck)
* **BUILD\_common**: ☑(check)
* **BUILD\_example**: ☐(uncheck)
* **BUILD\_features**: ☑(check)
* **BUILD\_filters**: ☑(check)
* **BUILD\_geometry**:☑(check)
* **BUILD\_global\_tests**: ☐(uncheck)
* **BUILD\_io**: ☑(check)
* **BUILD\_kdtree**: ☑(check)
* **BUILD\_keypoints**: ☑(check)
* **BUILD\_octree**: ☑(check)
* **BUILD\_outofcore**: ☑(check)
* **BUILD\_people**: ☑(check)
* **BUILD\_recognition**: ☑(check)
* **BUILD\_registration**: ☑(check)
* **BUILD\_sample\_consensus**: ☑(check)
* **BUILD\_search**: ☑(check)
* **BUILD\_segmentation**: ☑(check)
* **BUILD\_simulation**: ☐(uncheck)
* **BUILD\_stereo**: ☑(check)
* **BUILD\_surface**: ☑(check)
* **BUILD\_surface\_on\_nurbs**: ☑(check)
* **BUILD\_tools**: ☑(check)
* **BUILD\_tracking**: ☑(check)
* **BUILD\_visualization**: ☑(check)

**Boost**

* **Boost\_DATE\_TIME\_LIBRARY\_DEBUG**: `D:\lib\Boost\lib\libboost_date_time-vc140-mt-1_61.lib`
* **Boost\_DATE\_TIME\_LIBRARY\_RELEASE**: `D:\lib\Boost\lib\libboost_date_time-vc140-mt-gd-1_61.lib`
* **Boost\_FILESYSTEM\_LIBRARY\_DEBUG**:`D:\lib\Boost\lib\libboost_filesystem-vc140-mt-1_61.lib`
* **Boost\_FILESYSTEM\_LIBRARY\_RELEASE**: `D:\lib\Boost\lib\libboost_filesystem-vc140-mt-gd-1_61.lib`
* **Boost\_INCLUDE\_DIR**: `D:\lib\Boost\include\boost-1_61`
* **Boost\_IOSTREAMS\_LIBRARY\_DEBUG**: `D:\lib\Boost\lib\libboost_iostreams-vc140-mt-1_61.lib`
* **Boost\_IOSTREAMS\_LIBRARY\_RELEASE**: `D:\lib\Boost\lib\libboost_iostreams-vc140-mt-gd-1_61.lib`
* **Boost\_LIBRARY\_DIR\_DEBUG**: `D:\lib\Boost\lib`
* **Boost\_LIBRARY\_DIR\_RELEASE**: `D:\lib\Boost\lib`
* **Boost\_MPI\_LIBRARY\_DEBUG**: `D:\lib\Boost\lib\libboost_mpi-vc140-mt-1_61.lib`
* **Boost\_MPI\_LIBRARY\_RELEASE**: `D:\lib\Boost\lib\libboost_mpi-vc140-mt-gd-1_61.lib`
* **Boost\_SERIALIZATION\_LIBRARY\_DEBUG**: `D:\lib\Boost\lib\libboost_serialization-vc140-mt-1_61.lib`
* **Boost\_SERIALIZATION\_LIBRARY\_RELEASE**: `D:\lib\Boost\lib\libboost_serialization-vc140-mt-gd-1_61.lib`
* **Boost\_SYSTEM\_LIBRARY\_DEBUG**: `D:\lib\Boost\lib\libboost_system-vc140-mt-1_61.lib`
* **Boost\_SYSTEM\_LIBRARY\_RELEASE**: `D:\lib\Boost\lib\libboost_system-vc140-mt-gd-1_61.lib`
* **Boost\_THREAD\_LIBRARY\_DEBUG**: `D:\lib\Boost\lib\libboost_thread-vc140-mt-1_61.lib`
* **Boost\_THREAD\_LIBRARY\_RELEASE**: `D:\lib\Boost\lib\libboost_thread-vc140-mt-gd-1_61.lib`

**CMAKE**

* **CMAKE\_CONFIGURATION\_TYPES**: `Debug;Release`
* **CMAKE\_INSTALL\_PREFIX**: `D:\lib\PCL`

**FLANN**

* **FLANN\_INCLUDE\_DIR**: `D:\lib\flann\include`
* **FLANN\_LIBRARY**: `D:\lib\flann\lib\flann_cpp_s.lib`
* **FLANN\_LIBRARY\_DEBUG**: `D:\lib\flann\lib\flann_cpp_s-gd.lib`

**OPENNI2**

* **OPENNI2\_INCLUDE\_DIRS**: `C:\Program Files\OpenNI2\Include`
* **OPENNI2\_LIBRARY**: `C:\Program Files\OpenNI2\Lib\OpenNI2`

**QHULL**

* **QHULL\_INCLUDE\_DIR**: `D:\lib\qhull\include`
* **QHULL\_LIBRARY**: `D:\lib\qhull\lib\qhullstatic.lib`
* **QHULL\_LIBRARY\_DEBUG**: `D:\lib\qhull\lib\qhullstatic_d.lib`

**WITH**

* **WITH\_CUDA**: ☐(uncheck)
* **WITH\_DAVIDSDK**: ☐(uncheck)
* **WITH\_DOCS**: ☐(uncheck)
* **WITH\_DSSDK**: ☐(uncheck)
* **WITH\_ENSENSO**: ☐(uncheck)
* **WITH\_FZAPI**: ☐(uncheck)
* **WITH\_LIBUSB**: ☐(uncheck)
* **WITH\_OPENGL**: ☑(check)
* **WITH\_OPENNI**: ☐(uncheck)
* **WITH\_OPENNI2**: ☑(check)
* **WITH\_PCAP**: ☐(uncheck)
* **WITH\_PNG**: ☐(uncheck)
* **WITH\_QHULL**: ☑(check)
* **WITH\_QT**: ☑(check)
* **WITH\_RSSDK**: ☐(uncheck)
* **WITH\_VTK**: ☑(check)

然后再次 **Configure** 无误后使用 **Generate** 生成 VS 解决方案。

使用管理员权限启动 Visual Studio，通过 **File \| Open \| Project/Solution** 菜单打开 `D:\lib\PCL-1.8.0\build\PCL.sln` 解决方案。

在 **Debug** 模式下，从 **Solution Explorer** 中选定 **ALL\_BUILD**，右键选择 **Build** 构建源代码，构建完成后选定 **INSTALL**，再右键选择 **Build** 将构建生成的文件安装到指定位置。

切换为 **Release** 模式，在 **Solution Explorer** 中选定 **ALL\_BUILD**，右键选择 **Build** 构建源代码，构建完成后选定 **INSTALL**，再右键选择 **Build** 将构建生成的文件安装到指定位置。

这样将生成 Release 版本和 Debug 版本的库文件和动态链接库。

编译成功后添加用户变量 `PCL_ROOT` 为 `D:\lib\PCL`，并在变量 **Path** 中添加 `%PCL_ROOT%\bin` 和 `%OPENNI2_REDIST64%`。

注意到选定了 **BUILD\_all\_in\_one\_installer** 选项，构建的时候会把用到的第三方库编译好的文件拷贝到 `D:\lib\PCL\3rdParty` 目录中，因此整个过程编译完成后仅需要保留 `D:\lib\PCL` 目录就可以了，但是要注意修改一些之前设置的用户变量，包括：

* BOOST\_ROOT: `D:\lib\PCL\3rdParty\Boost`
* EIGEN\_ROOT: `D:\lib\PCL\3rdParty\Eigen`
* FLANN\_ROOT: `D:\lib\PCL\3rdParty\FLANN`
* QHULL\_ROOT: `D:\lib\PCL\3rdParty\Qhull`
* VTK\_DIR: `D:\lib\PCL\3rdParty\VTK`

编译完成后最好重启系统或注销用户账户重新登录，以使这些用户变量和环境变量生效。

## 测试


**Visual Studio 2015**:

使用 CMake 来配置和生成项目文件是最方便的。

新建一个目录 `test_vs`，在其中再创建一个空文件夹 `build`。

创建 `CMakeLists.txt` 文件，其内容如下：

```
cmake_minimum_required( VERSION 2.8 )

# Create Project
project( solution )
add_executable( project main.cpp )

# Set StartUp Project (Option)
# (This setting is able to enable by using CMake 3.6.0 RC1 or later.)
set_property( DIRECTORY PROPERTY VS_STARTUP_PROJECT "project" )

# Find Packages
find_package( PCL 1.8 REQUIRED )

if( PCL_FOUND )
  # [C/C++]>[General]>[Additional Include Directories]
  include_directories( ${PCL_INCLUDE_DIRS} )

  # [C/C++]>[Preprocessor]>[Preprocessor Definitions]
  add_definitions( ${PCL_DEFINITIONS} )
  
  # For Use Not PreCompiled Features 
  #add_definitions( -DPCL_NO_PRECOMPILE )

  # [Linker]>[General]>[Additional Library Directories]
  link_directories( ${PCL_LIBRARY_DIRS} )

  # [Linker]>[Input]>[Additional Dependencies]
  target_link_libraries( project ${PCL_LIBRARIES} )
endif()
```

然后再添加一个 `main.cpp` 文件，其内容如下：

```cpp
#include <iostream>
#include <pcl/point_cloud.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/common/common_headers.h>


int main(char argc, char** argv)
{
	// Create Point Cloud Object Pointer
	pcl::PointCloud<pcl::PointXYZ>::Ptr source_cloud(new pcl::PointCloud<pcl::PointXYZ>());

	// Configureable  Parameters
	float radius = 10.0f;

	// Generating clouds
	for (float theta(0.0); theta <= 360.0f; theta += 2.0f) {
		for (float phi(0.0); phi <= 180.0f; phi += 2.0f) {
			pcl::PointXYZ tmp_point;
			tmp_point.x = radius*cosf(pcl::deg2rad(theta))*sinf(pcl::deg2rad(phi));
			tmp_point.y = radius*sinf(pcl::deg2rad(theta))*sinf(pcl::deg2rad(phi));
			tmp_point.z = radius*cosf(pcl::deg2rad(phi));
			source_cloud->points.push_back(tmp_point);
		}
	}

	// Visualization
	pcl::visualization::PCLVisualizer viewer("visualizer");
	pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ> source_cloud_color_handler(source_cloud, 255, 255, 255);
	viewer.addPointCloud(source_cloud, source_cloud_color_handler, "original_cloud");
	viewer.addCoordinateSystem(5.0);

	while (!viewer.wasStopped()) {
		viewer.spinOnce();
	}

	return 0;
}
```

然后启动 CMake，和源代码的编译类似，设置源代码目录和构建目录如下：

* **Where is the source code**: `test_vs`
* **Where to build the binaries**: `test_vs\build`

点击 **Configure**，然后点击 **Generate** 即可在 `build` 目录中生成 VS 解决方案文件。

使用 Visual Studio 打开 `build` 目录中的 `solution.sln`，点击 `Ctrl+F5` 不调试运行或 `F5` 调试运行，若配置成功，将显示一个生成的球状点云，如下图所示


![test_vs]({{ site.qnurl }}/media/pcl-compile/test_vs.png){: .img-fluid}

**Qt**

需要使用 Qt 自带的 `qmake` 来配置相关选项，使用 Qt Creator 新建一个新的 Widgets Application，项目命名为 `test_qt`，则创建完成后可以在项目侧边栏看到 `test_qt.pro` 文件，双击编辑添加以下内容：

```
INCLUDEPATH += D:\lib\PCL\include\pcl-1.8
INCLUDEPATH += D:\lib\PCL\3rdParty\Eigen\eigen3
INCLUDEPATH += D:\lib\PCL\3rdParty\VTK\include\vtk-7.0
INCLUDEPATH += D:\lib\PCL\3rdParty\Boost\include\boost-1_61
INCLUDEPATH += D:\lib\PCL\3rdParty\FLANN\include

LIBS +=  -LD:\lib\PCL\3rdParty\VTK\lib \
         -lvtkGUISupportQt-7.0-gd \
         -lvtkIOImage-7.0-gd \
         -lvtkInteractionImage-7.0-gd \
         -lvtkRenderingCore-7.0-gd \
         -lvtkCommonExecutionModel-7.0-gd \
         -lvtkCommonCore-7.0-gd \
         -lvtkCommonDataModel-7.0-gd \
         -lvtkCommonMath-7.0-gd \
         -lvtkRenderingOpenGL2-7.0-gd \
         -lvtkRenderingLOD-7.0-gd \
         -lvtkInteractionStyle-7.0-gd

LIBS +=  -LD:\lib\PCL\lib \
         -lpcl_common_debug \
         -lpcl_visualization_debug

LIBS += -LD:\lib\PCL\3rdParty\Boost\lib
```

`INCLUDEPATH` 语法用于添加头文件目录，`LIBS` 语法用于添加库文件目录，该部分配置的内容取决于使用了哪些模块，精简项目不使用的模块能够加快编译速度。

这里测试 **QVTKWidget** 组件用于可视化点云的功能。

添加一个头文件 `cloudObject.h`，内容如下：

```cpp
#ifndef CLOUDOBJECT_H
#define CLOUDOBJECT_H

#include <vtkAutoInit.h>
VTK_MODULE_INIT(vtkRenderingOpenGL2);
VTK_MODULE_INIT(vtkInteractionStyle);

#include <QMainWindow>
#include <QVTKWidget.h>
#include <pcl/point_cloud.h>
#include <pcl/common/common_headers.h>
#include <pcl/visualization/pcl_visualizer.h>

class cloudObject: public QMainWindow
{
    Q_OBJECT
public:
    cloudObject(QWidget *parent = 0);
    ~cloudObject();

private:
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud;
    boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer;
    QVTKWidget* widget;
    void initialVtkWidget();
};

#endif // CLOUDOBJECT_H
```

添加对应的源文件 `cloudObject.cpp`，内容如下：

```cpp
#include <iostream>
#include <vtkRenderWindow.h>
#include "cloudObject.h"

cloudObject::cloudObject(QWidget *parent)
    : QMainWindow(parent)
{
    initialVtkWidget();
    resize(500,500);
    setCentralWidget(widget);
}

cloudObject::~cloudObject()
{

}
void cloudObject::initialVtkWidget()
{
    cloud.reset(new pcl::PointCloud<pcl::PointXYZ>);
    viewer.reset(new pcl::visualization::PCLVisualizer("viewer", false));
    widget = new QVTKWidget;

    float radius = 10.0f;
    for (float theta(0.0); theta <= 360.0f; theta += 2.0f) {
        for (float phi(0.0); phi <= 180.0f; phi += 2.0f) {
            pcl::PointXYZ tmp_point;
            tmp_point.x = radius*cosf(pcl::deg2rad(theta))*sinf(pcl::deg2rad(phi));
            tmp_point.y = radius*sinf(pcl::deg2rad(theta))*sinf(pcl::deg2rad(phi));
            tmp_point.z = radius*cosf(pcl::deg2rad(phi));
            cloud->points.push_back(tmp_point);
        }
    }

    viewer->addPointCloud(cloud, "cloud");
    widget->SetRenderWindow(viewer->getRenderWindow());
    viewer->setupInteractor(widget->GetInteractor(), widget->GetRenderWindow());
    viewer->addCoordinateSystem(2.0);
    widget->update();
}
```

和 Visual Studio 的测试类似，我们首先创建一个点云对象，生成球状的点云，并使用 `QVTKWidget` 组件可视化。

编辑 `main.cpp` 内容为：

```cpp
#include "cloudObject.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    cloudObject w;
    w.show();
    return a.exec();
}
```

执行 **构建 \| 执行 qmake**， 然后 **构建 \| 运行** 运行程序，如下图所示：


![test_vs]({{ site.qnurl }}/media/pcl-compile/test_qt.png){: .img-fluid}

如果测试没有问题，说明编译生成的程序库都是可用的。

## 参考

[Building PCL 1.8.0 with Visual Studio](https://gist.github.com/UnaNancyOwen/59319050d53c137ca8f3#file-pcl1-8-0-md) (日文)
