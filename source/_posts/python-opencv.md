---
title: "Python OpenCv使用手册"
date: 2019-07-25 21:32:00
updated: 2020-07-26 09:53:00
categories: python
---

## 图片属性获取

### 获取图片大小

```python
img.shape	# 返回一个元组(height, width, pixels)
```

## 图片常用操作

### 显示图片

```python
# 如果不加后面那两行，可能显示的图片是纯黑色的，无法正常显示
cv2.imshow('窗口名',image)
cv2.waitKey(0)  
cv2.destroyAllWindows()
```

### 伸缩/压缩图片

```python
img = cv2.imrerad('input.png')
img2 = cv2.resize(img, (512, 512), interpolation=cv2.INTER_CUBIC)
```

### 裁剪图片

```python
img2 = img[0:128, 0:512]	# 四个点都必须为整数
```

### 图片匹配/查找子图片出现位置

```python
# 以下代码来自https://stackoverflow.com/questions/50579050/template-matching-with-multiple-objects-in-opencv-python/58514954#58514954
import cv2
import numpy as np
import time

image = cv2.imread('smiley.png', cv2.IMREAD_COLOR )
template = cv2.imread('template.png', cv2.IMREAD_COLOR)

h, w = template.shape[:2]
method = cv2.TM_CCOEFF_NORMED
res = cv2.matchTemplate(image, template, method)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)	# 其中max_loc就是子图片的左上角的横纵坐标位置

# 如果想匹配多个，可以用下面这种方法
threshold = 0.90	# 设定一个最小的匹配度，所有匹配都有一个匹配度，从高往低计算
max_val = 1
while max_val > threshold:
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val > threshold:
        res[max_loc[1]-h//2:max_loc[1]+h//2+1, max_loc[0]-w//2:max_loc[0]+w//2+1] = 0   
        image = cv2.rectangle(image,(max_loc[0],max_loc[1]), (max_loc[0]+w+1, max_loc[1]+h+1), (0,0,0) )

cv2.imwrite('output.png', image)	# 这里会把匹配到的地方都标上黑框标记
```

## 视频常用操作

### 获取视频帧率帧数

```python
movie = cv2.VideoCapture('test.mp4')
movie.get(cv2.CAP_PROP_FRAME_COUNT)	# 帧数
movie.get(cv2.CAP_PROP_FPS)	# 帧率
movie.release()
```

### 逐帧遍历

```python
while True:
  ret, frame = movie.read()
  if not ret:
    break
  cv2.imwrite('filename.png', frame)	# 将该帧以图片的形式保存下来
```

### 跳转到指定帧

```python
movie.set(cv2.CAP_PROP_POS_FRAMES, 233)
ret, frame = movie.read()
```

