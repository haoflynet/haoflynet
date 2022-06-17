如果超过10秒没有输入流live555 error，会自动断开，可以添加--loop参数



vlc -vvv --loop



vlc input.mp4 -vvv --loop --sout "#rtp{sdp=rtsp://192.168.9.80:10086/stream}" 	# 将输入流转换为输出流rtsp，可以直接用vlc播放器进行播放



如果输入流为rtp，那么案例说应该是vlc rtp://127.0.0.1:5001,但是会说需要sdp

那么创建一个sdp文件，例如 test.sdp，内容如下

```
c=IN IP4 192.168.9.80	# 这是输出的IP地址
m=video 5004 RTP/AVP 96 
a=rtpmap:96 H264/90000
```

