---
title: "Strapi CMS 使用手册"
date: 2021-07-14 08:30:00
updated: 2021-08-16 10:53:00
categories: frontend
---

- [Roadmap](https://portal.productboard.com/strapi/1-roadmap/tabs/2-under-consideration): 真的有好多还没开发完成的实用功能

## 安装与配置

### 常用命令

```shell
export PORT=3000 && npm run develop	# 更改启动端口
```

### 配置文件

```javascript
// config/server.js, Server相关配置
module.exports = ({ env }) => ({
  host: env('HOST', process.env.HOST),
  port: env.int('PORT', process.env.PORT),
  admin: {
    url: 'admin',	// 可以修改默认的后台路径，但是不能设置为/ root路径，关注https://github.com/strapi/strapi/issues/9302
    auth: {
      secret: env('ADMIN_JWT_SECRET', process.env.ADMIN_JWT_SECRET),
    },
  },
});

// config/api.js, API相关配置
module.exports = ({ env }) => ({
  responses: {
    privateAttributes: ['_v', 'id', 'created_at'],
  },
  rest: {
    defaultLimit: 100,
    maxLimit: 250,
  },
});

// config/plugins.js, 插件相关配置
module.exports = {
  graphql: {	// graphql插件相关配置
    endpoint: '/graphql',
    shadowCRUD: true,
    playgroundAlways: false,
    depthLimit: 7,
    amountLimit: 100,
    apolloServer: {
      tracing: false,
    }
  }
}

// extensions/users-permissions/config/security.json, 修改jwt token的配置
{
  "jwt": {
    "expiresIn": "1d"
  }
}

// .env, 有几个默认的Strapi相关的配置，例如是否开启更新提示等，默认都是关闭了的
```

### 自定义Role及权限

- 免费版不能在web端直接进行配置，不过可以修改数据库，看一下数据库的表结构就能很好修改了，但问题是每次修改了types结构以后需要重新分配role的权限，否则权限会丢失，可以使用以下代码在重新启动应用时自动更新权限，但还是有个问题，如果应用不完全重启，仍然不会更新，因为应用没有完全重启的话`admin`的也不会更新的:

  ```javascript
  // config/functions/bootstrap.js
  "use strict";
  
  const lodash = require('lodash');
  
  // Prevent permissions loss
  const setDefaultRolePermissions = async () => {
    const adminRole = await strapi.query("role", "admin").findOne({id: 1});
    const customRoles = await strapi.query("role", "admin").find({id_gt: 3});
  
    customRoles.forEach(customRole => {
      console.log(`Check ${customRole.name} permissions`);
      customRole.permissions.forEach(permission => {
        // compare permission fields with adminRole
        const realPermission = adminRole.permissions.find(p => p.action === permission.action && p.subject === permission.subject)
        if (permission.properties.fields && permission.action.includes('plugins::content-manager.explorer') &&(permission.properties.fields.length !== realPermission.properties.fields.length ||
          permission.properties.fields.length !== lodash.uniq(permission.properties.fields.concat( realPermission.properties.fields)).length)) {
          strapi.query("permission", "admin").update({id: permission.id}, {properties: realPermission.properties})
        }
      })
    })
  };
  
  
  module.exports = async () => {
    setTimeout(setDefaultRolePermissions, 3000);	// 使用timeout是因为刚重启的时候数据库还没根据新的结构更新
  };
  ```

### 升级步骤

升级非常简单，直接在`composer.json`里面全局替换，例如将`3.5.2`全部替换成`3.6.1`，在执行以下命令即可

```shell
npm install
rm -rf .cache && rm -rf build/
```

### 修改admin系统文件

- 只需要参照`node_modules/strapi-admin/`中的目录结构，在根目录新建admin文件夹与其保持一致，任何想要覆盖的都可以放在这里
- 替换logo，可以在`admin/src/assets/images`中放置

## 其他特性

<!--more-->

### Hooks

### Middlewares

- 有一些自带的中间件: favicon、public、session、logger、parser、gzip、responseTime、poweredBy，安全相关的有csp、p3p、hsts、xframe、xss、cors、ip(可以设置黑白名单)

### Functions

- `./config/functions`目录下，这里面的函数可以用`trapi.config.functions['fileName']()`来调用
- `bootstrap.js`每启动都会执行

#### 定时获取外部数据

- 支持定时从外部获取数据并存储到数据库中，不过我没玩儿过，可以参考[这里](https://strapi.io/documentation/developer-docs/latest/guides/external-data.html#content-type-settings)

## API集成

- [这里](https://strapi.io/documentation/developer-docs/latest/developer-resources/content-api/integrations.html)列举了各个前端如何使用API的方法
- 调用API如果开启了认证，那么就得用一个user来用接口登录获取jwt token，并且这里的user和登录用户不一样，需要重新注册才行，并且默认都可以注册，注册了一个后可以在`USERS & PERMISSIONS PLUGIN -> Advanced Settings`去关闭注册功能

### graphql

- 服务端需要先安装`strapi install graphql`，客户端也需要安装`npm install @apollo/client graphql` 

```javascript
// 登录获取jwt token
mutation {
  login(input: { identifier: "email", password: "password" }) {
    jwt
  }
}
```

## 外部插件

### [Cloudinary支持官方文档](https://strapi.io/blog/adding-cloudinary-support-to-your-strapi-application)

集成步骤

1. 安装`npm install strapi-provider-upload-cloudinary graphql --save`

2. 在`config/plugins.js`中添加`upload`配置:

   ```json
   module.exports = ({ env }) => ({
       // ...
       upload: {
         provider: 'cloudinary',
         providerOptions: {
           cloud_name: env('CLOUDINARY_NAME'),
           api_key: env('CLOUDINARY_KEY'),
           api_secret: env('CLOUDINARY_SECRET'),
         },
       },
       // ...
     });
   ```

#### 支持上传至指定目录

- 官方的这个插件默认不支持指定上传目录，可以关注这个`issue`，也不知道他们怎么想的，如果要支持自定义目录或者其他clodinary配置，可以用[strapi-provider-upload-cloudinary-folderoptions](https://github.com/VerdeCircle/strapi-provider-upload-cloudinary-folderoptions)，但是它有个问题就是upload from url的时候会把那个url当成目录层级，可是url本身放到url中会报错

- 第二种方法就是自己修改一下官方那个插件即可，挺简单的：

  1. 修改`package.json`添加依赖: `strapi-provider-upload-cloudinary-folder: "file:providers/strapi-provider-upload-cloudinary-folder"`
  2. 修改`config/plugin.js`，将`upload.provider`修改为`cloudinary-folder`，并且在`providerOptions`中添加参数`folder: env('CLOUDINARY_DEFAULT_FOLDER')`

- 复制[package.json](https://github.com/strapi/strapi/blob/master/packages/strapi-provider-upload-cloudinary/package.json)内容到`providers/strapi-provider-upload-cloudinary-folder/package.json`并修改`name`为`strapi-provider-upload-cloudinary-folder`

- 复制[index.js](https://github.com/strapi/strapi/blob/master/packages/strapi-provider-upload-cloudinary/lib/index.js)内容到`providers/provider-upload-cloudinary-folder/index.js`简单修改一下将配置传入:

  ```javascript
  init(config) {
      cloudinary.config(config);
      const folder = config.folder;
  
      return {
        upload(file, customConfig = {}) {
          return new Promise((resolve, reject) => {
            const config = {
              resource_type: 'auto',
              public_id: file.hash,
              folder,
            };
            
            ...
          }
  }
  ```

### [strapi-tinymce 集成tinymce](https://github.com/chiqui3d/strapi-tinymce)

集成步骤

1. 安装`npm install --save @tinymce/tinymce-react`

2. 从[tiny](https://www.tiny.cloud/get-tiny/self-hosted/)下载`tinymce`源码到`public`目录下，即目录结构为`public/tinymce`

3. 执行`strapi generate:plugin wysiwyg`生成新的富文本插件

4. 将[仓库](https://github.com/chiqui3d/strapi-tinymce)中的`content-manager/admin/src/components`复制到`plugins/wysiwyg/admin/src`下

5. 修改`plugins/wysiwyg/admin/src/index.js`将最后的返回值修改为我们自己的组件

   ```javascript
   strapi.registerField({ type: 'wysiwyg', Component: WysiwygWithErrors});
   return strapi.registerPlugin(plugin);
   ```

6. 如果要editor支持所有的html tag，可以在`plugins/wysiwyg/admin/src/components/WysiwygWithErros/Tinymce.js`的`init`属性中添加

   ```shell
   extended_valid_elements: "*[*]",
   non_empty_elements: "td,th,iframe,video,audio,object,script,pre,code,area,base,basefont,br,col,frame,hr,img,input,isindex,link,meta,param,embed,source,wbr,track, svg,defs,pattern,desc,metadata,g,mask,path,line,marker,rect,circle,ellipse,polygon,polyline,linearGradient,radialGradient,stop,image,view,text,textPath,title,tspan,glyph,symbol,switch,use",
   ```

### 实现/集成color picker功能

- 仓库见[Strapi_ColorPicker_Plugin](https://github.com/paulgaumer/Strapi_ColorPicker_Plugin)，他还写了个[文档](https://www.paulgaumer.com/blog/how-to-create-a-color-picker-plugin-for-strapi-cms)

- 由于原本的代码不能直接用，所以这里记录下具体集成步骤:

  1. 将上面仓库代码中的`api/plugins/colorPicker`复制到我们项目的`plugins/`目录下

  2. 修改`plugins/colorpicker/admin/src/components/colorPicker/index.js`的如下代码:

     ```javascript
     const Title = styled.h5`
       margin-bottom: 1rem;
       color: #333740;
       text-transform: capitalize;	// title增加首字母大写样式
     `;
     
     const updateColorValue = (colorValue) => {
       props.onChange({ target: { name: props.name, value: colorValue } });	// 名字修改为属性本来的名字，这样用于组件的时候也不会有bug
     };
     
     <Title>{props.name.split('.').slice(-1)[0]}</Title>	// title也用本来的名字，只是首字母大写而已
     ```

  3. 最重要的，一定要`npm run build`一下

  4. 由于strapi对自定义字段还未支持完成，所以现在新加的字段不会在UI上面显示，如果要将某个字段修改为colorpicker类型，需要手动在components下面的scheme中进行修改:

     ```javascript
     "color": {
     	"type": "colorpicker",
     	"columnType": "string"
     }
     ```

### 实现网页菜单配置

- 目前我没找到一个比较好的菜单配置插件
- 目前component不支持嵌套自身，所以我只能自己做两个component: TopMenu(title, url, subMenus), SubMenu(title, url)，只能二级，如果多级只能再加新的component

## TroubleShooting

- **The file is too big**: 这一般是nginx的限制，上传的文件太大了，需要修改nginx的配置`client_max_body_size 10m`

- **如果新建的内容访问接口是404**: 一般是因为没有发布publish

- **relationship 关联对象拖动排序无效**:  明明保存时提交的字段的顺序都是正确的，但是提交后又是原来的顺序了，目前是[还没修复](https://github.com/strapi/strapi/issues/2166)，但是可以先把所有的关联删除了，保存后再重新新建就行了

- **无法多级嵌套使用components**: 网页上不行，但是直接修改`component`的json文件一般是可以的，但有时候也不能用，还是得等官方支持才行:

  ```json
  // 例如如果网页上不能选择某个component，那么可以直接修改其json文件，在attributes里面添加字段
  {
    "collectionName": "components_common_main_menus",
    "info": {
      "name": "MainMenu",
      "icon": "braille",
      "description": ""
    },
    "options": {},
    "attributes": {
      "text": {
        "type": "string"
      },
      "dropdownMenus": {
        "type": "component",
        "repeatable": true,
        "component": "common.dropdown-menu"
      }
    }
  }
  ```

- **error TypeError: Cannot read property 'attributes' of undefined**: 可能是某个组件没上传导致的，如果报错行数在`./node_moduels/strapi-plugin-documentation/services/Documentation.js:592:42`直接去里面把`component`打印出来吧