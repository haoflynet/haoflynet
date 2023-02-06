- 一个用于认证美国银行账户的平台
- 前后端的库有很多，一定要选择对，可以参考[这里](https://plaid.com/docs/api/libraries/#link-client-sdks)                          
- 几种支持的payment类型:
  - ACH: 美国，美国的银行标识号就是routing numbers
  - EFT：加拿大
  - BACS：英国
  - IBAN/SIC：欧盟
- 感觉主要的流程就是后端生成link token，前端用link token初始化link component，用户输入自己的认证信息，成功就生成public token，后端再用public token获取access token
- sandbox测试账户：[Sandbox test credentials](https://plaid.com/docs/sandbox/test-credentials/)

## API

### Auth

```javascript
const request: AuthGetRequest = {
  access_token: accessToken,
};

try {
  // 获取银行账户信息(bank account)和标识号(identification numbers)
  const response = await plaidClient.authGet(request);
  const accountData = response.data.accounts;	// 银行账户信息
  const numbers = response.data.numbers; // identification numbers信息
} catch (error) {
}
```

### Link Token

- 需要在后端创建link token，前端才能用这个token与plaid交互，即前端初始化Link这个component

```javascript
const request = {
  user: {
    client_user_id: user.id,	// 可以直接用你系统中的用户的id，主要是要保持唯一
  },
  client_name: 'Plaid Test App',
  products: ['auth'],
  language: 'en',
  webhook: 'https://webhook.example.com',
  redirect_uri: 'https://domainname.com/oauth-page.html',
  country_codes: ['US'],
};
try {
  const createTokenResponse = await client.linkTokenCreate(request);
  response.json(createTokenResponse.data);
} catch (error) {
  // handle error
}
```

### Access Token

- 后端用前端的publick token置换出access token

```javascript
const response = await client.itemPublicTokenExchange({
  public_token: publicToken,
});
const accessToken = response.data.access_token;
const itemID = response.data.item_id;
```

### accountsGet

- 获取accounts详情

```javascript
const accountsResponse = await client.accountsGet({
  access_token: accessToken,
});
response.json(accountsResponse.data);
```

## 前端集成

- 后端提供创建link token的接口，然后前端可以直接参考这样用[simple.tsx](https://github.com/plaid/react-plaid-link/blob/ca3a9167db880ba080e2bf77047f7cf0f1f59d33/examples/simple.tsx)

