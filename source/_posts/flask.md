---
title: "flask 教程"
date: 2015-11-07 05:02:39
updated: 2017-10-09 23:07:00
categories: python
---

## 基本框架
```python
from flask import Flask, request
app = Flask(__name__)
	
@app.route('/', methods=['GET', 'POST'])	# 定义仅接收哪些类型的请求
def hello():
    if request.method == 'POST':
        return "POST"
    return "Hello World!"
	
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
```

但是，业界普遍认为，`tornado`与`flask`同时使用能够同时发挥两个框架的有点，前者用于异步处理高并发请求，后者便于编写，这时候`torando`作为一个`httpserver`对外提供http访问，`flask`比`tornado`更加简单易用，只是因为`flask`在生产环境是需要`WSGI server`的，所以`Tornado`是非常适合的，至少比`Apache`作为server好，而前面的`nginx`也只是作为负载。`Flask's build-in server is not suitable for production as it doesn't scale well and by default serves only one request at a time`[——Deployment Options](http://flask.pocoo.org/docs/0.11/deploying/)

## 项目结构

使用蓝图功能，方便模块化，不同的模块相当于不同的app：

	.
	├── app1
	│   ├── templates/		# 放置html模板，jinja2的模板
	│   ├── static/
	│   │   ├── css
	│   │   ├── js
	│   │   └── img
	│   ├── __init__.py
	│   ├── models.py
	│   └── views.py
	├── instance/
	│   └── config.py	# 不出现在版本控制中的机密配置变量，而且该文件可覆盖config.py里的配置，以保证安全，这样就可以将本地配置与线上配置分离了，instance文件夹是flask的特性
	├── migrations/
	├── tests/
	├── venv/
	├── requirements.txt
	├── config.py	# 一般是在__init__.py进行加载
	└── run.py

run.py的内容

	from flask import Flask
	from app1 improt app1
	from flask_sqlalchemy import 
	
	app = Flask(__name__, instance_relative_config=True)	# 第二个参数是为了加载instance文件夹
	
	app.config.from_object('config')	# 加载配置文件config.py，之后可以通过app.config['name']来访问对应的配置了，这和flask的配置是放在一起的，这里设置DEBUG就能影响到flask
	app.config.from_pyfile('config.py') # 这里是在加载instance文件夹下的配置，这样就可以覆盖config.py里面的配置了
	app.config['HOST']	# 这样子获取配置
	
	app.register_blueprint(app1, url_prefix='/app1')	# 可以指定前缀
	
	SQLAlchemy(app)	# 连接数据库，数据库的各项配置可直接写在config.py里面
	
	if __name__ == '__main__':
		app.run()

app1下的__init__.py:

	from flask import Blueprint
	assert = Blueprint('app1', __name__, template_folder='', static_folder='')
	
	import views

app1下的views.py:

	from flask import requests
	from app1 import app1
	
	@app1.route('/')
	def hello():
		return 'Hello World'

app1下的models.py

	from sqlalchemy import Column
	from flask_sqlalchemy import SQLAlchemy
	
	db = SQLAlchemy()
	
	class User(db.Model):		# 这样子定义	

配置文件的内容config.py:

	DEBUG = True
	BIND_HOST = '0.0.0.0'
	BIND_PORT = 5000
	
	SQLALCHEMY_DATABASE_URI = ''			# 在这里面写配置会直接连接
	SQLALCHEMY_ECHO = True                  # 测试用，输出所有的sql语句
	SQLALCHEMY_POOL_SIZE = 5                # 数据库连接池大小，默认5
	SQLALCHEMY_POOL_TIMEOUT = 10            # 超时时间，默认10
	SQLALCHEMY_POOL_RECYCLE = 2 * 60 * 60   # 连接回收时间，默认2小时
	SQLALCHEMY_TRACK_MODIFICATIONS = True   # 去除最新版本启用的warning
## 请求和响应
### request

	# 获取表单提交数据, 仅用于表单
	request.form.get('begin', '')
	
	# 获取POST数据
	request.json
	
	# 获取GET参数
	request.args.get('q', '')
	
	# 处理get请求
	data = request.get_json(silent=False)
	
	# 获取用户真实IP
	if request.headers.getlist('X-Forwarded-For'):
		ip = request.headers.getlist('X-Forwarded-For')[0]
	else:
		ip = request.remote_addr
### resposne

```python
# 返回JSON数据
from flask import jsonify
return jsonify(username=g.user.username, email='asd')
```

## 数据库
flask

## TroubleShooting
