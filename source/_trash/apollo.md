## 安装和配置

- 官方文档居然都是讲在React中怎么用的，如果不依赖于React只需要从core里面引入client即可`import { ApolloClient } from '@apollo/client/core';`

```javascript
const client = new ApolloClient({
  uri: 'http://localhost:1337/graphql',
  cache: new InMemoryCache(),
  headers: {
    authorization: 'token'
  }
})
```

## 查询

```javascript
await client.query({
  query: gql`
		products {
			id
		}
  `
})
```









如果想要知道用户查询的字段可以用graphql-tools的addSchemaLevelResolveFunction，在里面用[graphql-parse-resolve-info](https://www.npmjs.com/package/graphql-parse-resolve-info)如果添加这个方法不行就试着让info到handler里面去，我最终在experss-graphql了然后自己直接用[graphql-parse-resolve-info](https://www.npmjs.com/package/graphql-parse-resolve-info)



https://www.apollographql.com/docs/apollo-server/api/graphql-tools/