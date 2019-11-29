用FFmpeg从视频截取任意一帧图片

ffmpeg -i test.asf -y -f image2 -ss 00:01:00 -vframes 1 test1.jpg

```
ffmpeg -i 1.flv -filter_complex "delogo=x=1017:y=21:w=246:h=44" 2.flv  // 去除视频水印，简单地模糊一下，其中x和y是左上角的像素坐标，w表示宽度，h表示高度
```