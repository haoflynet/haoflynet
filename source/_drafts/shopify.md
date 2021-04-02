shopify开发

## Shopify开发

### Liquid手册

#### 模板结构

- `templates/index.liquid`就是首页了

##### assets

- 可以用`scss`来写`css`非常方便，只需要在`assets`里新建一个文件，例如`styles.scss.liquid`，然后`layout/theme.liquid`中引用即可`{{ 'styles.scss.css' | asset_url | stylesheet_tag }}`

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

##### FIlters

- 需要注意的是`paginate`和`sort`不能混合使用，但是有些对象自带了`sort`功能的，可以参考[collection](#collection)

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
// Match filters，能够进行一些基本的数学运算，包括abs、at_most、at_least、ceil、devided_by、floor、minus、plus、round、times、modulo(求余)
// Media filters，包括external_video_tag、external_video_url、img_tag、img_url、media_tag、model_viewer_tag、video_tag
// Money filters，跟钱price有关的一些运算，包括money、money_with_currency、money_without_trailing_zeros、money_without_currency
 
// img_tag，以直接应用于product、variant、line item、collection、image对象，可以指定参数，第一个参数为alt，第二个参数为class，例如
{{ 'smirking_gnome.gif' | asset_url | img_tag: 'Smirking Gnome', 'cssclass1 cssclass2' }} // 会输出:
<img src="//cdn.shopify.com/s/files/1/0147/8382/t/15/assets/smirking_gnome.gif?v=1384022871" alt="Smirking Gnome" class="cssclass1 cssclass2" />


{{ line_item | img_url: '1024x' }} 
{{ 'logo.png' | asset_img_url: '300x' }}	// 返回assets中的图片，并且能指定大小
{{ 'size-chart.pdf' | file_url }}
{{ 'logo.png' | file_img_url: '1024x768' }}	// 返回files中的图片
{{ product | img_url: '400x400', crop: 'bottom' }}
{{ product | img_url: '400x400', scale: 2 }}	// 缩放
{{ product | img_url: '400x400', format: 'pjpg' }}	// 设置格式
  
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
  
  {% for part in paginate.parts %}
    <a href="{{ part.url }}" {% if forloop.index == paginate.current_page %}class="active"{% endif %}>{{ part.title }}</a>
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

#### Objects/常用对象

- 对象的`handle`适用起来非常方便，可以直接通过`handle`找到对象，而这个`handle`其实就是url后缀，例如

  ```javascript
  // about-us就是about-us这个page的handle
  {{ pages.about-us.title }}
  {{ pages["about-us"].title }}
  
  articles['/blogName/aaaaa']	// 这里是这个blog的article的handle
  ```

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

#### form表单

- shopify的表单都是内置的

##### Contact

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



