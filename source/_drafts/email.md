---
title: "邮件/邮箱相关知识点 "
date: 2019-09-05 14:40:00
categories: Javascript
---

邮件的preheader默认取的是body中开头的字符，可以用hack的方式自定义 ,在body最开始加入下面的元素即可

```
<span class="preheader" style="display: none !important; font-size:0; line-height:0">
  To finish setting up your account, we need to verify your email address. Please click the button in this email to do so.
&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;
</span>
```