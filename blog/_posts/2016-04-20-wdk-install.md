---
layout: post
title: Qt-MSVC 版本开启调试功能
modified: 2016-04-25
hidden: true
description: 介绍如何在 Windows 预编译版本的 Qt 下开启调试功能。
tags: [Coding]
---

在 Windows 环境下安装 VS2013 或者 VS2015 预编译版本的Qt后会发现，尽管 Qt 能够正常编译和运行程序，但是在启动调试时会提示没有调试器。此时需要安装 **Windows 调试工具（WinDbg)**, 目前 WinDbg 工具包含在 **Windows 驱动程序工具包（WDK）**中。下载地址：[下载 WDK、WinDbg 和相关工具](https://msdn.microsoft.com/zh-CN/windows/hardware/hh852365.aspx)。

下载完成后按照提示安装，重新启动Qt则会自动检测到调试工具。

