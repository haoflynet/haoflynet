---
title: "树莓派控制GPIO电路"
date: 2017-11-06 19:52:39
updated: 2017-11-06 20:54:00
categories: 平凡之路
---

最近在尝试用树莓派通过继电器来控制家庭电路的实验，所以学习了一下树莓派的GPIO控制，发现真的超级简单。

关于树莓派GPIO针脚的图解可以参考这张图片(图片来自https://raw.githubusercontent.com/wiki/Yradex/RaspberryPi3_OS/GPIO.png)。每个针脚的详细解释可以参见(https://pinout.xyz/pinout)

![](http://ojccjqhmb.bkt.clouddn.com/raspberry-gpio.png)

### 使用Python控制继电器

首先需要安装GPIO控制库: `pip install RPi.GPIO`

```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pin = 17

GPIO.setup(pin, GPIO.OUT)	# 每次输出信号前需要先设置信号输出
GPIO.output(pin, GPIO.HIGH)	# 输出高电平

GPIO.setup(pin, GPIO.OUT)
GPIO.setup(pin, GPIO.LOW)	# 输出低电平
```

### 使用GPIO控制继电器

1. 关于继电器的输入输出以及信号控制端，可以参考[极客机械扫盲](http://haofly.net/%E6%9E%81%E5%AE%A2%E6%9C%BA%E6%A2%B0%E6%89%AB%E7%9B%B2/index.html)。
2. 将树莓派的5V输出端以及Ground端分别连接继电器的VCC和GND端。
3. 将树莓派的某一个GPIO针脚连接继电器的某一个信号输入端。
4. 通过Python控制即可，Just like this。![](http://ojccjqhmb.bkt.clouddn.com/raspberry-gpio_0.JPG)

