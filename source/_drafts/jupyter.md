## 安装配置

```shell
# 直接以docker的方式安装
docker run -d -p 8888:8888 --user root jupyter/tensorflow-notebook
```

## 运行

```shell
jupyter run notebook.ipynb # 可以直接在命令行运行指定的文件
```

## 语法

### 安装第三方库

```shell
! pip install matplotlib	# 在命令前面加上一个感叹号即可
```

