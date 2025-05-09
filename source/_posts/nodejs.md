---
title: "node.js教程"
date: 2015-12-07 10:02:30
updated: 2025-03-05 08:50:30
categories: frontend
---
- [`nodejs`各个版本当前的维护情况](https://nodejs.org/en/about/releases/)(10.x已经不再维护，12.x在2022年4月30日停止维护，14.x在2023年4月30日停止维护，16.x在2024年4月30日停止维护)。个人觉得当前应该使用的版本是`MAINTENANCE LTS START`的，`ACTIVE LTS START`应该没有`MAINTENANCE LTS START`的稳定，所以现在直到`2022-10-18`都应使用`14.x`

## 安装
需要注意的是，关于npm的所有命令，最好都不要用root用户执行，否则会出现各种不可预料甚至连官方文档都说不清的问题

稳定版: 

```shell
# centos用下面命令安装指定版本nodejs
sudo curl --silent --location https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# ubuntu用下面命令安装指定版本nodejs
sudo curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
# docker里面没有sudo就直接
curl -sL https://deb.nodesource.com/setup_18.x | sudo bash -
apt-get install -y nodejs

# 添加淘宝镜像，既然用的阿里云，那淘宝的镜像也就不介意了
npm install -g nrm && nrm use cnpm	# 这样可以防止npm和cnpm混用导致的各种not found的错误
npm install -g cnpm --registry=https://registry.npm.taobao.org
```
安装package.json 直接`npm install`后面不加package.json的名字

## package.json文件

```json
{
  "scripts": {	// 指定了运行脚本命令的npm命令行缩写
    "start": "node index.js",
    "test": "",
    "deploy": "next build & next export & copyfiles _redirects out/"	// 可以使用copyfiles工具来复制文件，npm install copyfiles --save-dev
  },
  "bin": {	// 用于指定各个内部命令对应的可执行文件的位置
    "someTool": "./bin/someTool.js"	// 当然这也可以直接在scripts里面写成./node_modules/bin/someTool.js
  },
  "engines": {	// 指定了运行环境
    "node": ">=0.10.3 <0.12", // 强制指定node版本 "node": ">=18"
		"npm": "~1.0.20"
  },
  "dependencies": {	// 指定项目运行所依赖的模块
    "aaa": "~1.2.2",	// 波浪号，这里表示>1.2.2(1.2.x)且<1.3.x
    "bbb": "^1.2.2",	// 插入号，这里表示>1.2.2(1.x.x)且<2.x.x
    "ccc": "latest", // 安装最新版本
  },
  "devDependencies": {	// 指定项目开发所依赖的模块
    
  }
}
```

### 同一个repo多个项目共享文件

1. 可以将共享的方法或者文件放到一个shared目录下，并且将shared设置为一个单独的package，这样目录结构就是这样的:
   ```shell
   project/
     proj1/
       package.json
     proj2/
     	package.json
     shared/
       package.json
   ```

2. 然后将shared/package.json的`package.json`中的`name`设置为`@proj/shared`

3. 接着在proj1和proj2中都可以这样引入到`package.json`中
   ```json
   {
     "dependencies": {
       "@proj/shared": "file:../shared"
     }
   }
   ```

4. 然后在proj1和proj2中可以这样使用了:
   ```javascript
   import { sendEmail } from "@nsc/shared/emailUtil";
   ```

## 常用语法

### 类

```javascript
// 声明一个类
class Rectangle {
  height = 0;	// 公有字段声明
  static displayName = "Point";	// 静态变量
  
  // 类的构造函数
  constructor(height, width) {
    this.height = height;
    this.width = width;
  }
  
  // Getter方法
  get area() {
      return this.calcArea()
  }
  
  // Method方法
  calcArea() {
      return this.height * this.width;
  }

	// 静态方法
 	static distance(a, b) {
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        return Math.hypot(dx, dy);
  }
}
```

### nodejs原生http请求

- 无需安装任何package

```javascript
const https = require('https')

const req = https.request('https://haofly.net', res => {
  res.on('data', (chunk) => (body += chunk.toString()));
  res.on('error', () => reject(res))
  res.on('end', () => {
    if (res.statusCode >= 200 && res.statusCode <= 299) {
      resolve({statusCode: res.statusCode, headers: res.headers, body: body});
    } else {
      reject('Request failed. status: ' + res.statusCode + ', body: ' + body);
    }
  })
})
req.on('error', () => reject)
req.write(body, 'binary')
req.end()
```

### 命令行

```javascript
process.argv	// 从命令行接收参数
```

### ECSMAScript/es6概念

- `export`和`import`是`es6`之后才支持的

- es的重要版本

  ```shell
  ES6 ES2015 # 2015年6月发布, 之后每年6月出一个新版本
  ES7 ES2016
  ES8 ES2017
  ES9 ES2018
  ES10 ES2019
  ES11 ES2020
  ES12 ES2021
  ```

- 一些比较使用的新的语法

  ```javascript
  // 解构赋值
  const [a, b, c] = [value1, value2, value3]
  const {name, age} = obj
  ```

## 常用命令

- 报名前面带"@"符号的，表示是属于某个组织，又组织上传到镜像源里面的

#### Nvm

- 可以通过`node -v > .nvmrc`将当前node版本限制在文件中，之后在当前目录只需要执行`nvm use`即可自动选择对应的版本

可以通过`nvm`来同时使用多个`node`版本，mac上可以直接`brew install nvm`进行安装(其他平台直接[官网安装方法](https://github.com/nvm-sh/nvm))，安装完成后根据提示添加`sh`的`rc`文件，常用命令如下:

```shell
nvm ls-remote	# 查看所有可用的node版本
nvm install xxx	# 下载需要的版本
nvm use xxx	# 使用指定的版本
nvm alias default xxx 	# 设置默认的node版本
nvm uninstall v7.10.1

rm `which node` && nvm alias default 18.20.0 # 替换system默认的版本
```

#### npm

```shell
npm init		# 将当前目录设置为一个npm库，自动生成package.json文件，如果没有package.json文件可以用这个方法生成，它也会自动把node_module下的已安装包加进来的
npm install 包名 --save	# 安装包，并且更新到package.json中去
npm install 包名 --save-dev	# 安装包，并且更新到package.json的开发依赖中区
npm install 包名@3.1.0 --save	# 安装指定版本的包
npm install git+https://github.com/haoflynet/example.git	# 从Github仓库安装模块
npm install git://github.com/haoflynet/example.git
npm list --depth=0	# 列出已安装模块
npm list -g --depth=0 # 列出全局安装的包
npm list --depth=0 2> /dev/null	# 忽略标准错误输出(npm ERR!这种错误将被忽略
npm view 包名 versions	# 列出指定包的所有版本
npm update 			# 升级当前目录下的所有模块
npm update 包名		# 更新指定包
npm install npm -g	# 升级npm
npm install -g n && n stable # 升级node.js到最新稳定版
升级node.js
npm install --verbose # 显示debug日志

npm config delete name	# 删除某个配置

#  代理设置
npm config set proxy=http://127.0.0.1:1080 && npm config set proxy=https://127.0.0.1:1080
```
#### Yarn

- `yarn`从`1.10x`开始会在`yarn.lock`中增加`integrity`字段，用于验证包的有效性
- yarn真的笔npm快，而且每次lock文件的变动要少一些

```shell
yarn add 包名	# 安装包
yarn add -D 包名 # 安装dev依赖
npm install yarn@latest -g	# 升级yarn
yarn dev -p 8000	# yarn能直接将参数传递给scripts，npm不行
```

## TypeScript

- 给js引入type，使开发更加严谨

- 引入步骤：
  1. `npm install --save-dev typescript @types/node`
  2. 初始化`./node_modules/.bin/tsc --init`
  3. 最后使用`tsc`命令进行编译，将它放入`package.json`的`scripts`里面即可
  
- 配置

  ```json
  {
    "compilerOptions": {
      "target": "es5", // 生成的代码的语言版本
      "skipLibCheck": true,	// 跳过类型声明文件的类型检查
      "allowSyntheticDefaultImports": true,	// 运行import x from 'y'这种操作，即使模块没有显示指定default的到处
      "strict": true, // 开启严格模式
    },
    "include": ["src"],	// 搜索ts文件的路径
  }
  ```
  
- 函数定义

  ```javascript
  // 可变参数
  function test(field1: string, ...fields: string)
  ```

- 常用类型

  ```javascript
  interface MyType {
    [key: string]: string;	// mapping类型
  }
  
  type MyType = {
    username: string;
    pass: string;
  }
  
  type Type2 = keyof MyType;	// Type2会被解析为'username'|'pass'
  
  enum MyEnum {	// 注意定义枚举的时候要把key和value都写出来，如果写成enum MyEnum {VALUE1, VALUE2}这样可能会导致后面无法拿来匹配值，无论字符串还是枚举都匹配不上
    VALUE1 = 'VALUE1', VALUE2 = 'VALUE2', VALUE3 = 'VALUE3'
  }
  ```

- 自定义类型:

  ```javascript
  interface MyType {
    name: string;
    children: MyType2[];	// 定义数组
    [index: number]: { id: number; label: string; key: any };
  }
  ```

- 常见错误
  - **Object is of type 'unknown' typescript generics**: 如果程序无法判断准确的类型，那么我们需要强制声明一下类型，例如`(error as Error).message`
  - **Property 'classList' does not exist on type 'Never'**: 对于react的ref需要这样定义: `const myEl = useRef<HTMLDivElement>(null);`
  - **window undefined**: 尝试生命一个window对象
    ```javascript
    export interface CustomWindow extends Window {
      customAttribute: any;
    }
    declare let window: CustomWindow;
    ```

## ~~使用Forever管理NodeJs应用~~(生产环境最好用[pm2](https://haofly.net/pm2))

- 直接使用`sudo npm install forever -g`进行安装

### forever常用命令

```shell
forever list	# 查看当前所有管理的服务
forever stopall 	# 停止所有服务
forever stop 服务ID	# 停止指定服务
forever restartall	# 重启所有服务
forever logs -f 服务ID	# 查看某个服务的日志

# 下面这些命令一般用于非config文件启动方式
forever server.js	# 直接启动进程
forever start server.js	# 以daemon方式启动进程
forever start -l /var/log/forever.log -a server.js	# 指定日志文件
forever start -o /var/log/forever/out.log -e /var/log/forever/err.log -a server.js	# 分别指定日志和错误日志文件，-a表示追加
forever start -w server.js	# 监听文件夹下所有文件的改动并自动重启
```

## 常用包推荐

- [adm-zip](https://github.com/cthackers/adm-zip): 制作zip包工具，很多lambda函数都需要将仓库打包成zip文件，这个库就很有用:

  ```javascript
  const AdmZip = require('adm-zip');
  
  const zip = new AdmZip();
  
  zip.addLocalFolder('../repo', './', (path) => {
      if (path.includes('node_modules') ||	// 忽略特定的文件夹
          path.includes('build/') ||
          path.includes('dist/') ||
          path.includes('.zip') ||
          path.includes('logs/')
      ) {
          return false;
      }
      return true;
  });
  zip.writeZip('./repo.zip');
  ```

- [bcrypt](https://www.npmjs.com/package/bcrypt): 非常推荐的安全的密码/密码hash库，不用自己维护盐值，它是把计算次数和盐值都放到hash值里面去了

- [dotenv](https://www.npmjs.com/package/dotenv): 支持.env文件读取环境变量

  ```javascript
  // 默认读取项目根目录的.env文件，也可以自定义.env文件的路径
  import { config } from 'dotenv';
  
  config({
    path: '../.env',
  });
  
  // 使用require的方式
  require('dotenv').config({
    path: `configs/${process.env.NODE_ENV}.env`,
  });
  ```

- [human-numbers](https://github.com/Kikobeats/human-number)：转换数字的大小K、M、B、T，不过它其实就一个[方法](https://github.com/Kikobeats/human-number/blob/master/src/index.js)，都可以不用它这个包

- [node-csv](https://github.com/adaltas/node-csv): 读写CSV文件的库，它由cdv-generate,csv-parse,csv-transform,csv-stringify几个部分组成，一个一次性安装，也可以单独安装

- [object-sizeof](https://www.npmjs.com/package/object-sizeof): 获取变量所占内存的大小，有时候非常需要这样的东西

- [randomstring](https://www.npmjs.com/package/randomstring): 生成随机字符串

- [uuid](): uuid首选version 4，每秒生成10亿个，大约需要85年才会重复

- [yup](https://github.com/jquense/yup): 非常简单且易于集成的认证库

## TroubleShooting

- **Permission Denied**问题，使用npm命令总是会出现这个问题，解决方法最简单的是把npm目录的拥有者修改为当前用户的名字` sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}`

- **安装包时报错Unexpected end of JSON input while parsing near ' : '** 尝试先执行`npm cache clean --force`，然后再安装

- **gyp: No Xcode or CLT version detected!**: 需要先安装`xcode`命令工具: `xcode-select --install`

- **npm install结果被系统killed掉了**: 一般是内存不足，可以使用增加swap的方法，参考[Linux 手册](https://haofly.net/linux/index.html)

- **ReferenceError: describe is not defined NodeJs**: 应该是`mocha`这个测试库报的错，安装它即可: `npm install mocha -g`

- **wasm code commit Allocation failed - process out of memory**: 在Apple m1(apple silicon)上npm编译失败，可以尝试将`node`升级到`v15.3.0`及以上

- **a promise was created in a handler but was not returned from it**: 通常是`bluebird`报错，函数没有正确地返回，遇到这个情况一个是验证回掉函数`then`是否有正确的返回，如果没有，那么可以添加一个`return null`语句，需要注意的是，如果`then`回掉里面只有一个语句，例如`.then(res => res + 'abc')`，这样不用单独写`return`，但如果里面的语句不只一句就得加了

- **Node Sass does not yet support your current environment: Windows 64-bit with Unsupported runtime (88)**: `npm rebuild node-sass`

- **Error: spawn ../node_modules/optipng-bin/vendor/optipng ENOENT**: 尝试执行`npm rebuild`

- **this._settlePromiseFromHandler is not a function**: 尝试删除`node_module`目录并重新安装

- **gulp: command not found**: `npm install gulp-cli -g`

- **SyntaxError: Unexpected token export**: 尝试使用`module.exports = XXX`来到处模块或方法

- **Unsupported platform for fsevents@1.4.9: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"}**: 原因是在m1的mac上面安装了该包并上传了自己的`package-lock.json`，得清理一下缓存才行了:

  ```shell
  rm -rf node_modules package-lock.json
  npm cache clean --force
  npm cache verify
  npm install --verbose
  ```

- **Uncaught Error: ENOENT: no such file or directory, uv_cwd**: 检查一下当前目录是否还存在文件，node_modules这些目录是否还在

- **error TS2694: Namespace 'NodeJS' has no exported member 'TypedArray'.**: 尝试`yarn add --dev @types/node`

- **Cannot invoke an object which is possibly 'undefined'** 通常是在调用一个可能为undefined的对象的方法的时候出现，需要对方法也是用问号表达式: `props.obj?.click?.()`

- **npm ERR! integrity checksum failed when using sha1: wanted ... but got ...**: 尝试执行

  ```
  npm cache clean -force
  npm cache verify
  ```

- **从Github私有仓库安装**: 需要在github生成token，然后放入`.npmrc`中:

  ```shell
  @optionsai:registry=https://npm.pkg.github.com/
  //npm.pkg.github.com/:_authToken=这里就是token
  ```

- **nodejs如何退出进程**

  ```javascript
  process.exit()
  ```
  
- nodejs中直接使用await报错: `SyntaxError: await is only valid in async functions and the top level bodies of modules`
  ```javascript
  // 将其修改为一个异步方法
  async function run() {
      // 在这里使用 await
      const result = await someAsyncFunction();
      console.log(result);
  }
  run()
  ```
  
- **/usr/lib/libcurl.dylib (No such file or directory)**: 在mac上安装失败，可以尝试

  ```shell
  brew install curl-openssl
  export PATH="/opt/homebrew/opt/curl/bin:$PATH" >> ~/.zshrc
  ```

##### 扩展阅读

**[N-club](https://github.com/nswbmw/N-club):** 使用Koa + MongoDB + Redis搭建的论坛系统

[不容错谷哦的Node.js项目架构](https://mp.weixin.qq.com/s/nivph5JV_sovSDDSCsKmAA)n
