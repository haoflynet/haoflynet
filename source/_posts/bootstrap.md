---
title: "BootStrap wiki"
date: 2015-02-20 08:30:39
categories: frontend
---
# Bootstrap
Bootstrap是由Twitter退出的一个用于前端开发的开发工具包，其中包含了许多简洁大方的css样式和实用的js插件，当然，它是移动设备优先的响应式开
发方式。



##  特殊功能(使用Tips)

- 下拉选择列表(需要bootstrap.js)：

      <div class="form-group">
        <label for="sel1">Select list:</label>
        <select class="form-control" id="sel1">
          <option>1</option>
          <option>2</option>
          <option>3</option>
          <option>4</option>
        </select>
      </div>
- input的属性(居然没有哪个地方写了的，我也是醉了，难道只有我没有找到，还是只有我什么基础都没有还来用bootstrap):

      <input placeholder="Enter email">   placeholder属性表示在输入框内预先显示的文字
      <input type="email">  type会影响到该输入框的展现形式，它的值可以是checkbox、email、file、password、text(文本输入框)
      <input class="form-control"> input只有加了这个类才会呈现得好看一点，并且默认宽度会变成100\%
- 表单里面点击按钮禁止跳转，不要讲button的type设置为subbmit或者不设置，必须将其设置为`type="button"`才不会强制刷新当前页面

## 常用网址

**百度的CDN**： <http://apps.bdimg.com/libs/bootstrap/3.3.0/css/bootstrap-theme.min.css> <http://apps.bdimg.com/libs/bootstrap/3.3.0/css/bootstrap.min.css> [http://apps.bdimg.com/libs/bootstrap/3.3.0/js/bootstrap.min.js ](http://apps.bdimg.com/libs/bootstrap/3.3.0/js/bootstrap.min.js)**全局CSS样式**：[http://v3.bootcss.com/css/ ](http://v3.bootcss.com/css/)**组件**：[http://v3.bootcss.com/components/ ](http://v3.bootcss.com/components/)**JavaScript插件**：[http://v3.bootcss.com/javascript/ ](http://v3.bootcss.com/javascript/)**jQuery UI Bootstrap**：[http://www.bootcss.com/p/jquery-ui-bootstrap/ ](http://www.bootcss.com/p/jquery-ui-bootstrap/)**Glyphicons字体图标**：[http://v3.bootcss.com/components/#glyphicons ](http://v3.bootcss.com/components/#glyphicons)**实例精选(几个简单的模板)**：<http://v3.bootcss.com/getting-started/#examples>
