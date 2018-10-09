---
title: "Swagger与其他API文档编写工具对比"
date: 2017-02-26 23:26:00
updated: 2018-10-07 14:39:00
categories: tools
---

> 随着见闻的逐渐加深，接触或者了解过一些其他的优秀的文档编写工具，由于未深入研究过，所以，仅仅在这里进行简单的列举:
>
> - [APIDOC](http://apidocjs.com/#run): 支持大量编程语言的根据注释自动生成文档
> - [ApiGen](https://github.com/ApiGen/ApiGen): PHP7的类文档自动生成工具
> - [YApi](https://github.com/YMFE/yapi): 极力推荐，开源工具，拥有其他项目的收费功能，并且也支持内网部署及二次开发
> - [eolinker](https://www.eolinker.com/#/): 暂时未了解
> - [showdoc](https://github.com/star7th/showdoc): 暂未了解

## swagger特点

swagger是我见过唯一还算将就的一个API文档制作与展示工具，其实最终都没让我找到一款完美的API文档编写工具。

swagger优点:

- 一个文件就是一个文档


- 只针对API，而不针对特定的语言的API，很多自动生成API的工具基本都是只针对特定的API的
- 支持Json和yaml来编写API文档，并且支持导出为json、yaml、markdown等格式
- 如果编写好了API了，可以自动生成相应的SDK，没错，可能你的API接口代码还没有开始写，它就能帮你制作相应的SDK了，而且支持几乎所有主流编程语言的SDK
- 支持自动生成大量主流编程语言/框架的server端
- 界面清晰，无论是editor的实时展示还是ui的展示都十分人性化，其他的API编写工具基本上都做不到这一点，如果自己仅仅用markdown来编写，又要纠结该如何展现，十分痛苦。
- 官网有直接的demo，甚至都可以不用自己搞一套服务器

swagger缺点:

- 貌似无法更改主题
- 中英文的文档都比较少，其主要原因应该是官网的文档本身就不完善，只有针对不同模块儿的介绍，却没有针对具体用户的文档
- yaml文件只能和API项目本身放在一起，这一点暂时还不知道有什么解决方案

<!--more-->

### 其他的API文档编写工具

#### Apizza

- 外观模仿postman，但是只有网页版，必须谷歌浏览器并且必须安装插件，不开源，不能确定以后是否收费
- 由于外观模仿postman，所以ui上还是不大满意
- 能够自定义环境变量，并且可以不同的环境不同的环境变量
- 拥有团队协作功能，并且有一定的权限管理功能
- 可直接在接口处编写文档，并且能够导出HTML文档，导入Postman Json或者Swagger Json
- 偶尔会有缓存没有清理的问题
- 没有mock server的功能

#### APIBlueprint

- 自定义markdown语法，用markdown来编写
- 由于自定义了太多的语法，个人认为最后的markdown文件非常混乱，因为很多时候多空格多空行不会影响结果
- 也能生成mock server
- 界面美观，但是不是很直观
- 能够导出markdown和yaml

#### RAP

- 淘宝出品，Github上start数4000+
- 可以在公司内部搭建，不同的团队都可以在上面创建团队文档和分组
- 不能定义GET、POST、PUT、DELETE之外的请求
- Model不能共享，写了一个地方另外一个地方还要写
- 只能定义200的响应，无法定义请求头、请求格式和相应格式
- 网页直接用js生成mock数据
- 界面有些地方好看，有些地方很丑。。。
- 只能导出为没有样式的html

## 安装与使用

我这里仅仅是简单地使用了swagger其中一项功能，即用`swagger-editor`编写API文档，生成yaml文件，然后通过`swagger-ui`来进行展示。由于仅仅是我本地搭建，所以两个组件都使用的docker搭建:

```shell
docker run -i -t -p 8080:8080 --name swagger-ui -d swaggerapi/swagger-ui
docker run -i -t -p 8081:8080 --name swagger-editor -d swaggerapi/swagger-editor
```

然后访问`http://127.0.0.1:8080`即可访问`swagger-ui`，`http://127.0.0.1:8081`即可访问`swagger-editor`了。

接下来就是问题最多的如何使用的问题了，在第一次使用过程中，有诸多的问题需要解决，当然，主要的就是CROS问题。

#### CROS跨域问题

在使用editor的时候你可能会用到`Try this operation`功能，即把接口定义好，想要直接进行请求调试，填上参数后网页可能会在js报这样的错误: `XMLHttpRequest cannot load http://api.haofly.net/projects/test. Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource. Origin 'http://127.0.0.1:8081' is therefore not allowed access.`这就是传说中的CROS问题了，原因是后台程序为了安全默认关闭了跨域的请求，这时候有两种方式，一种是修改nginx，使其能直接通过，一种是修改程序，使其在返回请求的时候能够附带加上CROS的信息。例如，我在Laravel下面，可以添加这样一个中间件:

```php
namespace App\Http\Middleware;
use Closure;
class EnableCrossRequestMiddleware
{
    public function handle($request, Closure $next)
    {
        $response = $next($request);
        $response->headers->set('Access-Control-Allow-Origin', 'http://127.0.0.1:8081');
        $response->headers->set('Access-Control-Allow-Headers', 'Origin, Content-Type, Cookie, Accept, Authorization, Application, X-Requested-With');
        $response->headers->set('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, OPTIONS, DELETE');
        $response->headers->set('Access-Control-Allow-Credentials', 'true');
        return $response;
    }
}
```

这样，后台程序就允许`127.0.0.1:8081`这个域进行跨域访问了。

#### OAuth2认证问题

swagger是无法自定义请求头的，这一点，其Github上面的Issues有解释，现在已经忘了，但是针对特殊的头，它还是会有特定的办法，比如OAuth2的认证，它本身就是支持的。

首先，需要在yaml文件中定义这样一些字段:

```yaml
securityDefinitions:	# 在根路径上添加这个字段
  Bearer:
    type: apiKey
    name: Authorization
    in: header
    
/projects/{projectName}:
  get:
    summary: 获取指定项目名的项目信息
    security:			# 在需要有认证的接口添加这个字段
      - Bearer: []
    parameters:
      - name: projectName
        in: path
        type: string
        description: 项目名
        required: true
    responses:
      200:
        description: 项目信息
```

之后，`swagger-editor`实时预览会出现`Security Authentication`的安全认证，可以将`token`填入其中，然后在`Try this operation`的时候勾选上`Security->Bearer`即可，可以看到自动在请求头中添加了`Authorization`字段了。

#### Swagger-ui获取解析文件的问题

其实`Swagger-ui`仅仅是接收一个url，通过该url获取yaml文件，然后负责解析而已。但是，这里的坑也是不少的。

首先，在`swagger-ui`中，默认发送的请求，是针对那个yaml文件所在的地方，这是十分坑的地方，所以yaml文件必须放在相应的API项目的文件里。暂时没有发现其他的解决方案。

其次，给定的url并不直接指向该文件的静态路径，而是需要添加CROS的响应头，所以不能直接用nginx的静态文件来处理。哎，所以基本上要做到的是，你直接访问那个url的时候，浏览器会弹出下载狂而不是直接显示那个文件的内容。

### 文档编写语法

虽然`json`比`yaml`好用，但是在这里我还是觉得`yaml`更好看，更方便，所以我这里都用`yaml`来用，并且如果要`json`，它都是可以互相转换的，语法都一样。以下来自[官方文档](http://swagger.io/specification/)

```yaml
swagger: '2.0'						# swagger的版本
info:
  title: 文档标题
  description:  描述
  version: "v1.0"					# 版本号
  termsOfService: ""				# 文档支持截止日期
  contact:							# 联系人的信息
  	name: ""						# 联系人姓名
  	url: ""							# 联系人URL
  	email: ""						# 联系人邮箱
  license:							# 授权信息
  	name: ""						# 授权名称，例如Apache 2.0
  	url: ""							# 授权URL

host: api.haofly.net				# 域名，可以包含端口，如果不提供host，那么默认为提供yaml文件的host
basePath: /							# 前缀，比如/v1

schemes:							# 传输协议
  - http
  - https
  
securityDefinitions:				# 安全设置
  api_key:
    type: apiKey
    name: Authorization				# 实际的变量名比如，Authorization
    in: header						# 认证变量放在哪里，query或者header
  OauthSecurity:					# oauth2的话有些参数必须写全
    type: oauth2
    flow: accessCode				# 可选值为implicit/password/application/accessCode
    authorizationUrl: 'https://oauth.simple.api/authorization'
    tokenUrl: 'https://oauth.simple.api/token'
    scopes:
      admin: Admin scope
      user: User scope
      media: Media scope
  auth:
  	type: oauth2
  	description: ""					# 描述
  	authorizationUrl: http://haofly.net/api/oauth/
  	name: Authorization				# 实际的变量名比如，Authorization
  	tokenUrl:
  	flow: implicit					# oauth2认证的几种形式，implicit/password/application/accessCode
  	scopes:
  	  write:post: 修改文件
  	  read:post: 读取文章
  	  
security:							# 全局的安全设置的一个选择吧
  auth:
    - write:pets
    - read:pets
  	  

consumes:							# 接收的MIME types列表
  - application/json				# 接收响应的Content-Type
  - application/vnd.github.v3+json
  
produces:							# 请求的MIME types列表
  - application/vnd.knight.v1+json	# 请求头的Accept值
  - text/plain; charset=utf-8

tags:								# 相当于一个分类
  - name: post	
    description: 关于post的接口
    
externalDocs:
  description: find more info here
  url: https://haofly.net
    
paths:								# 定义接口的url的详细信息
  /projects/{projectName}:			# 接口后缀，可以定义参数
    get:
      tags:							# 所属分类的列表
        - post	
      summary: 接口描述				 # 简介
      description: 					# 详细介绍
      externalDocs:					# 这里也可以加这个
      	description:
      	url:
      operationId: ""				# 操作的唯一ID
      consumes: [string]			# 可接收的mime type列表
      produces: [string]			# 可发送的mime type列表
      schemes: [string]				# 可接收的协议列表
      deprecated: false				# 该接口是否已经弃用
      security:						# OAuth2认证用
        - auth: 
        	- write:post
        	- read: read
      parameters:					# 接口的参数
        - name: projectName			# 参数名
          in: path					# 该参数应该在哪个地方，例如path、body、query等，但是需要注意的是如果in body，只能用schema来指向一个定义好的object，而不能直接在这里定义
          type: string				# 参数类型
          allowEmptyValue: boolean			# 是否允许为空值
          description: 项目名		  # 参数描述
          required: true			# 是否必须
          default: *				# 设置默认值
          maximum: number			# number的最大值
          exclusiveMaximum: boolean	# 是否排除最大的那个值
          minimum: number			# number的最小值
          exclusiveMinimum: boolean
          maxLength: integer		# int的最大值
          minLength: integer
          enum: [*]					# 枚举值
          items:					# type为数组的时候可以定义其项目的类型
        - $ref: "#/parameters/uuidParam"	# 这样可以直接用定义好的
      responses:					# 设置响应
        200:						# 通过http状态来描述响应
          description: Success		# 该响应的描述
          schema:					# 定义返回数据的结构
          	$ref: '#/definitions/ProjectDataResponse'	# 直接关联至某个model
          
  /another:	# 另一个接口
  	  responses:
  	  	200:
  	  		description:
  	  		schema:
  	  		  type: object
  	  		  properitis:
  	  		  	data:
  	  		  		$ref: '#/definitions/User'	# 关联
  
definitions:			# Model/Response的定义，这里的定义不强制要求返回数据必须和这个一致，但是在swagger-ui上，会展示这里面的字段。
  Product:				# 定义一个model
    type: object		# model类型
    properties:			# 字段列表
      product_id:		# 字段名
        type: integer	# 字段类型
        description: 	# 字段描述
	  product_name:
	  	type: string
	  	description: 
  ProjectDataResponse:
  	type: object
  	properties:
  		data:
  			$ref: '#/definitions/ProjectResponse'	# model之间的关联，表示在data字段里面包含的是一个ProjectResponse对象

parameters:				# 可以供很多接口使用的params
  limitParam:
    name: limit
    in: query
    description: max records to return
    required: true
    type: integer
    format: int32

responses:				# 可以供很多接口使用的responses
  NotFound:
    description: Entity not found.	
	
```

#### 支持的数据类型

```tex
integer: int32
long: int64
float
double
string
byte
binary
boolean
date
dateTime
password
```
