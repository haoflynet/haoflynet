session写入失败

```php
A PHP Error was encountered

Severity: Warning

Message: mkdir(): Invalid path
```

可能之前设置的是window或者其他没有权限的路径，可以这样配置$config['sess_save_path'] = sys_get_temp_dir();





https://gist.github.com/yidas/30a611449992b0fac173267951e5f17f



# Codeigniter 3 server configuration for Nginx & Apache

## 