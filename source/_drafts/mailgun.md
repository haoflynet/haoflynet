https://handlebarsjs.com/zh/guide/expressions.html#%E5%8A%A9%E6%89%8B%E4%BB%A3%E7%A0%81 

这是模板文档，官方的文档就随便写了两个。。。



## 模板语法

```handlebars
// 循环
{{#each users}}
	{{ name }}	// 直接取user.name
{{/each}}

{{#each myArr}}
	{{ myArr.[0] }}	// 直接取user.name
{{/each}}

// 判断
{{#if test}}
	{{ name }}
{{^}}	// else否则
  {{ name }}
{{/if}}
```

## 发送语法

```javascript
const data = {
  from: `Haofly <test@haofly.net>`,
  to: 'xxx@haofly.net',
  subject: 'Subject',
  template: 'template_name',
  'h:X-Mailgun-Variables': JSON.stringify({ test: 'test' }),	// 发送json格式的data，但是不能超过16kb
  attachment: Buffer.from(csvStr, 'utf8'),	// 如果发送attachment可以直接发送Buffer
};

await mailgunSender.messages().send(data, (error, body) => {});
```

