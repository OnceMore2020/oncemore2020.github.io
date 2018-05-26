---
layout: post
title: Anaconda Environment 使用
modified: 2018-05-27 00:34:02.017141
tags: [Coding]
feature: true
description: 了解如何使用 Anaconda 的 Environment 特性创建、管理、配置 Python 环境。
---

和 [virtualenv](https://virtualenv.pypa.io/en/stable/) 一样，Anaconda 提供了一套创建“虚拟环境”的机制，文档中称为 “Anaconda Environments”。Anaconda Environment 和 Anaconda 整合更好，如果使用的 Python 环境是 Anaconda，推荐用其替代 virtualenv 进行环境的管理。

> 下文的操作在 Anaconda 的 `root` 环境中运行。在 Windows 上，即 `Anaconda Prompt` 命令行工具。

## 0. 创建环境

```bash
conda create --name myenv
```

`--name` 参数带的是需要创建的环境的名字。

还可以指定 Python 的版本号

```bash
conda create --name myenv python=3.6
```

其实，不指定 Python 版本号时，还是会安装 Python 运行时和 pip 包管理器等默认项（可通过 `~/.condarc` 配置），可以通过开关参数 `--no-default-packages` 关闭默认安装。

更酷的是可以在创建时一口气指定还需要安装的包，例如：

```bash
conda create -n myenv python=3.4 scipy=0.15.0 astroid babel
```

## 1. 激活/去激活环境

Windows

```bash
activate myenv
deactivate
```

OS X / Linux

```bash
source activate myenv
source deactivate
```

## 2. 管理环境

列出所有环境

```bash
conda env list
```

查看当前的环境

```bash
conda info --envs
```

## 3. “Freeze”

```bash
conda env export > environment.yml
```

生成的 `*.yml` 文件可以用于分发，用户可以使用 `*.yml` 文件直接创建环境

```bash
conda env create -f environment.yml
```

## 4. 删除环境

```bash
conda env remove --name myenv
```

或者

```bash
conda remove --name myenv --all
```
