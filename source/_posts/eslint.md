---
title: "Js代码格式化工具 - eslint的使用"
date: 2021-06-30 22:00:00
updated: 2022-02-12 08:30:00
categories: frontend
---

- 代码风格交给eslint，其他的不要进行强制规定

在实际项目中，最好配合以下几个工具，让整个项目的代码风格统一

- eslint：代码格式检查工具
- lint-staged：对git的暂存文件进行lint检查
- husky：git钩子，能够很方便地在项目中配置git的hook操作，通过它我们能够实现在代码提交时检查并尝试修复一些代码风格问题

## 安装与初始化

1. 直接这样一起安装几个工具: `npm install --save-dev husky lint-staged eslint`
2. 可以执行`./node_modules/.bin/eslint --init`对当前目录的项目进行eslint初始化，能够通过交互式的命令进行配置，完成后会在当前目录创建配置文件`.eslintrc.js`

<!--more-->


```shell
? How would you like to use ESLint? …
  To check syntax only
❯ To check syntax and find problems
  To check syntax, find problems, and enforce code style
  
? What type of modules does your project use? # 项目中使用什么类型的模块
❯ JavaScript modules (import/export)	# vue项目选这个
  CommonJS (require/exports)
  None of these
  
? Which framework does your project use? # 项目中使用什么框架
❯ React
  Vue.js
  None of these
  
? Does your project use TypeScript? › No / Yes	# 项目是否使用TypeScript，如果是下面会提示是否安装typescript的eslint

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

3. 在项目的`package.json`配置`husky`和`lint-stage`

```json
{
  "scripts": {
    "prepare": "husky install",	// 如果是整个项目统一用，那么只需要这样即可
    "lint-staged": "lint-staged"
  },
  "lint-staged": {
    "src/**": [		// 可以以目录形式指定目标
      "eslint --fix"
    ],
    "*.{js,vue}": [	// 也可以以文件后缀的形式指定目标
      "eslint --fix"
    ]
  }
}
```

4. 如果有多个子目录需要不同的规则可以这样做

   ```shell
   # 首先，package.json中的prepare script需要这样改。虽然不同子目录不同的规则，但是.git是一个，所以hook也只能有一个，可以在项目根目录创建和安装.husky
   "prepare": "husky install .husky",
   
   # 然后，在pre-commit脚本中添加逻辑，进入不同的子目录运行不同的eslint程序
   #!/bin/sh
   . "$(dirname "$0")/_/husky.sh"
   
   cd frontend
   echo 'Check frontend code'
   
   if [ -f "node_modules/.bin/lint-staged" ]; then
     ./node_modules/.bin/lint-staged
   else
     lint-staged
   fi
   
   cd ../backend
   echo 'Check Backend code'
   
   if [ -f "node_modules/.bin/lint-staged" ]; then
     ./node_modules/.bin/lint-staged
   else
     lint-staged
   fi
   ```

5. 执行`npm prepare`会在根目录创建`.husky`文件夹，并将hook应用到当前git仓库中

6. 添加`pre-commit` hook，执行命令`./node_modules/.bin/husky add .husky/pre-commit "npm run lint-staged" && git add .husky/pre-commit`

   如果想要修改执行命令可以修改`.husky/pre-commit`例如

   ```shell
   #!/bin/sh
   . "$(dirname "$0")/_/husky.sh"
   
   cd myDir
   echo 'Check My code'
   
   if [ -f "node_modules/.bin/lint-staged" ]; then
     ./node_modules/.bin/lint-staged
   else
     lint-staged
   fi
   ```

### 同一仓库多个目录配置

- 如果同一个仓库里面有多个目录需要配置单独的规则，那么需要在每个目录都是用`eslint init`一次，并在每个项目单独执行`npm compare`命令以安装`husky`到`.git` 的hook中并修改每个`.husky/pre-commit`进入正确的目录

## eslint配置

- eslint规则[官方网站](https://cn.eslint.org/)

### eslint常用命令

```shell
eslint file.js	# 校验指定文件
eslint --fix file.js	# 校验并尝试修改指定文件
```

### eslint规则配置

#### 全局配置

 以下配置都是在`.eslintrc.js`中

```javascript
module.exports = {
    "env": {	// 想启用的环境，默认就行
        "es2021": true,
        "node": true
    },
    "extends": [	// 从指定的插件中继承规则
        "eslint:recommended",	// eslint:all表示使用eslint的所有规则，可参考http://eslint.cn/docs/rules/，"eslint:recommended"表示使用eslint所有规则里面打勾的规则，"standard"表示使用standard的规则(需要先npm install standard --save-dev)，参考https://standardjs.com/rules-zhcn.html#javascript-standard-style。除了standard，还有Airbnb风格，但我比较习惯standard
        "plugin:@typescript-eslint/recommended"	// 如果是typescript需要添加这个插件
    ],
		"extends": ["standard-with-typescript"],	// 如果是standard with typescript，依赖直接执行 npm install --save-dev eslint-config-standard-with-typescript，npm<7需要参考https://github.com/standard/eslint-config-standard-with-typescript
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
      "@typescript-eslint/restrict-template-expressions": 0,	// 模板语法不验证类型，`${abc.def}`
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
      ],
  		'no-use-before-define': ['error', { variables: false, classes: false, functions: false }],	// 函数或方法或类的定义在使用的后面，如果要禁用可以这样做，一般不建议这样做
      'camelcase': 'off',	// 禁用camelcase提示，不推荐禁用
      'no-param-reassign': 'off', // 在函数内修改参数的值，不推荐禁用,
      'variable-name': [
        true,
        "allow-snake-case"	// 允许下划线分割
      ]
    },
    "overrides": [
      {
        files: ['pages/**'],	// 如果只想要某个指定的目录使用不同的规则，可以在overrides中这样定义
      	rules: {
          'react/prop-types': 'off'
        }
      }
    ]
};
```

#### 指定代码单独/忽略配置

- 除了使用rules来全局忽略某些配置以外，还能在局部忽略某些配置，例如: 

```javascript
// eslint-disable-next-line no-undef // 能忽略下一行出现的未定义错误，如cordova
cordova.plugins...

