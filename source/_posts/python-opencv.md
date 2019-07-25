---
title: "Python OpenCv使用手册"
date: 2019-07-25 21:32:00
categories: python
---

## 图片属性获取

### 获取图片大小

```python
img.shape	# 返回一个元组(height, width, pixels)
```

## 图片常用操作

### 伸缩/压缩图片

```python
img = cv2.imrerad('input.png')
img2 = cv2.resize(img, (512, 512), interpolation=cv2.INTER_CUBIC)
```

#### 裁剪图片

```python
img2 = img[0:128, 0:512]	# 四个点都必须为整数
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

