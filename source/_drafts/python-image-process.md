```python
from PIL import Image

im = Image.open(path)
width, height = im.size	# 获取图片高度和宽度
im.show()	# 显示图片
im = im.transpose(Image.ROTATE_90)	# 图片旋转90度
im2 = im.crop((y1, x1, y2, x2))	# 图片切割
```

