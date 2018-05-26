---
layout: post
title: Visual Studio Code 集成终端
modified: 2018-05-27
feature: true
tags: [Valyria Steel]
description: 使用 Visual Studio Code 的集成终端功能快速地在编辑器中调出终端
---

Visual Studio Code 的 **集成终端(Integrated Terminal)** 功能可以基于当前工作空间快速地打开一个终端面板，并且这个集成终端支持自定义。

## 唤出终端

有三种方法可以唤出终端：

1. 通过菜单 **View \| Toggle Integrated Terminal**；
2. 通过 **Ctrl + Shift + P** 从命令面板使用 **View:Toggle Integrated Terminal**；
3. 快捷键 **Ctrl+`**

## 配置文件

集成终端在 Linux 和 OS X 上默认调用 `$SHELL` 变量作为默认终端，在 Windows 上默认调用 `%COMSPEC%` 变量（通常是CMD）作为终端。集成终端相关的配置选项在配置文件中的 `terminal.integrated.shell.*`段，另外，在 Linux 和 OS X 上还可以通过 `terminal.integrated.shellArgs.*`段来配置传递给终端的参数。

Windows 上可以使用这些选项更改默认的集成终端，如 64 位的CMD，或者Powershell，终端继承 VS Code 的权限。最酷的是，还支持 Git Bash 提供的 `bash.exe` 甚至是 [Bash on Ubuntu (on Windows)](https://msdn.microsoft.com/zh-cn/commandline/wsl/install_guide)。

```
// 64-bit cmd it available, otherwise 32-bit
"terminal.integrated.shell.windows": "C:\\Windows\\sysnative\\cmd.exe"
// 64-bit PowerShell if available, otherwise 32-bit
"terminal.integrated.shell.windows": "C:\\Windows\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe"
// Git Bash
"terminal.integrated.shell.windows": "C:\\Program Files\\Git\\bin\\bash.exe"
// Bash on Ubuntu (on Windows)
"terminal.integrated.shell.windows": "C:\\Windows\\sysnative\\bash.exe"
```

另外，能够通过 `terminal.integrated.fontFamily`、`terminal.integrated.fontSize`、`terminal.integrated.lineHeight` 三个选项来定义终端的字体、字体尺寸、线高等选项。

## 选中运行

在编辑器中选定的字体，可以通过 **Terminal:Run Selected Text in Active Terminal** 命令使其在集成终端中运行！

![](https://code.visualstudio.com/images/integrated-terminal_terminal_run_selected.png){:.img-responsive}

![](https://code.visualstudio.com/images/integrated-terminal_terminal_run_selected_result.png){:.img-responsive}

## 参考链接

1. [Integrated Terminal](https://code.visualstudio.com/docs/editor/integrated-terminal)
