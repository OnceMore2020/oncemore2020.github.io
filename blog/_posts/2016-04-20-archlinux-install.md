---
layout: post
title: Archlinux 安装配置
modified: 2016-04-25
hidden: false
feature: archlinux.png
tags: [Valyria Steel]
description: Archlinux 是最好的 Linux 发行版，并且安装和使用 Archlinux 并不难！本文记录从零开始安装 Archlinux的过程并附带简单解释，文末附上非常有用的 ArchLinux 参考指南。
---

## 安装镜像

推荐从 [中科大镜像站](http://mirrors.ustc.edu.cn/archlinux/iso/) 下载当月的 Archlinux 镜像。 (Archlinux 每个月初会发行新安装包)

* 若要直接安装到电脑上，使用下载的镜像刻录U盘，然后使用U盘引导系统。

* 若在虚拟机中(如VirtualBox)安装，直接从虚拟机引导ISO镜像即可进入安装界面。

![04.PNG]({{ site.qnurl }}/media/arch-install/04.PNG){:.img-fluid}

### 附：VirtualBox 设置

建议设置桥接网卡，这样虚拟机内的系统可以获得一个和宿主机独立的IP地址，方便远程ssh登录。建议启用EFI。

![00.PNG]({{ site.qnurl }}/media/arch-install/00.PNG){:.img-fluid}

![01.PNG]({{ site.qnurl }}/media/arch-install/01.PNG){:.img-fluid}

![02.PNG]({{ site.qnurl }}/media/arch-install/02.PNG){:.img-fluid}

![020.PNG]({{ site.qnurl }}/media/arch-install/020.PNG){:.img-fluid}

## 开始之前

注意下文需要输入的指令中包含命令提示符，`$` 表示普通用户指令，不需要超级用户权限，`#`表示超级用户指令，需要超级用户权限才能执行。复制粘贴或照着输入时需要忽略命令提示符。

一般来说，在建立普通用户之前都是用的是超级用户执行指令，建立普通用户之后建议登录普通用户继续操作。

## 分区设置

我们现在有一块未分区的磁盘，其在文件系统中的位置是 `/dev/sda`，在安装之前首先对该磁盘进行分区。假设机器开启了EFI，下文建立新系统的分区表（GPT分区），并设置`/dev/sda1`为 ESP 启动分区，`/dev/sda2`来挂载新系统的根目录。

使用 `parted` 分区:

方案一：ESP分区512MB，剩余空间全部给`/`:

```bash
# parted /dev/sda
(parted) mklabel gpt
(parted) mkpart ESP fat32 1MiB 513MiB
(parted) set 1 boot on
(parted) mkpart primary ext4 513MiB 100%
(parted) quit
```

方案二：启用swap分区（4GB）：

```bash
# parted /dev/sda
(parted) mklabel gpt
(parted) mkpart ESP fat32 1MiB 513MiB
(parted) set 1 boot on
(parted) mkpart primary linux-swap 513MiB 4.5G
(parted) mkpart primary ext4 4.5G 100%
(parted) quit
```

接下来需要将新建立的分区挂载到从镜像启动的系统的文件系统内，才能使用从镜像启动的系统来将ArchLinux系统文件拷贝进新系统的分区(有点绕口)。将`/dev/sda2`挂载到安装系统的`/mnt`，并将`/dev/sda1`挂载到安装系统的`/mnt/boot`。这里需要建立起一个映射概念，即目前的`/mnt`对应于新系统的根目录`/`，目前的`/mnt/boot`对应于新系统的`/boot`。

挂载分区（以方案一为例）:

```bash
# ls /dev | grep sda
# mkfs.ext4 /dev/sda2
# mkfs.fat -F32 /dev/sda1
# mount /dev/sda2 /mnt
# mkdir -p /mnt/boot
# mount /dev/sda1 /mnt/boot
```

注意：如开启了swap分区（如`/dev/sda2`），需要输入

```bash
# mkswap /dev/sda2
# swapon /dev/sda2
```

## 设置软件源

ArchLinux 使用 pacman 作为包管理器，`/etc/pacman.d/mirrorlist` 作为 pacman 软件源的配置文件。安装之前我们选择国内的较快的开源镜像站提供的ArchLinux软件源来加速文件下载。

打开`/etc/pacman.d/mirrorlist`，选择一个国内的软件源粘贴到文件的前面位置，如使用vi编辑器将中科大软件源放到前排（打开文件->选择ustc软件源->复制->粘贴到第5行后面->保存退出）：

```bash
# vi /etc/pacman.d/mirrorlist
(vi) /ustc<enter>
(vi) yy
(vi) :5<enter>
(vi) p
(vi) :wq<enter>
```

## 开始安装

ArchLinux使用 `pacstrap` 来将系统文件拷贝到`/mnt`内，再说一遍，之前我们将`/dev/sda2`挂载到了`/mnt`，目前`/mnt`是新系统的根目录。

```bash
# pacstrap /mnt base base-devel
```

`base` 是必选项，包含基础软件包，`base-devel` 包含了常用的开发工具组合。

## 修改 fstab

所谓 fstab, 就是 File System TABle 的意思，是组织文件系统的一张表。`/mnt`是新系统的根目录，需要将新系统根目录下的文件系统表记录到新系统的`/etc/fstab`文件中，即`/mnt/etc/fstab`。

```bash
# genfstab -U -p /mnt >> /mnt/etc/fstab
```

## 进入新系统

好了，该做的都做了，该进入新系统了。

```bash
# arch-chroot /mnt
```

会发现命令行提示符有一些小变化，说明已经作为root用户登录进新系统了。输入

```bash
# passwd
```

设置root用户的密码。


## 设置时区

`/usr/share/zoneinfo` 内存储了世界各地的时区信息，创建一个链接到`/etc/localtime`，即时区配置文件。

```bash
# ln -s /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
```

## locale设置

编辑`/etc/locale.gen`文件，添加下面几行，表示需要支持 UTF-8 编码的中文和英文，以及 GBK 和 GB2312 编码的中文。

```bash
en_US.UTF-8
zh_CN.UTF-8
zh_CN.GBK
zh_CN.GB2312
```

编辑`/etc/locale.conf`文件设置系统语言为英文

```bash
LANG="en_US.UTF-8"
```

保存退出后使用

```bash
# locale-gen
```

生成系统的本地化设置。

## 引导器

为了使重启系统后能够脱离安装镜像，进入安装的新系统，必须要对启动引导做一些设置。

```bash
# mkinitcpio -p linux
# bootctl install
```

然后编辑`/boot/loader/entries/arch.conf`，加入以下内容

```bash
title          Arch Linux
linux          /vmlinuz-linux
initrd         /initramfs-linux.img
options        root=/dev/sda2 rw
```

然后编辑`/boot/loader/loader.conf`加入以下内容，表示默认使用`arch.conf`内设置的启动系统。

```
timeout 3
default arch
```

## 完成安装

在重启之前，首先退出系统，然后卸载`/mnt`

```bash
# exit
# umount -R /mnt
```

重启系统，以root用户身份登入新安装的系统。

## 添加用户

如添加一个用户名为`guanhao`、使用`/bin/bash`作为默认shell、在`users`用户组中的用户，并设置密码。

```bash
# useradd -m -g users -s /bin/bash guanhao
# passwd guanhao
```

赋予`guanhao` 执行`sudo`的权限，执行

```bash
visudo
```

插入以下行：

```bash
(add guanhao ALL=(ALL) ALL)
```

## DHCP和DNS设置

编辑`/etc/systemd/network/MyDhcp.network`，添加以下内容

```
[Match]
Name=en*

[Network]
DHCP=ipv4
```

然后使用`systemctl`来使能并启动`systemd-networkd.service`和`systemd-resolved.service`守护进程。

```
# systemctl enable systemd-networkd.service
# systemctl start systemd-networkd.service
# systemctl enable systemd-resolved.service
# systemctl start systemd-resolved.service
# ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
```

系统会自动从路由器获取一个独立于宿主机的IP地址。

到此为止，安装工作基本完成了。在进一步的 tweak 之前，为了保护来之不易的新系统，建议使用刚建立的普通用户登录系统，如

```bash
# su guanhao
```

## AUR 配置

[AUR](https://aur.archlinux.org/) 中包含了一些 Archlinux 官方仓库中没有的或者版本更新的软件，使用AUR仓库中的PKGBUILD脚本可以方便的安装官方仓库中没有的软件。`yaourt`则进一步封装了AUR的使用，采用类似于`pacman`的操作来从AUR获取和安装新软件。

要启用yaourt，编辑`/etc/pacman.conf`（需要使用sudo才能具有写权限），添加：

```
[archlinuxfr]
SigLevel = Never
Server = http://repo.archlinux.fr/$arch
```

然后使用pacman安装yaourt（记住pacman 安装软件的方法）

```bash
$ sudo pacman -Sy yaourt
```

## ssh配置

要使用SSH远程登录 ArchLinux，首先安装openssh

```bash
$ sudo pacman -S openssh
```

然后编辑ssh服务器守护进程的配置文件`/etc/ssh/sshd_config`，修改Port为一个自定义的端口号替代默认的22号端口，这样有两个好处：

* 安全考虑
* 局域网端口转发以支持多台机器

然后使用`systemctl`使能并启动`sshd.service`守护进程

```bash
$ sudo systemctl enable sshd.service
$ sudo systemctl start sshd.service
```

在机器所在的局域网路由器上做端口转发设置，即可从任何地方使用ssh客户端登录该机器。

## Virtualbox增强功能

Virtualbox给客户端操作系统提供了增强工具以增强显示、粘贴板、共享文件夹等功能。从ArchLinux官方仓库安装`virtualbox-guest-utils`即可。

```bash
$ sudo pacman -S virtualbox-guest-utils
```

然后添加内核模块使起开机自动启动，编辑`/etc/modules-load.d/virtualbox.conf`，添加以下几行

```
vboxguest
vboxsf
vboxvideo
```

这样每次开机后运行

```bash
$ VBoxClient-all
```

即可使能增强功能。

### 附：共享文件夹设置

首先在 Virtualbox 中给Archlinux分配共享文件夹，如宿主机上的整个分区

![06.PNG]({{ site.qnurl }}/media/arch-install/06.PNG){:.img-fluid}

然后在Archlinux中输入

```bash
$ sudo mount -t vboxsf G_DRIVE /mnt
```

即可将共享文件夹挂载到`/mnt`位置，当然也可以选择其他位置，这样访问`/mnt`就可以访问宿主系统上的文件夹。

## 参考

好吧，其实参考文章们才是最重要的，建议没事就读读~

1. [给妹子看的 Arch Linux 桌面日常安装](https://bigeagle.me/2014/06/archlinux-install-for-beginners/)
1. [Arch Linux easy install with with windows (dual boot) for beginners](https://lampjs.wordpress.com/2014/09/01/arch-linux-easy-install-with-with-windows-dual-boot-for-beginners/)
1. [ArchLinux - Beginners' guide](https://wiki.archlinux.org/index.php/Beginners%27_guide)
1. [ArchLinux - Virtualbox](https://wiki.archlinux.org/index.php/VirtualBox)
1. [ArchLinux - systemd](https://wiki.archlinux.org/index.php/Systemd)
1. [ArchLinux - General recommendations](https://wiki.archlinux.org/index.php/General_recommendations)
1. [ArchLinux - pacman/Tips and tricks](https://wiki.archlinux.org/index.php/Pacman/Tips_and_tricks)
1. [ArchLinux - Users and groups](https://wiki.archlinux.org/index.php/Users_and_groups)
1. [ArchLinux - Secure Shell](https://wiki.archlinux.org/index.php/Secure_Shell)
