---
layout: post
title: 加班时，记得为家里的她点亮一盏灯
modified: 2017-12-10
feature: true
tags: [Everglow]
description: The night is dark and full of terrors, but love burns them all away.
---

最近加班多，回家迟，希望家里能有一盏灯，在她打开门的那一刻，自动点亮，驱除黑暗。

### 物料清单

1. 树莓派
2. USB供电装饰灯
3. 红外感应模块

### 连线

![]({{ site.qnurl }}/media/ir_light_ctrl/ir_sensor.png){:.img-fluid .rounded .mx-auto .d-block}

红外感应模块的 VCC 连接树莓派 3.3V 针脚，GND 连接 GROUND 针脚，REL 连接 GPIO 3 号针脚（物理编号）。树莓派的 GPIO 针脚编号分为 _GPIO编号_ 和 _物理编号_ 两种，这里使用物理编号，即 REL 连接 5 号针脚。

![]({{ site.qnurl }}/media/ir_light_ctrl/physical-numbers.png){:.img-fluid .rounded .mx-auto .d-block}

装饰灯连接树莓派的 USB 端口 2

![]({{ site.qnurl }}/media/ir_light_ctrl/rasp_usb_port.jpg){:.img-fluid .rounded .mx-auto .d-block}

### 程序控制

#### 控制思路

红外感应模块感应到有人体靠近时，会在 REL 输出高电平，使用这个信号来控制 USB 口的供电，进而控制装饰灯的熄灭和点亮。

#### USB 端口供电控制

USB 端口控制，采用 [hub-ctrl](https://github.com/codazoda/hub-ctrl.c) 来实现。

打开 USB 端口 2 供电

```bash
./hub-ctrl -h 0 -P 2 -p 1
```

关闭 USB 端口 2 供电

```bash
./hub-ctrl -h 0 -P 2 -p 0
```

#### 自动控制USB端口供电

当检测到 GPIO 5 号针脚高电平时，打开 USB 端口 2 供电，并延时 5 秒，当 GPIO 5 号针脚低电平时，关闭 USB 端口 2 供电。16 行的 Python 程序可以轻松地帮我完成这个控制流程。

```python
import RPi.GPIO as GPIO
import os
import time

def task_entry():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(5, GPIO.IN)
    while(True):
        if GPIO.input(5) == 1:
            os.system('/home/guanhao/usb_hub/hub-ctrl -h 0 -P 2 -p 1')
            time.sleep(5)
        else:
            os.system('/home/guanhao/usb_hub/hub-ctrl -h 0 -P 2 -p 0')

if __name__ == '__main__':
    task_entry()
```

### 效果

动图为开门后，自动触发装饰灯点亮的效果图

![]({{ site.qnurl }}/media/ir_light_ctrl/light_on.gif){:.img-fluid .rounded .mx-auto .d-block}

> The night is dark and full of terrors, but love burns them all away.
