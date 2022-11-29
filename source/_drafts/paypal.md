## 支付Payment集成

### [内嵌HTML的方式](https://developer.paypal.com/api/nvp-soap/paypal-payments-standard/integration-guide/html-reference-landing/)

- 其实就是生成一个`paypal`的button，是非常安全方便的

#### [HTML表单](https://developer.paypal.com/api/nvp-soap/paypal-payments-standard/integration-guide/formbasics/)

- 直接放一个form表单，原理非常简单，我们甚至可以直接放一个`https://www.paypal.com/cgi-bin/webscr?后面各种参数`的url在自己的网页或者app里面

```html
<FORM action="https://www.paypal.com/cgi-bin/webscr" method="post">
    <input type="hidden" name="cmd" value="_xclick-subscriptions">	<!--cmd表示当前按钮的功能，_xclick-subscriptions表示创建一个订阅-->
  	<input type="hidden" name="custom" value="user_id"> <!--是一个非常重要的字段，可以用于我们存放自己系统的数据，比如放一个url，这样就能在创建成功的IPN或者hook里面获取到，能够安全地获取到正确的用户-->
  	<input type="hidden" name="notify_url" value="https://haofly.net">	<!--指定IPN地址，注意IPN在全局也有配置Business dashboard -> Account Settings -> Notifications，这里相当于一个单独的配置，paypal在支付成功后会调用这个地址，注意如果在这个地址上加参数依然是不安全的，因为IPN message里面并不包括这个-->
</FORM>
```

## 常用API

## 通知

### IPN(Instant Payment Notification)

- 需要在账户的后端控制台设置全局的，或者可以在表单的`notify_url`字段设置局部表单的IPN回调地址
- 支付直接通知，注意是以表单的方式提交的，不是json数据
- 收到消息需要验证，验证方式就是收到的时候将原数据拿来请求验证接口，[这里](https://developer.paypal.com/api/nvp-soap/ipn/IPNImplementation/#specs)有几种语言的验证实例

### Webhook

