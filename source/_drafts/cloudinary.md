---
title: "Cloudinary 使用手册"
date: 2019-09-05 14:40:00
categories: Javascript
---

# Deliver remote media files

- 不用API而是直接通过URL自动将照片传到到cloudinary，可以限制domain，直接后面跟自己真实的图片路径即可。例如:

  https://res.cloudinary.com/demo/image/fetch/https://upload.wikimedia.org/wikipedia/commons/1/13/Benedict_Cumberbatch_2011.png

- 设置方法: `Settings -> Security`然后将指定的域名添加到`Allowed fetch domains`，然后Save即可







动词：

w_400,h_400	限制高度和宽度

c_crop: 裁剪，https://res.cloudinary.com/demo/image/upload/w_300,h_200,c_crop/sample.jpg

c_fill

c_scale

c_thumb

f_auto，默认值，应该是会根据客户端的不同选择，web端反正选这个就是webp，非常棒

f_png, 意思是fetch_format，获取到的图像的格式，远端如果是jpg，也可以转换成png

g_face

g_south_east

o_90

r_max: r_圆角，max表示直接把图片裁剪成圆形，r_50,r_20等



mp4只有声音，尝试加上c_scale,w_1280参数试试



django使用

```
image = CloudinaryField(
    "Image",
    overwrite=True,
    resource_type="image",
    transformation={"quality": "auto:eco"},
    format="jpg",
)
```



## TroubleShooting

- **API上传大文件报413错误，但其实并没有超过账户的limit**: 其实是因为sdk默认的`upload`方法最大只支持100MB，如果要上传超过100MB的文件需要分片上传，使用`upload_large`方法