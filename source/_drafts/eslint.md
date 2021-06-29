nodejs代码格式化

主要是用以下三个工具

- husky，git钩子，能够方便地在nodejs项目中配置git的hook操作
- lint-staged，对git暂存文件进行lint检查
- eslint，代码格式检测工具



eslint可以检测出代码问题，并标红，但是并不会自动格式化，需要手动格式化，介入Prettier并配置可以进行自动格式化。但是两者可能有冲突



cnpm install --save-dev  husky lint-staged eslint

eslint规则中文网站 https://cn.eslint.org/

单独执行estlint命令

eslint file.js# 仅校验

eslint --fix file.js	校验并尝试修改

.eslintrc.js文件

```text
"lint": "eslint --ext \".js\" src --fix"
```

 

初始化当前项目的eslint配置，./node_modules/.bin/eslint --init，能够通过交互式生成对应的配置文件：

```shell
? How would you like to use ESLint? …
  To check syntax only
❯ To check syntax and find problems
  To check syntax, find problems, and enforce code style
  
? What type of modules does your project use? # 项目中使用什么类型的模块
❯ JavaScript modules (import/export)	# vue一般选这个
  CommonJS (require/exports)
  None of these
  
? Which framework does your project use? # 项目中使用什么框架
❯ React
  Vue.js
  None of these
  
? Does your project use TypeScript? › No / Yes	# 项目是否使用TypeScript，如果是下面会安装typescript的eslint

? Where does your code run? …  (Press <space> to select, <a> to toggle all, <i> to invert selection)
✔ Browser
✔ Node

? What format do you want your config file to be in? …
❯ JavaScript
  YAML
  JSON
  
@typescript-eslint/eslint-plugin@latest @typescript-eslint/parser@latest
? Would you like to install them now with npm? › No / Yes
```

完成后会在根目录创建文件`.eslintrc.js`

```javascript
module.exports = {
    "env": {	// 想启用的环境
        "es2021": true,
        "node": true
    },
    "extends": [	// 从指定的插件中继承规则
        "eslint:recommended",	// eslint:all表示使用eslint的所有规则，可参考http://eslint.cn/docs/rules/，"eslint:recommended"表示使用eslint所有规则里面打勾的规则，"standard"表示使用standard的规则(需要先npm install standard --save-dev)，参考https://standardjs.com/rules-zhcn.html#javascript-standard-style。我比较习惯standard，还有arbnb风格
        "plugin:@typescript-eslint/recommended"	// 如果是typescript需要添加这个插件
    ],
    "parser": "@typescript-eslint/parser",
    "parserOptions": {
        "ecmaVersion": 12,
        "sourceType": "module"
    },
    "plugins": [	// 使用的额外的插件，例如下面的html插件和react插件
        "@typescript-eslint",
      	"html", // 用于html代码中的js代码校验，需安装eslint-plugin-html
      	"react", // 用于react代码的验证，需安装eslint-plugin-react
    ],
    "rules": { // 这里放自定义的规则，0表示关闭规则，1表示设置为warn，2表示error
      "@typescript-eslint/strict-boolean-expressions": 0, 	// 禁用布尔表达式中的严格类型判断，本来if(value)即使value为true或者为对象时都可以，但是如果这个规则为1，那么只能为true，必须单独处理null或者空字符串等情况，特别麻烦
      "@typescript-eslint/explicit-module-boundary-types": [
        "error",
        {	// 仅仅覆盖规则的某个选项
          "allowArgumentsExplicitlyTypedAsAny": true	// 也可以允许typescript中使用any来声明函数参数
        }
      ]
      "@typescript-eslint/no-explicit-any": 0,	// 禁用它可以允许typescript中使用any来声明类型
      "max-len": [
      	"error",
      	{
      		"code": 150	// 有些规则默认行宽只有80或者180，如果要更改该规则可以这样做
   	 		}
      ]
    }
};
```

除了使用rules来全局忽略某些配置以外，还能在局部忽略某些配置，例如: 

```javascript
// eslint-disable-next-line no-undef // 能忽略下一行出现的未定义错误，如cordova
cordova.plugins...

/* eslint-disable import/first */	// 这样注释能忽略当前文件下面所有行的指定的错误，这里是忽略import/first错误
```



然后在package.json中配置husky和lint-staged

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "src/**": [
      "eslint --fix",
      "git add"
    ]
  }
}
```

 最后git add . && git commit -m ''即可测试，这个时候代码有问题，就会报错





某些特定规则的常见解决办法：

1. # Requires Promise-like values to be handled appropriately (`no-floating-promises`)

   这是没有处理promise的结果和错误，例如

   ```javascript
   (async () => {
     ...
   })() // 需要加上下面的then和catch才能避免错误提示，也是一种很好的编码习惯
     .then(() => { console.log('Start Success') })
     .catch(() => { console.log('Start Failed') })
   ```

   2.Require statement not part of import statement.
   
   可以把`const path = require('path')`改为`import path = require('path')`
## Troubleshooting

- **ESLint: iterators/generators require regenerator-runtime, which is too heavyweight for this guide to allow them. Separately, loops should be avoided in favor of array iterations.(no-restricted-syntax)**: 这是`Airbnb`中的一条规则`no-restricted-syntax`会禁用一些新特性新语法，比如`for await ... in`，如果要禁用不建议在`rules`中整个禁用，直接在使用的地方加`// eslint-disable-next-line no-restricted-syntax`吧
- **lint-staged Node.js requirement to 12.13.0**: 最新版本的`lint-staged`要求node版本>=12.13.0，或者降级`lint-staged`
- **eslint.rc里面的excludes不起作用，tsc的时候仍然去检查了node_modeuls里面的东西**: 尝试升级`typescript`到3.9.* +
