sendgrid 手册

- 原来是可以看到日志的，在`Activity`菜单，只不过得先点一下search才行

## 安装配置

```shell
npm install --save @sendgrid/mail
```

### 域名认证

#### 通过DNS认证邮箱域名

- Would you also like to brand the links for this domain? 可以选择这个选项，选择后只需要设置DNS，对方收到邮件的发送者就是你自己的域名了，而不是`xxx@sendgrid.net`

#### Laravel使用sendgrid

- Laravel没有内置，但是可以用SMPT协议来发送，需要添加如下环境变量

```shell
MAIL_MAILER=smtp
MAIL_HOST=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=后台生成的apikey
MAIL_ENCRYPTION=tls
MAIL_FROM_NAME="John Smith"
MAIL_FROM_ADDRESS=from@example.com
```

## Sendgrid发送邮件

```javascript
const sgMail = require('@sendgrid/mail');

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const msg = {
  to: 'test@example.com',
  from: 'test@example.com', // Use the email address or domain you verified above
  subject: 'Sending with Twilio SendGrid is Fun',
  text: 'and easy to do anywhere, even with Node.js',
  html: '<strong>and easy to do anywhere, even with Node.js</strong>',
};

// 如果在后台定义好了邮件模板可以直接这样发送
const msg = {
    to: 'test@example.com',
    from: 'test@example.com',
    templateId: 'd-xxxxxxxxxxxxxxxxx',
    dynamicTemplateData: {	// 邮件模板里面的变量
        userName: 'abc',
    }
};

sgMail.send(msg).then(() => {})
```

### 邮件模板[handlebars](https://docs.sendgrid.com/for-developers/sending-email/using-handlebars)

- 需要注意的是如果是url等包含特殊字符的变量，需要用`{{{}}}`

```javascript
{{ username }}	// 变量
{{{ url }}}	// 包含特殊字符的变量

// if else 语法
{{#if user.profile.male}}
   <p>Dear Sir</p>
{{else if user.profile.female}}
   <p>Dear Madame</p>
{{else}}
   <p>Dear Customer</p>
{{/if}}
```