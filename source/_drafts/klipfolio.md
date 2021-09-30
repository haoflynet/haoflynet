## Data Sources数据源

- 可以来自系统中已定义好的第三方服务，也可以直接来自于文件上传、API接口、SQL查询、FTP上传、Email附件

- 可以自定义时间去刷新(1h - 24h)，但是如果是文件上传这种是不能自动刷新的

- 可以支持参数，但是必须依赖于klip变量，例如，可以写成`https://haofly.net/{props.pageName}`，这里的`pageName`就是klip的变量，如果是第一次访问一个之前没有请求过的参数，那么可能会比较慢，后续的定时刷新也是可以起作用的，刷新的会把所有请求过的参数都请求一遍

- 如果要在`dashboard`上手动请求刷新data sources，可以直接data sources的请求刷新接口:

  ```javascript
  // 使用html component做一个刷新按钮，然后手动POST接口
  xmlHttp.open('POST', 'https://app.klipfolio.com/datasources/ajax_refresh_datasource', true);
  xmlHttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xmlHttp.send('di=&dsid=' + data source的id); // 这里加上di表示直接等待它完成，如果不加则是把它放入了刷新队列里面去
  ```

  



只有html component组件能够自己写js
https://support.klipfolio.com/hc/en-us/articles/215545798-How-to-build-HTML-Template-components#java



变量，自定义的变量好像只能在选择组件的时候新建和设置，都没有一个全局可以设置的地方

https://support.klipfolio.com/hc/en-us/articles/215547108#usevar
