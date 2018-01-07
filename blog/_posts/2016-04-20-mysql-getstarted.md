---
layout: post
title: MySQL 快速上手
modified: 2016-04-25
hidden: true
feature: mysql.png
tags: [Database]
description: 从基础概念介绍到安装配置和使用，快速上手 MySQL。
---

## 游戏名目

**数据库（Database）** 是按照数据结构来组织、存储和管理数据的仓库，

**关系型数据库（Relational Database Management System）**，是建立在关系模型基础上的数据库，借助于集合代数等数学概念和方法来处理数据库中的数据，其特点包括：

1. 数据以表格的形式出现
2. 每行为各种记录名称
3. 每列为记录名称所对应的数据域
4. 许多行和列组成一张表单
5. 若干的表单组成数据库

**SQL（Structured Query Language）语言** 是介于关系代数与关系演算之间的结构化查询语言，是一个通用的、功能极强的关系型数据库语言。

MySQL 是最流行的关系型数据库管理系统，性能高、成本低、可靠性好，最早属于 MySQL AB 公司，后来几经转折到了 Oracle 手里，目前仍然提供社区版本的 MySQL，为了规避其闭源的风险，MySQL 创始人 [Michael "Monty" Widenius](https://en.wikipedia.org/wiki/Michael_Widenius) 主导开发了 MySQL 的分支版本 MariaDB。

## 安装MySQL

使用发行版的包管理器安装，如 Archlinux 使用 [MariaDB](https://mariadb.org/) 作为默认的 MySQL 实现，安装和配置参考 [MySQL - ArchWiki](https://wiki.archlinux.org/index.php/MySQL) 进行。

首先安装`mariadb`包

```bash
$ sudo pacman -S mariadb
```

然后初始化 MariaDB 的目录

```bash
$ sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
```

然后使用 `systemd` 使能并启动 `mysqld.service` 守护进程。

```bash
$ sudo systemctl enable mysqld.service
$ sudo systemctl start mysqld.service
```

之后启动机器 `mysqld.service` 会作为守护进程自动启动。

然后执行以下脚本来进行一些初始化安全设置(设置root用户密码、删除匿名用户、关闭root用户远程登录、删除test数据库、重载授权表)，注意提示输入root用户密码时直接按回车即可，这个root用户和系统的root用户需要区分开。

```bash
$ sudo mysql_secure_installation
```

## 基础入门

MySQL 数据库系统使用 **客户端-服务器（Client-Server）** 架构，`mysqld` 作为服务器，负责在数据库上进行实际的操作，客户端 `mysql` 通过SQL语言和服务器端交互，告诉服务器如何在数据库上进行操作。因此之前的配置将`mysqld.service` 添加到守护进程，而之后我们主要需要了解如何使用`mysql`客户端和SQL语句来和服务器通信。

使用

```bash
$ mysql -u root -p
```

即可作为数据库的 root 用户登录。

### 创建帐号

添加用户分为两步：创建用户(`CREATE USER`) + 授权(`GRANT`)，需要由root用户来完成。示例：创建一个用户名为`oncemore`密码为`666666`的用户，并且授予`mydb`数据库的所有权限。

```bash
MariaDB> CREATE USER 'oncemore'@'localhost' IDENTIFIED BY '666666';
MariaDB> GRANT ALL PRIVILEGES ON mydb.* TO 'oncemore'@'localhost';
MariaDB> FLUSH PRIVILEGES;
MariaDB> quit
```

`FLUSH PRIVILEGES` 更新已经加载到内存当中的授权信息，使得修改的授权信息生效。另外，`quit`用于退出 MariaDB，也可以使用`exit`或者`Ctrl+D`组合键退出。注意到每条语句使用`;`结束，回车换行不会被解析为语句结束，也可以使用`\g`来结束语句(go)。

用户创建成功后，即可使用

```bash
$ mysql -u oncemore -p
```

登入新建的用户。

### 配置选项

前面已经见过了`-u`、`-p`等命令行选项，`-u`选项表示登录服务器的用户名，`-p`表示通过命令提示符输入用户密码。使用`mysql --help`可以获得完整的选项列表。需要注意的是，可以通过`-p[password]`或者`--password=[password]`来登录而不是通过命令提示输入密码，但是不建议这样做，因为系统中的其他用户能够通过`ps`指令查看到你的登录指令从而轻易获取到密码。默认情况下表示连接本地(`localhost`)的MySQL服务器，也可通过`-h`选项来指定其他主机。在使用`localhost`时，MySQL使用Unix域套接字文件而不是TCP/IP协议来建立连接，这时可通过`-S file_name`或者`--socket=file_name`来指定套接字文件，在ArchLinux下默认使用`/run/mysql/mysql.sock`。

如果尝试直接运行`mysql`，会报错

```
$ mysql
ERROR 1045 (28000): Access denied for user 'guanhao'@'localhost' (using password: NO)
```

而忽略掉某些选项时（`'-h'`）却不会报错，因为某些选项可以直接使用默认值，并且这些默认值可以通过配置文件来配置。MariaDB 按照以下顺序读取配置文件（`mysqld --help --verbose`输出的前几行有说明）：

1. `/etc/my.cnf`
2. `/etc/mysql/my.cnf`
3. `~/.my.cnf`

不同位置的配置文件具有不同的作用范围，`~/.my.cnf`位置在用户各自的家目录，供系统用户配置自己的MySQL选项，而前两个配置文件由系统管理员用于配置系统全局选项。使用`mysqld --print-defaults`可以打印当前的配置。

如果需要直接使用`mysql`指令登录，在`~`创建一个`.my.cnf`文件，插入以下文本即可。出于安全考虑，还是建议不要将密码以明文形式存储。

```
[client]
host = localhost
user = oncemore
password = 666666
```

注意到`[client]`是配置文件的一个组，表示MySQL客户端建立连接相关的配置，此外还有`[mysql]`、`[mysqld]`等组。此外，还需要注意的细节包括：

* 用`#`、`;`表示注释
* 如果配置值包含空格，需要用`"`包围起来
* 后出现的配置会覆盖之前的出现的配置
* 命令行选项优先级高于配置文件选项，如使用`mysql -u root -p`会忽略配置文件内指定的用户信息

最后，最好给配置文件设置合适的权限，放置其他用户修改

```bash
$ chmod 600 ~/.my.cnf
```

### 创建数据库

创建数据库和表并插入数据，需要用到的语法：

{:.table .table-bordered .table-hover .table-striped}
|语法|作用|
|:---|----:|
|`CREATE DATABASE`|创建数据库|
|`CREATE TABLE`|创建表|
|`INSERT INTO`|插入一行数据|

示例（首先使用`oncemore`账户连接SQL服务器）：

```bash
MariaDB [(none)]> CREATE DATABASE mydb;
Query OK, 1 row affected (0.00 sec)
MariaDB [(none)]> USE mydb;
Database changed
MariaDB [mydb]> CREATE TABLE langs (name VARCHAR(20), level INT);
Query OK, 0 rows affected (0.23 sec)
MariaDB [mydb]> INSERT INTO langs (name, level) VALUES('cpp',60);
Query OK, 1 row affected (0.01 sec)
MariaDB [mydb]> INSERT INTO langs (name, level) VALUES('python',70);
Query OK, 1 row affected (0.03 sec)
MariaDB [mydb]> INSERT INTO langs (name, level) VALUES('javascript',NULL);
Query OK, 1 row affected (0.03 sec)
MariaDB [mydb]> SELECT * FROM langs;
+------------+-------+
| name       | level |
+------------+-------+
| cpp        |    60 |
| python     |    70 |
| javascript |  NULL |
+------------+-------+
3 rows in set (0.03 sec)
```

说明：创建了 `mydb` 数据库（之前已授权），在`mydb` 内创建了表`langs`，插入了三行（cpp,python,javascript)。注意`NULL`表示未知值（空值）。最后使用`SELECT * from` 语法打印整个`langs`表，如果某些表项过长导致输出阅读困难，可以使用`\G`作为语句结束，纵向地打印表项，将每列的值分布到单独的行显示，在启动`mysql`时加上`-E`或者`--vertical`选项可以对整个会话生效。

### 执行方式

除了使用`mysql`指令建立连接然后一句一句地输入语句执行之外，还可以通过命令行直接执行语句，这时需要给`mysql`指令加上`-e`选项，多条语句之间使用`;`分隔，如

```bash
$ mysql -e "SELECT COUNT(*) from langs;SELECT NOW();" mydb
+----------+
| COUNT(*) |
+----------+
|        3 |
+----------+
+---------------------+
| NOW()               |
+---------------------+
| 2016-04-21 16:12:08 |
+---------------------+
```

除此之外，当然还可以像其他编程语言一样，将SQL语句存储到一个单独的文件中，然后使用`mysql`读取文件内的语句（当然，如果可以读取文件，那也可以读取其他程序的输出）。

## 参考文章

3. [MariaDB - Wikipedia](https://zh.wikipedia.org/wiki/MariaDB)
1. [MySQL - ArchWiki](https://wiki.archlinux.org/index.php/MySQL)
2. [mysqld Configuration Files and Groups](https://mariadb.com/kb/en/mariadb/mysqld-configuration-files-and-groups/)
4. [MySQL CookBook, 3rd Edition](http://shop.oreilly.com/product/0636920032274.do)
