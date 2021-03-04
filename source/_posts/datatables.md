---
title: "Js强大的表格插件Datatables配置指南"
date: 2020-11-15 20:40:00
updated: 2021-03-01 12:41:00
categories: Javascript
---

## Datatables 安装

[简单的HTML方式使用](https://datatables.net/manual/installation)

[使用NPM的方式安装datatables](https://datatables.net/download/npm)

[官网的示例大全，可以在里面搜索到很多种使用场景](https://datatables.net/examples/index)

## Datatables 配置大全


```javascript
$('#exampleTable').dataTable({
  ajax: {
    url: '/getData',
    type: 'get',
    headers: {},
    data: function (data) {	// 修改或添加请求的参数，常用于自己写的搜索框
      data.searchName = 'xxxx';
    },
    dataSrc: function (res) {	// 修改接口返回的数据
     	res.data.map(item => {
        item.name = '<button>abc</button>';
      })
      return res.data;
    }
  },
  buttons: [{
    text: "Bulk Make as Completed",
    className: 'marked-as-complate-btn'
  }],
  columns: [	// 从数据源dataSrc中取哪些列进行展示
    { data: 'name' },
    { data: 'status' },
    { 
      className: 'test',	// 给某一列添加类
      data: 'id',	// 列的数据名
      orderable: true, // 是否允许排序
      render: function (data, type, row) {	// 给某一列单独添加渲染方式，而不是直接展示值
      	return '<input type="checkbox" class="form-control" value=' + row.value  +'>';
      },
      searchable: false,	// 是否允许过滤
      type: 'date',	// 设置该列的类型，例如date、num、num-fmt(比如货币等$100,000)、html-num、html-num-fmt、html、string
      visible: true,	// 设置列是否可见
      width: '20%', // 强行设置列的宽度，支持数字和CSS写法
    },
  ],
  columnDefs: [{	// 相当于批量设置columns
    targets: [0, 1],	// 多少列，这里表示第0列和第1列
    orderable: false	// 定义是否可以拖动排序
  }],
  createdRow: function (row, data, index) {
    $(row).addClass('test');
  },
  data: {},	// 以数组的方式设置初始化数据，当然一般还是用的ajax
  displayLength: 10, // 默认展示的每页的记录数
  /* dom：定义表哥的控制元素以什么样式显示
  		l - length：长度改变输入控制
  		f - filtering：过滤输入框
  		t - table：表格本身
  		i - information：信息概览元素
  		p - pagination：翻页控制元素
  		r - processing：处理中显示元素
  	Bootstrap 3的样式默认值为 
      "<'row'<'col-sm-6'l><'col-sm-6'f>>" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-5'i><'col-sm-7'p>>"
  	Bootstrap 4的样式默认值为
  		"<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
  		"<'row'<'col-sm-12'tr>>" +
  		"<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>"
  	jQuery UI的样式默认值为
  	  '<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-tl ui-corner-tr"lfr>'+
  		't'+
  		'<"fg-toolbar ui-toolbar ui-widget-header ui-helper-clearfix ui-corner-bl ui-corner-br"ip>',
  */
  dom: "<'row'<'col-sm-12 col-md-6'f>>" +
       "<'row'<'col-sm-12'tr>>" +
       "<'row'<'col-sm-12 col-md-2'l><'col-sm-12 col-md-2'i><'col-sm-12 col-md-8'p>>", // 这里分三个部分进行设置，第一个row表示标题头，第二个row表示table内容，第三个row表示底部信息栏
  drawCallback: function (settings) {	// 重新渲染完成后执行
  	var api = this.api();
    console.log( api.rows( {page:'current'} ).data() ); // 获取当前页码
  },
  info: true, // 是否显示总数信息
  language: {		// 对表格进行国际化
    emptyTable: '表中没有可用数据了',
    info: "_START_ - _END_ of _TOTAL_",	// 修改10 - 20 of 30文字
		infoEmpty: "没有记录",
    infoFiltered: "从 _MAX_ 条记录中过滤"
    lengthMenu: '每页显示 _MENU_ 条',	// show xx entries
    loadingRecords: '加载中',
    processing: '处理中',
    search: '搜索',
    zeroRecords: '没有找到符合提交的数据',
    paginate: {
   		first: '首页',
    	last: '尾页',
    	next: '下一页',
    	previous: '上一页'
  	}
  },
  lengthMenu: [10, 20, 50, 100],	// 允许用户选择每页的现实数量
  ordering: false,	// 全局控制整个列表所有列的排序功能
  paging: false,	// 是否开启分页
  /*
  分页按钮样式
  numbers：仅显示数字
  simple：只显示Previous和Next
  simple_numbers： 显示Previous、Next、总页数
  full：显示First、Previous、Next、Last
  full_number：显示First、Previous、Next、Last、总页数
  first_last_numbers：显示First、Last、总页数
  */
  pagintType: 'simple_numbers',	// 分页按钮的样式
  processing: true,	// 是否在数据加载时出现“Processing”的提示
  responsive: true,
  rowReorder: true,	// 和下面这个不同的是这个只是简单的允许拖动排序，仅仅是第一列可以拖动
  rowReorder: {	// 根据指定字段自动进行排序
    dataSrc: 'order',	// 指定排序字段
    selector: 'tr td:not(:last-child)'	// 指定可拖动的行元素，如果仅仅是'tr'，那么整行都是可以直接拖动的
  }
  scrollX: true,
  searching: false,	// 屏蔽搜索框
  serverSide: true,	// 是否服务器端分页
});
```

<!--more-->

## Datatables Event

### row-reorder

- 拖动重新排序以后

```javascript
table.on('row-reorder', function ( e, diff, edit ) {
	console.log(diff); // 可以看到排序有变化的行的当前位置和以前的位置
});
```

## Datatables API

```javascript
const datatable = $('table').DataTable();

datatable.rows().data();	// 获取json格式的表格数据

datatable.ajax.reload();	// 手动重新请求ajax
datatable.clear();	// 清空表数据
datatable.rows.add(data);	// 添加行
datatable.draw();	// 更改表数据后重新绘制

datatable.rows({search:'keyword'}).indexes(); // 搜索并返回搜索到的索引

// 根据条件移除某条数据
datatable.rows(function (index, data, node) {
  return data[0] === 3;
}).remove().draw();
```

## Datatables 服务端ajax接口

前端的请求参数有这些:

```json
{
 	start: 0,	// 当前页开始索引
  length: 10, // 当前页大小
  draw: 1, // 当前渲染序号(需要原样返回)
}
```

服务端只需要返回这样几个数据即可:

```json
{
  'draw': _GET['draw'],	// 请求时候的draw数字
  'recordsTotal': 100,	// 总量
  'recordsFiltered': 100, //筛选的总量
  'data': [{}],	// 当前页数据
}
```

## [laravel-datatables](https://github.com/yajra/laravel-datatables): laravel扩展

- 通常我们不会一次性查询出所有的数据让前端进行分页，而是后端直接返回分页后的数据，这时候在使用该扩展时需要这样设置:

```php
$data = Users::paginate();	// 分页查询后的结果
return DataTables::of($data->data)
            ->addIndexColumn()	// 添加索引列
            ->addColumn('name', function ($user) {	// 添加自定义的列
                return $user . '===';
            })
            ->setFilteredRecords(count($data->data))	// 设置当前页的条数
            ->setTotalRecords($data->total)	// 设置总的条数
            ->skipPaging() // 表示已经是分好页的数据，这个参数必须加上
            ->make(true);
```

## Troubleshooting

- **npm方式引入datatables时分页按钮没有样式**: 可能是没有引入button的css文件:

  ```javascript
  require('datatables.net');
  require('datatables.net-bs');
  require('datatables.net-bs/css/dataTables.bootstrap.css');
  ```