/* eslint-disable import/first */	// 这样注释能忽略当前文件下面所有行的指定的错误，这里是忽略import/first错误
```

#### 单独忽略指定文件

- 需要在`.eslintignore`中添加文件，语法同`.gitignore`

## TroubleShooting

- **Requires Promise-like values to be handled appropriately (`no-floating-promises`)**: Promise必须要能正确处理响应与异常，可以加上`then`和`catch`

  ```javascript
  (async () => {
    ...
  })() // 需要加上下面的then和catch才能避免错误提示，也是一种很好的编码习惯
    .then(() => { console.log('Start Success') })
    .catch(() => { console.log('Start Failed') })
  ```

- **Require statement not part of import statement.** 引入包的方式不同，需要将包引入方式改为允许的方式，例如
  将`const path = require('path')`改为`import path = require('path')`
  
- **ESLint: iterators/generators require regenerator-runtime, which is too heavyweight for this guide to allow them. Separately, loops should be avoided in favor of array iterations.(no-restricted-syntax)**: 这是`Airbnb`中的一条规则`no-restricted-syntax`会禁用一些新特性新语法，比如`for await ... in`，如果要禁用不建议在`rules`中整个禁用，直接在使用的地方加`// eslint-disable-next-line no-restricted-syntax`吧

- **lint-staged Node.js requirement to 12.13.0**: 最新版本的`lint-staged`要求node版本>=12.13.0(21年的)，或者降级`lint-staged`

- **eslint.rc里面的excludes不起作用，tsc的时候仍然去检查了node_modules里面的东西**: 尝试升级`typescript`到3.9.*及以上

- **Parameter 'xxx' implicitly has an 'any' type**: 要求太严的话就修改tsconfig.json，将compilerOptions下的noImplicitAny设置为false

- **"parserOptions.project" has been set for @typescript-eslint/parser**: 可以把`.eslintrc.js`文件加入`.eslintignore`中，或者把`.eslintrc.js`改成json后缀和格式，居然就可以了

- **no-plusplus**: 禁止使用一元操作符`++`或`--`，是因为空白可能会改变源代码的语义，可以使用`+=`来代替

- **consistent-return**: 原因是函数的返回值的类型不统一，可以自行修改一下

- **react camel case props**: 在react中禁止非驼峰写法的props，如果实在改不了，可以给它重命名: `{first_name: firstName, last_name: lastName}`

- **使用git的UI客户端，例如sourcetree，没有触发husky/eslint**：这个一般是由于sourcetree没有找到node导致，首先我们需要去sourcetree->Preference->Advanced->Always display full console output，打开后再次commit就会发现错误日志: `Can't find npx in PATH: ...Skipping pre-commit hook`，找不到node路径直接跳过了pre-commit hook。此时只需要将node路径加入环境变量即可。一般是由于我们使用的是nvm，我们只需要将nvm路径加入husky的环境变量即可：

  ```shell
  # vim ~/.huskyrc，这个文件就是用于加载这些环境变量的，注意这是home目录不是项目目录
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  
  export PATH="/Users/haofly/.nvm/versions/node/v15.3.0/bin:$PATH"	# 上面的配置还是不行那直接加到PATH吧
  ```
  
- **`No files matching the pattern "" were found`**: 找不到符合条件的文件就找不到嘛，非要抱个错出来，可以给`eslint`命令加上`--no-error-on-unmatched-pattern`
