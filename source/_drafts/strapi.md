strapi

## 安装与配置

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

### 定时获取外部数据

- 支持定时从外部获取数据并存储到数据库中，不过我没玩儿过，可以参考[这里](https://strapi.io/documentation/developer-docs/latest/guides/external-data.html#content-type-settings)

## 外部插件

### [Cloudinary支持官方文档](https://strapi.io/blog/adding-cloudinary-support-to-your-strapi-application)

### [strapi-tinymce 集成tinymce](https://github.com/chiqui3d/strapi-tinymce)









https://forum.strapi.io/t/can-not-edit-content-types-in-content-types-builder/1225



npm install strapi-provider-upload-cloudinary --save



The autoReload feature is required to use this plugin. Start your server with `strapi develop`

https://github.com/strapi/strapi/issues/4890 网页上我们不能选择多层级的component，但是其实直接修改json代码是支持的，鬼迷日眼的



export PORT=3000 && npm run develop	# 更改启动接口



```
pm2 start npm --name app -- run start
```

##  

更改富文本编辑框 https://strapi.io/blog/how-to-change-the-wysiwyg-in-strapi

tinymce https://github.com/chiqui3d/strapi-tinymce

https://www.tiny.cloud/get-tiny/self-hosted/

创建新的字段https://strapi.io/documentation/developer-docs/latest/guides/registering-a-field-in-admin.html#setup

conetnt api https://strapi.io/documentation/developer-docs/latest/developer-resources/content-api/content-api.html#api-endpoints



配置显示的字段：https://github.com/strapi/strapi/issues/4128

npm install strapi-provider-upload-cloudinary --save



content api

筛选：Filters、Sort、Limit、Start、Publication State









## TroubleShooting

- **The file is too big**: 这一般是nginx的限制，上传的文件太大了，需要修改nginx的配置`client_max_body_size 10m`
- **如果新建的内容访问接口是404**: 一般是因为没有发布publish
- **relationship 关联对象拖动排序无效**:  明明保存时提交的字段的顺序都是正确的，但是提交后又是原来的顺序了，目前是[还没修复](https://github.com/strapi/strapi/issues/2166)，但是可以先把所有的关联删除了，保存后再重新新建就行了