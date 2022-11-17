## 安装配置

```python
pip3 install -U uiautomator2

import uiautomator2 as u2

d = u2.connect()	# 连接设备
```

## 常用方法

### 系统信息

```python
d.info	# 输出设备信息，包括currentPackageName当前运行的包名

d.implicitly_wait(20.0)	# 设置元素的查找等待时间，默认是20秒
print(d.implicitly_wait())
```

### 交互

```python
d.app_start("com.smzdm.client.android")	# 打开APP
d.app_start("com.smzdm.client.android", ".app.WelComeActivity")	# 打开APP指定的activity
d.app_stop("com.example.hello_world") # 关闭APP
d.app_stop_all()	# 停止所有运行中的APP


d.click(100, 200)	# 直接点击屏幕的坐标
d(text="允许").click()	# 点击屏幕中的文字
```

