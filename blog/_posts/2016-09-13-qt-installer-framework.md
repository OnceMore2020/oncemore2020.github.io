---
layout: post
title: Qt Installer Framework 制作安装包
modified: 2016-09-13
feature: false
tags: [Valyria Steel]
description: 使用 Qt Installer Framework 部署你的程序。
---

## 游戏名目

Qt Installer Framework （后简称QIF）提供了用于创建兼容不同桌面平台（Linux、Microsoft Windows、OS X）安装包的工具和应用集合，其能够生成若干安装页面，引导用户（软件终端用户）完成安装，并提供软件升级和卸载的功能。通常使用可安装内容（可执行文件、资源文件、动态链接库等）并指定一些必要的信息（如程序名字、授权文本等），即可构建一个安装包程序，用户（软件开发者）也可以对安装过程中的页面进行自定义。

![]({{ site.qnurl }}/media/qt-installer/ifw-overview.png){:.img-responsive}

QIF 支持 **离线安装(offline)** 和 **在线安装(online)** 两种部署方式，两种方式都会安装一个 **维护工具(maintenance tool)** 用于添加、升级和删除组件。离线安装方式在安装期间不需要互联网连接，在线安装方式会首先安装维护工具，然后从远程仓库中拉取对应版本的组件进行安装。相对于离线安装方式，在线方式可以通过用户预先选择需要安装的组件的机制来避免下载不会被安装的组件，能够减小服务器压力，并节省软件用户的时间。

> 维护工具就像包管理器一样。

## 快速上手

### 配置 QIF

