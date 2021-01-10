---
title: "Cloudinary 使用手册"
date: 2019-09-05 14:40:00
categories: Javascript
---

# Deliver remote media files

不用API直接传照片到cloudinary，可以限制domain

https://res.cloudinary.com/demo/image/fetch/https://upload.wikimedia.org/wikipedia/commons/1/13/Benedict_Cumberbatch_2011.png

直接后面跟自己真实的图片路径即可





动词：

w_400,h_400	限制高度和宽度

c_crop

c_fill

c_scale

c_thumb

f_auto，默认值，应该是会根据客户端的不同选择，web端反正选这个就是webp，非常棒

f_png, 意思是fetch_format，获取到的图像的格式，远端如果是jpg，也可以转换成png

g_face

g_south_east

o_90

r_max