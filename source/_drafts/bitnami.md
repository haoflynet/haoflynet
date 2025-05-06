还不清楚这是个啥，反正很麻烦就是了

## 管理命令

```shell
sudo /opt/bitnami/ctlscript.sh status	# 查看状体啊
sudo /opt/bitnami/ctlscript.sh restart # 重启自身服务
sudo /opt/bitnami/ctlscript.sh restart apache	# 重启指定服务
```

## Apache

- 默认安装目录在`/opt/bitnami/apache2`，其访问日志也在`/opt/bitnami/apache2/logs`

```shell
sudo vim /opt/bitnami/apache2/conf/bitnami/bitnami.conf # 配置文件
sudo /opt/bitnami/ctlscript.sh restart apache # 重启apache
```

## MySQL

- [Bitnami管理MySQL文档](https://docs.bitnami.com/aws/infrastructure/mysql/)

- 卸载MySQL

  ```shell
  sudo /opt/bitnami/ctlscript.sh stop mysql
  sed -r 's/^(\[My|my)/\;\1/g' /opt/bitnami/properties.ini
  sudo mv /opt/bitnami/mysql /opt/bitnami/mysql-disabled
  ```

  