可以从 [Qt Downloads - Qt Installer Framework](http://download.qt.io/official_releases/qt-installer-framework/) 下载最新版本的预编译版本进行安装，也可在本机上编译源代码得到相关的二进制程序。

**编译源码方法**: 打开 Qt Creator，点击 New Project 进入项目创建页面，选择 *导入项目*，然后选择 *Git Repository Clone*，在下一个窗口中输入 QIF 源码的 git 仓库地址

[git://code.qt.io/installer-framework/installer-framework.git](git://code.qt.io/installer-framework/installer-framework.git)

选择项目路径，等待代码克隆完毕后根据提示完成 Configure 和构建即可在项目对应的 build 目录中的 *bin* 文件夹中生成 QIF 相关的二进制文件。

### 工作流

QIF 支持 **初始安装**、**添加组件**、**删除组件**、**升级组件** 等基础工作流。

初始安装，包括 **安装介绍**、**选择安装目录**、**选择组件**、**授权协议**、**Windows开始菜单项**（仅针对 Windows 平台）、**开始安装** 等流程。

![]({{ site.qnurl }}/media/qt-installer/ifw-user-flow-installing.png){:.img-responsive}

添加组件，用于在初始安装后添加新的组件（类似于包管理器），包括以下三个流程。

![]({{ site.qnurl }}/media/qt-installer/ifw-user-flow-adding.png){:.img-responsive}

删除组件，用于在删除之前安装的组件，包含以下流程，其中 *Remove* 选项直接删除所有组件。

![]({{ site.qnurl }}/media/qt-installer/ifw-user-flow-removing.png){:.img-responsive}

升级组件，用于从远程仓库获取升级的组件并安装，包括以下三个流程。

![]({{ site.qnurl }}/media/qt-installer/ifw-user-flow-updating.png){:.img-responsive}

### 创建安装包

要创建安装包，需要以下几个步骤：

1. 创建一个 *包目录(package)*，包含配置文件和待安装的包；
2. 创建一个配置文件制定如何构建安装包程序和在线仓库；
3. 创建一个 *包信息* 文件用于描述各待安装的组件；
4. 拷贝安装文件（可执行程序、资源文件、动态链接库）到包目录；
5. 使用`binarycreator(.exe)`工具来创建安装包。

下面详细说明每一个步骤。

---

**创建包目录**: 无论是离线安装方式还是在线安装方式，待安装的内容嵌入离线安装包或是存储在远程仓库中，都需要设计统一的目录结构和格式来组织和存储这些组件内容。包目录包含了需要安装的资源，其设计原则为：

1. 合理组织待安装组件
2. 便于扩展组件（添加、删除、升级）

QIF 规定包目录内至少应该包含 `config` 和 `packages` 两个目录，用于存储配置文件和包，对于 `packages` 目录，其结构看起来如下：

```
-packages
    - com.vendor.root
        - data
        - meta
    - com.vendor.root.component1
        - data
        - meta
    - com.vendor.root.component1.subcomponent1
        - data
        - meta
    - com.vendor.root.component2
        - data
        - meta
```

各子目录的命名类似于域名标识，用于区分各个组件，子目录中包含 `data` 和 `meta` 两个子目录。`meta` 目录中存储部署和安装过程的配置选项，其中的文件不会被安装程序解压到终端用户的计算机上，`meta`中至少应该包含一个`package.xml`文件用于描述包信息，示例为

```
<?xml version="1.0"?>
<Package>
    <DisplayName>QtGui</DisplayName>
    <Description>Qt gui libraries</Description>
    <Description xml:lang="de_de">Qt GUI Bibliotheken</Description>
    <Version>1.2.3</Version>
    <ReleaseDate>2009-04-23</ReleaseDate>
    <Name>com.vendor.root.component2</Name>
    <Dependencies>com.vendor.root.component1</Dependencies>
    <Virtual>false</Virtual>
    <Licenses>
        <License name="License Agreement" file="license.txt" />
    </Licenses>
    <Script>installscript.qs</Script>
    <UserInterfaces>
        <UserInterface>specialpage.ui</UserInterface>
        <UserInterface>errorpage.ui</UserInterface>
    </UserInterfaces>
    <Translations>
        <Translation>sv_se.qm</Translation>
        <Translation>de_de.qm</Translation>
    </Translations>
    <DownloadableArchives>component2.7z, component2a.7z</DownloadableArchives>
    <AutoDependOn>com.vendor.root.component3</AutoDependOn>
    <SortingPriority>123</SortingPriority>
    <UpdateText>This changed compared to the last release</UpdateText>
    <Default>false</Default>
    <ForcedInstallation>false</ForcedInstallation>
    <Essential>false</Essential>
    <Replaces>com.vendor.root.component2old</Replaces>
</Package>
```

各个标签的用法如下：

|标签|用途|
|:---|:---|
|DisplayName|组件名字(用户友好)|
|Description|描述字段(用户友好)|
|Version|版本号|
|ReleaseDate|发布日期|
|Name|域名标识格式的包名字|
|Dependencies|指定依赖项，并且可以附带指定版本号，版本号支持`=,>,<,>=,<=`符号，但是必须使用`&lt`来替换`<`，用`&lt;=`来替换`<=`|
|AutoDependOn|设置自动依赖项，只有在指定的依赖完全满足时，组件的单选框才会被自动选定，组件才能被安装，并且在依赖项被移除时，自动被移除|
|Virtual|设置为`true`后在安装程序中隐藏显示当前包，对`root`组件无效|
|SortingPriority|组件在安装程序中显示的优先级，优先级高的组件排在顶部|
|Licenses|用户授权文档，多个文档用多个`<License></License>`来组织|
|Script|指定在安装包运行时加载的脚本|
|UserInterfaces|安装包需要额外加载的页面|
|Translations|国际化支持，指定需要加载的国际化文件|
|UpdateText|升级组件时的附加描述|
|Default|可选值包括`true`、`false`、`script`，设置为`true`时，在安装时当前包默认被选定,也可设置为`script`，这样在运行时解析脚本来设置是否默认选定，脚本通过`<Script></Script>`来指定。|
|Essential|设置为`true`后，若当前包有更新，包管理器在当前包更新后才能使用；若是新添加的包，则自动安装|
|ForcedInstallation|值为`true`时设定当前包为必选安装项|
|Replaces|用当前包来替换的组件|
|DownloadableArchives|列出在线安装包可以下载的文件（用逗号分隔）|
|RequiresAdminRights|如果安装包需要提升权限才能安装，设置为`true`|

`data`目录包含了安装程序在安装过程中解压的内容，必须使用 7zip 格式的压缩包(`*.7z`)，可以使用 QIF 的 `archivegen`工具来生成压缩包。

---

**创建配置文件**: 在`config`目录中创建一个`config.xml`文件，包含以下内容

```
<?xml version="1.0" encoding="UTF-8"?>
<Installer>
    <Name>Your application</Name>
    <Version>1.0.0</Version>
    <Title>Your application Installer</Title>
    <Publisher>Your vendor</Publisher>
    <StartMenuDir>Super App</StartMenuDir>
    <TargetDir>@HomeDir@/InstallationDirectory</TargetDir>
</Installer>
```

各个标签的用法如下：

|标签|用法|
|:--|:---|
|Title|显示于安装程序的标题栏|
|Name|指定应用名字|
|Version|应用版本号|
|Publisher|软件发布方|
|StartMenuDir|（Windows）程序在开始菜单中的名字|
|TargetDir|默认安装路径|

---

**创建包信息描述文件**: 此文件用于描述各个组件的信息，放在组件目录内的`meta`目录中，命名为`package.xml`，示例如下：

```
<?xml version="1.0" encoding="UTF-8"?>
<Package>
    <DisplayName>The root component</DisplayName>
    <Description>Install this example.</Description>
    <Version>0.1.0-1</Version>
    <ReleaseDate>2010-09-21</ReleaseDate>
    <Licenses>
        <License name="Beer Public License Agreement" file="license.txt" />
    </Licenses>
    <Default>script</Default>
    <Script>installscript.qs</Script>
    <UserInterfaces>
        <UserInterface>page.ui</UserInterface>
    </UserInterfaces>
</Package>
```


## 参考文档

1. [Qt Installer Framework Manual](http://doc.qt.io/qtinstallerframework/index.html)
2. [End User Workflows](http://doc.qt.io/qtinstallerframework/ifw-use-cases.html)
3. [Package Directory](http://doc.qt.io/qtinstallerframework/ifw-component-description.html)
