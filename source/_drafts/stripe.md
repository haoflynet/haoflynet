- [测试卡号及账号](https://stripe.com/docs/testing)

## [stripe API](https://stripe.com/docs/api)

- API 是`server`端用来管理的

### 主要的资源

#### Balance

- 可以获取当前账号的余额，和控制台的`Balances`数据一样

#### Balance Transactions

- id开头是`txn`

- 交易记录，对应控制台`Payments->All transactions`，`charge`也是这里

#### Charges

- id开头是`ch_`
- 对信用卡/借记卡进行收费，这个对应的也是控制台`Payments->All transactions`，对，创建了一个`charge`后就能在这里看到了
- `charge`的`customer`可能为空，可能只是用卡片支付了一下，没有创建`customer`

#### Customer

- id开头是`cus_`

- 管理用户(增删改查)，能获取到用户的`email`、`name`、`default_source(默认的支付方式(card_id)source)`

#### Disputes

- 纠纷、争议

#### Events

#### Files

#### File Links

#### Mandates

#### PaymentIntents

- 表示一个客户付款的全过程，建议为每个订单或会话创建一个`PaymentIntent`，当失败的时候还能用来重试

#### SetupIntents

- 这个应该可以不用

#### Payouts

- 提现
- 在`Settings/Payout settings`可以进行设置添加银行账户，并且每种货币对应一个账户，必须提供银行卡，并且和`customer/accounts`都没有关联，只能提现到自己的银行卡，而且还不能使用测试的银行账户
- 可以在控制台设置定时任务自动提现
- 这个接口还能添加第二个参数，指定stripeaccount，用于关联账户的体现:

```javascript
const payout = await stripe.payouts.create({
  amount: 1000,
  currency: 'usd',
}, {
  stripeAccount: '{{CONNECTED_STRIPE_ACCOUNT_ID}}',
});
```

#### Products产品

- 产品

#### Prices价格

- id开头是`price_`，和产品相关联的

#### Refunds退款

```javascript
// 对某次charge发起退款
charge = await stripe.charges.refund(charge.id, {
	amount: 1000
});
```

#### Tokens

### 支付方式管理

#### PaymentMethods

#### Bank Accounts

- 能够获取指定customer的sources(即信用卡详情)，这些就是客户的支付方式

#### Cards

- 这也是用户的卡片，和`Bank Accounts`接口是一样的

#### Sources

- 这才是真正的卡吧

### 支付

#### Sessions

### 记账(BILLING)

### CONNECT

#### Accounts

- 和`Customer`不同的是，`Accounts`是当前账户支付钱给他们，而`Customer`是他们支付给当前账户
- `Account`有三种: Custom/Standard/Managed

- 控制台有个[Connected accounts](https://dashboard.stripe.com/test/connect/accounts/overview)，好像就是转账给供应商或者服务提供商的，每个服务商会有一个account，里面那个示意图比较能说明其含义，提供服务的是第三方，相当于做了一个外卖系统，我们自己是外卖系统，客户是点餐的人，account就是商家
- 控制台居然还能设置关联账户的提现方式Payout，是自动按周期提现还是通过API提现还是在控制台手动提现，可以用`accounts.update`接口来设置其payouts的方式

- 表示一个`stripe`账户，你当前登陆的 就是一个`account`
- 要创建`Account`的话，必须在`Connected accounts`里面启用才行
- 需要注意使用API创建了用户，还有一些详细信息必须填入(这个可以在控制填写)，但是最后有一个`terms of service`必须使用API来`update`

```javascript
const account = await stripe.accounts.create({
  type: 'custom',
  country: 'US',
  email: 'test@example.com',
  capabilities: {
    card_payments: {requested: true},
    transfers: {requested: true},
  },
});

await stripeClient.accounts.update(
  account.id,
  {
    tos_acceptance: {	// 表示用户同意terms of service
      date: 1609798905,
      ip: '8.8.8.8'
    },
    settings: {	// 更新提现方式
      payouts: {
        schedule: {
          interval: 'manual',
        },
      },
    },
  }
);
```

#### External Accounts

- 关联账户的银行卡信息

```javascript
const bankAccount = await stripe.accounts.createExternalAccount(
  'acct_xxxxxxx',
  {
    external_account: 'btok_前端的stripe.js的token',
  }
);
```

#### Transfers转账

- 将资金从`Stripe`账户发送到关联的账户
- 和`Payouts`不同的是`Payouts`表示将钱从`Stripe`转移到您的账户或借记卡，而`transfer`则是将钱转移到关联的账户，相当于(payout是提现到银行，而transfer则类似于支付宝用户之间的互相转账，钱一直在stripe里面的，没有到银行)
- 需要要创建一个新的`transfer`对象，转出金额必须大于余额，否则会报错`Insufficient Funds`
- 不能给`customer`转
- 创建完成后能够在`Connected accounts -> ACCOUNT -> Activity Transfers`里面看到，或者在`Payments -> Transfers`里面
- 创建了`transfer`以后，当前账户里面的钱`Balances`立马就少了

```javascript
const transfer = await stripe.transfers.create({
  amount: 23,
  currency: 'usd',
  destination: 'acct_xxxxxxxxx',
  transfer_group: 'ORDER_95',
});
```

### FRAUD

### ORDERS

### webhook

## Webhooks

- 入口在`Developers -> Webhooks`，添加endpoint即可，里面有很多的事件可以选择

## 参考

- [nextjs-subscription-payments](https://github.com/vercel/nextjs-subscription-payments): 基于Next.js和stripe的订阅支付完整应用程序