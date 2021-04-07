.eslintrc.js文件

```text
"lint": "eslint --ext \".js\" src --fix"
```

 

```javascript
module.exports = {
  root: true,
  env: {	// 想启用的环境
    node: true,
    es6: true
  },
  extends: "standard",	// 从该插件中继承规则，"eslint:all"表示使用eslint的所有规则，可参考http://eslint.cn/docs/rules/，"eslint:recommended"表示使用eslint所有规则里面打勾的规则，"standard"表示使用starard的规则(需要先npm install standard --save-dev)，参考https://standardjs.com/rules-zhcn.html#javascript-standard-style
  plugins: [	// 使用额外的插件，如eslint-plugin-html、
    'html',	// 用于html代码中的js代码的验证
    'react',		// eslint-plugin-react，用于react代码的验证
    'standard',	// 也可以不用extends，而是直接写到standard里面来
  ],
  rules: {
    indent: ["error", 2],	// 自定义的规则
  }
}
```



