---
title: "Shopify 开发手册"
date: 2021-04-28 15:02:30
categories: javascript
---

## 后台配置

- 配置是否需要用户登陆`Settings->Checkout ->Customer accounts`，如果用户登陆是可选的，那么可以做一个[Continue as Guest](https://shopify.github.io/liquid-code-examples/example/customer-login)按钮

## Shopify前端开发

- `shopify`的搜索功能无法做更多自定义，但是他们的搜索匹配方式有点奇怪，很多时候不能搜到我们想要的东西，不用去想了，没有解决方案

### 命令行工具

```shell
theme download	# 将shpify那边的主题文件同步到本地
theme watch # 监听本地文件改动，如果有改动会自动上传上去
```

### Liquid手册

- 因为是后端渲染的，不要尝试在liquid里面获取query参数(js除外)，但是shopify的语法里有些方法可以获取到`product/variant`等参数的

#### 模板结构

- `templates/index.liquid`就是首页了

<!--more-->

##### Assets

- 可以用`scss`来写`css`非常方便，只需要在`assets`里新建一个文件，例如`styles.scss.liquid`，然后`layout/theme.liquid`中引用即可`{{ 'styles.scss.css' | asset_url | stylesheet_tag }}`
- 由于shopify的限制，目前无法在assets 里面使用子目录/二级目录

##### Sections

- Section类似于页面中一块一块的区域，如果指定了scheme，是可以在admin后台的UI上进行修改字段的，这个就非常方便了

- 常用的可以放在sections里面的东西：弹出框modal

- Section的内容是可以在admin前端改的，那就是说section在复用的时候是不能更改其内容的，只有snippet在复用的时候可以更改内容

- Section的属性可以在`config/settings_data`中最难过进行定义

  ```javascript
  {
    "current": {
      "sections": {
        "section文件名": {
          "type": "section文件名",
          "settings": {
  					"title": "My Site",
            "subtitle": "subtitle",
            "url": "shopify:\/\/collections\/all"
          }
        }
      }
    }
  }
  ```

- Section的定义，写到sections目录下即可

  ```javascript
  <div>
  	<h1>{{ section.settings.title }}</h1>	// 使用section的属性
  	<p>{{ section.settings.subtitle }}</p>
    
  </div>
  
  {% schema %}	// 定义这个section可以使用的属性，类似于vuejs中的Props
  {
    "name": "Main Hero",
    "settings": [
     	{
        "type": "image_picker",
        "id": "image",
        "label": "xxx"
      },
      {
        "type": "text",
        "id" "title",
        "label": "Title"
      },
      {
        "type": "text",
        "id": "subtitle",
        "label": "Sub Title"
      },
      {
        "type": "url",
        "id": "url",
        "label": "URL"
      }
    ]
  }
  {% endschema%}
  ```

- 在Template中引用section

  ```javascript
  {% section 'page-hero' %} // 在Templates中引用section
  ```

##### Snippets

- Snippet是比Section更小粒度的元素，类似于组件component了吧

- 定义比较简单了:

  ```javascript
  <div>
    {{ product.title }}	// 可以直接引用外部传进来的变量
  </div>
  ```

- 外部在使用的时候需要传入变量

  ```javascript
  {% render 'product', product: product %}
  ```

<!--more-->

#### 模板基本语法

```javascript
{{ product.title }} // 获取变量值

// if else 条件语句
{% if product.available %}
	aaa
{% else %}
	bbb
{% endif %}
```

#### Filters

- 需要注意的是`paginate`和`sort`不能混合使用，但是有些对象自带了`sort`功能的，可以参考[collection](#collection)
- `forloop.index`第一个索引是1，`forloop.index0`第一个索引是0

```javascript
// 字符串
{{ 'hello, world!' | capitalize }}	// 首字母大写
{{ 'hello, world!' | remove: 'world'}}	// 移除字符串
{{ 'hello, world!' | remove_first: 'world'}}	// 移除字符串，只移除第一个
{{ product.title | replace: 'Awesome', 'Mega' }}	// replace操作
{{ product.title | replace_first: 'Awesome', 'Mega' }}	// 只replace第一个
{{ "hello" | slice: 1, 3 }}	// slice操作
{{ '   too many spaces      ' | strip }}	// strip操作，去除前后空白，还有lstrip、rstrip、strip_html、strip_newlines
{{ "The cat came back the very next day" | truncate: 13 }}	// 限制显示长度，多的以省略号显示
{{ "ABCDEFGHIJKLMNOPQRSTUVWXYZ" | truncate: 18, ", and so on" }}	// 或者指定多的时候显示啥
{{ "The cat came back the very next day" | truncatewords: 4 }}	// 限制显示长度，但是以单位为单位
{% assign strs = 'hello, world!' | split: ',' %}	// 字符串的split方法，这里顺便把结果赋给一个新的变量
{{ 'sales' | append: '.jpg' }}	// 给字符串添加后缀
{{ 'sale' | prepend: 'Made a great ' }} // 给字符串添加前缀
{{ 'coming-soon' | camelcase }}	// 转换为驼峰形式
{{ 'UPPERCASE' | downcase }}	// 字符串小写
{{ 'i want this to be uppercase' | upcase }}	// 字符串大写
{{ "<p>test</p>" | escape }} // html元素escape
{{ '100% M & Ms!!!' | handleize }} // 转换特殊字符，输出为100-m-ms
{{ 'abc' | md5 }}	// 计算MD5，类似的还有sha1、sha256、hmac_sha1、hmac_sha256
{{ var | newline_to_br }}	// 每个元素后面添加一个<br>
{{ cart.item_count | pluralize: 'item', 'items' }}	// 设置单复数时的单位
var content = {{ pages.page-handle.content | json }};
{{ "test" | split: "" | reverse | join: "" }}	// 对字符串进行逆序操作(reverse只能用于数组所以用这种方式)

// 数组
{{ product.tags[2] }}	// 数组能直接用下标访问
{{ product.tags | join: ', '}}	// 数组的join操作
{{ proeuct.tags | first }}	// 获取数组第一个元素
{{ proeuct.tags | last }}	// 获取数组最后一个元素
{% assign all = arr1 | contact: arr2 %}	// contact方法合并两个数组
{{ my_array | reverse }}	// 数组逆序
{{ my_array | size }}	// 获取数组长度
{% assign products = collection.products | sort: 'price' %}	// 按照数组的某个值排序order
{% assign kitchen_products = collection.products | where: 'type', 'kitchen' %}	// 搜素数组
{{ my_array | split: ' ' | uniq }}	// 数组去重
{{ my_array | map: 'title'}}	// 去除数组中每个对象的指定key为一个新的数组

// Color filters，能动态改变color
// Font filters，能动态改变font
// Match filters，能够进行一些基本的数学运算，包括abs、at_most、at_least、ceil、devided_by、floor、minus(减法)、plus(加法)、round、times、modulo(求余)
{% assign count = count | plus: 1 %}
// Media filters，包括external_video_tag、external_video_url、img_tag、img_url、media_tag、model_viewer_tag、video_tag
// Money filters，跟钱price有关的一些运算，包括money、money_with_currency、money_without_trailing_zeros、money_without_currency
 
// img_tag，以直接应用于product、variant、line item、collection、image对象，可以指定参数，第一个参数为alt，第二个参数为class，例如
{{ 'smirking_gnome.gif' | asset_url | img_tag: 'Smirking Gnome', 'cssclass1 cssclass2' }} // 会输出:
<img src="//cdn.shopify.com/s/files/1/0147/8382/t/15/assets/smirking_gnome.gif?v=1384022871" alt="Smirking Gnome" class="cssclass1 cssclass2" />
  
// script_tag/stylesheet_tag，指定脚本和css
{{ 'shop.js' | asset_url | script_tag }}
{{ 'shop.css' | asset_url | stylesheet_tag }}

{{ 'Shopify' | link_to: 'https://www.shopify.com','A link to Shopify' }}	// link_to
{{ "Shopify" | link_to_vendor }}	// link_to_vendor
{{ "jeans" | link_to_type }}	// link_to_type
{{ tag | link_to_tag: tag }}
{{ tag | link_to_add_tag: tag }}
{{ tag | link_to_remove_tag: tag }}
 
<img src="{{ type | payment_type_img_url }}" />
{{ 'option_selection.' | shopify_asset_url | script_tag }}
{{ collection.url | sort_by: 'best-selling' }}
{{ "T-shirt" | url_for_type }}
{{ "Shopify" | url_for_vendor }}
<a href="{{ product.url | within: collection }}">{{ product.title }}</a>
 
// 时间
{{ article.published_at | time_tag }}	// 能直接输出<time datetime="2018-12-31T18:00:00Z">Monday, December 31, 2018 at 1:00 pm -0500</time>
{{ article.published_at | time_tag: format: 'date' }}
{{ article.published_at | time_tag: '%a, %b %d, %Y', datetime: '%Y-%m-%d' }}
{{ 'now' | date: "%Y %b %d" }}
{{ 'now' | date: "%Y" }}
 
Dear {{ customer.name | default: "customer" }}	// 设置默认值
{{ form.errors | default_errors }}	// 默认error

// 分页
{% paginate collection.products by 12 %}
	{%for product in collection.products %}
  	{% render 'product', proudct: product%}
  {% endfor %}
{% endpaginate %}
{% if paginate.pages > 1%}
	{% if paginate.previous.is_link %}	// 是否有上一页
  	<a href="{{ paginate.previous.url }}">prev</a>
  {% endif %}
  
  // for 循环
  {% for part in paginate.parts %}
    <a href="{{ part.url }}" {% if forloop.index == paginate.current_page %}class="active"{% endif %}>{{ part.title }}</a>
    {% if forloop.first == true %}{% endif %}	// 判断是否是第一个元素
    {% if forloop.last == true %}{% endif %}	// 判断是否是最后一个元素
    {{ forloop.length }}	// 循环长度
  {% endfor %}
  
  {% if paginate.next.is_link %}	// 是否有下一页
  	<a href="{{ paginate.next.url }}">next</a>
  {% endif %}
{% endif %}

{{ tag | highlight_active | link_to_tag: tag }}
 
<span>{{ 'products.product.sold_out' | t }}</span>	// 翻译
{{ product.variants.first.weight | weight_with_unit }}
{{ 'collection-1' | placeholder_svg_tag }}
```

##### URL filters

###### img_url

- 返回一个经过处理了的图片的URL地址，支持设置大小参数
- 如果不提供大小参数，那么默认返回的是一张`100 x 100`的小图

```javascript
{{ product | img_url: '720x720' }}	// 返回product的首图，并且图片大小为720x720
{{ product | img_url: 'master' }}	// 获取原图
{{ variant.image | img_url: '240x' }} // 也可以只提供宽度
{{ variant.image | img_url: 'x240' }} // 也可以只提供高度
{{ variant.image.src | img_url: '240x'}}	// 同上，可以带.src也可以不用
{{ product | img_url: '400x400', scale: 2 }}	// 设置缩放级别，不过scale的值只支持2或者3
{{ product | img_url: '400x400', format: 'pjpg' }}	// 设置图片格式，只支持pjpg和jpg
{{ product | img_url: '400x400', crop: 'bottom' }}	// 支持裁剪，crop值可选top、center、bottom、left、right
```

#### Objects/常用对象

- 对象的`handle`适用起来非常方便，可以直接通过`handle`找到对象，而这个`handle`其实就是url后缀，例如

  ```javascript
  // about-us就是about-us这个page的handle
  {{ pages.about-us.title }}
  {{ pages["about-us"].title }}
  
  articles['/blogName/aaaaa']	// 这里是这个blog的article的handle
  ```

##### all_products

- 获取所有的产品

```javascript
{{ all_products['wayfarer-shades'].title }}	// 可以使用产品的handle直接获取产品对象
```

##### articles

- 获取所有的文章

##### blogs

- 获取所有的blog

##### blog

```javascript
blog.all_tags	// 获取所有的tags
blog.articles	// 获取blog下所有的articles
blog.articles_count	// 获取blog下articles数量
```

##### collections

- 获取所有的collection

##### collection

```javascript
collection.default_sort_by	// 获取默认的排序方式
collection.sort_by	// 获取当前的排序方式，如果没有返回的是空字符串
/collections/widgets?sort_by=best-selling	// sort_by参数

// 一个排序的下拉菜单的实现
<select name="sort_by" onchange="location.href='{{ collection.url }}?sort_by=' +this.options[this.selectedIndex].value;">
  {% for option in collection.sort_options %}
    <option value="{{ option.value }}"
      {% if collection.sort_by != '' %}
        {% if option.value == collection.sort_by %}selected{% endif %}
      {% else %}
        {% if option.value == collection.default_sort_by %}selected{% endif %}
      {% endif %}
    >{{ option.name }}</option>
  {% endfor %}
</select>
```

##### current_page

- 获取全局的当前的分页页码

##### current_tags

- 获取当前的tags，如果是collection则是collection的tags，如果是product则是product的tags

##### customer

- 获取当前登陆的用户

##### handle

- 获取当前页面所属对象的handle

##### images

- 通过名字获取指定的图片

```javascript
{% assign image = images['my-image.jpg'] %}
<img src="{{ image }}" alt="{{ image.alt }}">
```

##### image

```javascript
product.featured_media.preview_image	// preview_iamge属性只能在_media对象上获取
image.product_id	// 获取image对应的产品id
```

##### linklist

- 是后台`Navigation`菜单里面的对象，我们一般获取的是`main-menu`，当然我们可以在后台添加新的menu

```javascript
{% assign main_menu = linklists.main-menu %}	// 从linklists获取Main Menu对象
{{ main_menu }}	// 获取main menu的层级，返回一个数字
 
// 遍历main-menu的links
{% for link in linklists.main-menu.links %}
  <a href="{{ link.url }}">{{ link.title }}</a>	// 获取link的title和url
{% endfor %}
```

##### pages

- 获取所有的页面

```javascript
<h1>{{ pages.about.title }}</h1>
<p>{{ pages.about.author }} says...</p>
<div>{{ pages.about.content }}</div>
```

##### page_description

- 获取页面的description原信息

```javascript
{% if page_description %}
  <meta name="description" content="{{ page_description }}" />
{% endif %}
```

##### paginate

- 分页对象

```javascript
{{ paginate.current_offset }}	// 当前的offset，从0开始
{{ paginate.current_page }}	// 当前页，从1开始
{{ paginate.items }} // 总数量
{{ paginate.page_size }} // 每页数量
```

##### product

```javascript
product.available	// 当前产品是否能够购买，如果产品的variants的quantity为0 就不能购买
product.collections	// 获取产品所属的所有的collections
product.compare_at_price	// 获取产品所有的variants的最低价格，如果没有则返回nil
product.compare_at_price_min	// 获取产品所有的variants的最低价格，如果没有则返回0
product.content	// 返回产品的description
product.description	// 同上
product.featured_iamge	// 返回product的第一张图片
product.first_available_variant	// 第一个variant
product.has_only_default_variant	// 是否只有默认的variant
product.images	// 所有的图片
product.media	// media
product.options	// 获取该产品下varitant所有的options，例如Color、Size、Material
product.options.size	// options的数量
product.options_by_name['Color'].values	// 通过名成获取option
product.price_max	// 返回产品最高价格
product.price_min // 返回产品最低价格
product.selected_variant	// 获取url的variant参数，自动找到对应的variant
product.selected_or_first_available_variant
product.tags	// 返回产品所有的tag，使用{% if product.tags contains tag %}去判断是否包含某个tag
product.template_suffix	// 返回产品的模板文件前缀，例如如果该产品使用的是product.wholesale.liquid那么它就返回wholesale，如果使用默认模板那么返回nil
```

##### recommendations

- 通过当前的产品/collection，返回相关联的产品

```javascript
{% if recommendations.performed %}
  {% if recommendations.products_count > 0 %}
    {% for product in recommendations.products %}
      {{ product.title | link_to: product.url }}
    {% endfor %}
  {% endif %}
{% else %}
  <div class="placeholder">Placeholder animation</div>
{% endif %}
```

##### serach

- 搜索结果可以是`article/page/product`

```javascript
{{ search.results_count }} // 搜索结果数量
{{ search.terms }} // 搜索的字符串
{% for item in search.results %}
  <h3>{{ item.title | link_to: item.url }}</h3>
	{{item.object_type}}	// 搜索结果的类型，article/page/product
{% endfor %}
```

##### variant

- variant至少包含一个option

#### form表单

- shopify的表单都是内置的

##### contact

- 一般用于`Contact Us`
- 用户提交的信息会以邮件的方式发送给`Settings->General->Sender email`

```html
{% form 'contact' %}
  <div class="form-group">
    <label for="name">Your Name</label>
    <input type="text" class="form-control" id="name" name="contact[name]">
  </div>
  <div class="form-group">
    <label for="email">Your E-mail</label>
    <input type="email" class="form-control" id="email" name="contact[email]">
  </div>
  <div class="form-group">
    <label for="phone">Your Phone</label>
    <input type="text" class="form-control" id="phone" name="contact[phone]">
  </div>
  <div class="form-group">
    <label for="address">Your Address</label>
    <input type="text" class="form-control" id="address" name="contact[address]">
  </div>
  <div class="form-group">
    <label for="detail">Description</label>
    <textarea class="form-control" id="detail" rows="4" name="contact[body]"></textarea>
  </div>
  <div class="modal-submit">
    <button type="submit" class="btn submit-btn">Submit</button>
  </div>
{% endform %}
```

##### guest_login

- 可以实现`login as guest`的功能，会跳转回之前的地址并继续，一般会在checkout的时候跳转到登陆页面，然后在登陆页面提交着表单即可重定向到匿名支付页面

- 如果想要任意地方直接跳转到支付界面，可以不用这个`form`，直接这样做:

  ```html
  <form action="/cart" method="post">
    <button name="checkout">Coutinue</button>
  </form>
  ```


## Shopify API开发

- 要想调用API，首先要先在store里面创建一个APP，创建的时候需要选择相应的权限(`Access Scope`)，后面可以添加的。创建完成就能有API Key和Password了
- 每个APP每分钟最多1000个请求，每秒最多50个请求，reset api每秒才2个，各个API的[频率限制](https://shopify.dev/api/usage/rate-limits)，但是计算就有点迷了，特别是graphql有自查询的时候

### [shopify graphql api](https://shopify.dev/api/admin-graphql#top)

- 上面文档页面有所有的endpoint

```javascript
// api官方文档给的那个Shopify.Utils.loadCurrentSession(req, res)例子是针对web app的，我们完全可以自己用脚本来写
const {Shopify, ApiVersion} = require("@shopify/shopify-api");

Shopify.Context.initialize({
  API_KEY: 'xxxxx',
  API_SECRET_KEY: 'xxxxx',
  SCOPES: ['read_product_listings', 'write_product_listings', 'read_products', 'write_products'],
  HOST_NAME: 'xxxxxx.myshopify.com',
  API_VERSION: ApiVersion.July21	// 这里的版本选最新的吧
})

// 发送graphql query请求
client.query({
  data: queryString,
}).then((res) => {
  console.log(JSON.stringify(res.body));
});

// 获取产品信息query
products (first: 3) {
  edges {
    node {
      id
      title
      metafields (first: 100) {	// 查询metafields，太麻烦了，而且这玩意儿还会让query cost变得很大
          edges {
            node {
              namespace
              key
              value
            }
          }
        }
    }
  }
}

// 创建产品，shopify node api graphql添加参数
client.query({
  data: {
    query: `
			mutation ProductCreate($input: ProductInput!) { // 注意这里的类型一定要和文档里面一样，该加感叹号就加感叹号，否则会报Nullability mismatch on variable $input and argument input (ProductInput / ProductInput!)错误
				productCreate(input: $input) {
					product {
						id
					}
				}
			}
		`,
    variables: {
      input: {
        title: 'abc'
      }
    }
  }
})
```

## 常用插件

- [Advanced Custom Fields](https://apps.shopify.com/advanced-custom-field?surface_detail=custom+field&surface_inter_position=1&surface_intra_position=1&surface_type=search): 扩展字段，免费里面好像这个还可以，基本能满足要求。不过我没搞懂它的custom fields和metafields有什么区别，不都差不多吗，不过推荐使用custom fields，因为可以在这个插件里面统一配置`Configuration->Advanced Custom Fields -> Products`，在这里面添加的字段会应用于所有对象上面。另外，无论哪种字段，都能够在API里面直接通过metafields获取
