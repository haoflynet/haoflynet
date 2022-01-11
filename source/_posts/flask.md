---
title: "flask 教程"
date: 2015-11-07 05:02:39
updated: 2021-01-07 17:43:00
categories: python
---

## 基本框架

[项目常用项目结构](https://github.com/haoflynet/project-structure/blob/master/Flask/README.md)

```python
from flask import Flask, request
app = Flask(__name__)
	
@app.route('/', methods=['GET', 'POST'])	# 定义仅接收哪些类型的请求
def hello():
    if request.method == 'POST':
        return "POST"
    return "Hello World!"

  
  
# 带参数的路由
@app.route('/<username>')
def func(username)
@app.route('/post/<int:post_id>')
	
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
```

但是，业界普遍认为，`tornado`与`flask`同时使用能够同时发挥两个框架的有点，前者用于异步处理高并发请求，后者便于编写，这时候`torando`作为一个`httpserver`对外提供http访问，`flask`比`tornado`更加简单易用，只是因为`flask`在生产环境是需要`WSGI server`的，所以`Tornado`是非常适合的，至少比`Apache`作为server好，而前面的`nginx`也只是作为负载。`Flask's build-in server is not suitable for production as it doesn't scale well and by default serves only one request at a time`[——Deployment Options](http://flask.pocoo.org/docs/0.11/deploying/)。

## 请求和响应
### request

```python
# 获取表单提交数据, 仅用于表单
request.form.get('begin', '')

# 获取POST数据
request.json
request.json.get('username')

# 获取GET参数
request.args.get('q', '')

# 处理get请求
data = request.get_json(silent=False)

# 获取header头
request.headers.get('Auth-Token')

# 获取用户真实IP
if request.headers.getlist('X-Forwarded-For'):
	ip = request.headers.getlist('X-Forwarded-For')[0]
else:
	ip = request.remote_addr
```
### resposne

```python
# 返回指定状态码
return make_response(jsonify({'a': 'b'}), 201)
return jsonify({'a': 'b'}), 201	# 也可以简单点这样做

# 返回JSON数据
from flask import jsonify
return jsonify(username=g.user.username, email='asd')
return jsonify({'username': g.user.username})

# 允许CORS，可以使用flask-cors库，也可以全局设置如下这个
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

## 如果仅针对单独的接口，可以添加装饰器，当然，该接口必须允许OPTIONS请求，才能直接返回请求
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,PATCH'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun
```

## 数据库
使用`flask-sqlalchemy`操作数据库，具体文档可以参考[SQLAlchemy手册](https://haofly.net/sqlalchemy)。`flask-sqlalchemy`帮我们做了很多我们其实不用关心的操作，例如自动新建和关闭`session`，但是需要注意的是，`flask-sqlalchemy`默认会在每次使用session的时候开启一个事务，每次请求完成自动结束事务，所以千万不要用它来运行长任务，否则事务一直不关闭，会导致表级锁，无法对表进行操作

## 常用扩展

#### flask-jwt-extended

- jwt扩展

```python
token = create_access_token(identity={'id': 1, 'role': 'admin'})

@app.route(...)
@jwt_required()	# 必须在路由上加上这个装饰器
def test():
  user = get_jwt_identity()	# 直接获取identity的数据
  
# 顺便可以写个验证中间件
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        if user.get('role') != 'admin':
            return jsonify({'error': 'Admin only operation'}), 401
        return func(*args, **kwargs)
    return wrapper
```

#### flask-bcrypt

- bcrypt扩展，加密密码用

#### flas-socketio

```python
socketio = SocketIO(app, cors_allowed_origins='*')	# 允许跨域cors
```

## TroubleShooting

- **AssertionError: View function mapping is overwriting an existing endpoint function: main**: 原因可能是在给控制器函数添加装饰器的时候没有重新定义其名称，导致每个使用该装饰器的控制器的签名都一样了，可以这样设置控制器:

  ```python
  def route_decorator(func):
      def wrapper():
          try:
              return func()
          except Exception as e:
              print(str(e))
              return {"message": str(e), "success": False, "code": 500}
      wrapper.__name__ = func.__name__	# 需要将签名设置为和以前的函数签名一致
      return wrapper
  ```

  