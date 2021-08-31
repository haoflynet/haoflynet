还不清楚这是个啥，反正很麻烦就是了

## MySQL

- 卸载MySQL

  ```shell
  sudo /opt/bitnami/ctlscript.sh stop mysql
  sed -r 's/^(\[My|my)/\;\1/g' /opt/bitnami/properties.ini
  sudo mv /opt/bitnami/mysql /opt/bitnami/mysql-disabled
  ```

  
