swagger教程

### swagger特点

swagger是我见过最强大的API文档制作与展示工具，没有之一。这是我亲身感受到的优缺点:

优点:

- 一个文件就是一个文档


- 只针对API，而不针对特定的语言的API，很多自动生成API的工具基本都是只针对特定的API的
- 支持Json和yaml来编写API文档，并且支持导出为json、yaml、markdown等格式
- 如果编写好了API了，可以自动生成相应的SDK，没错，可能你的API接口代码还没有开始写，它就能帮你制作相应的SDK了，而且支持几乎所有主流编程语言的SDK
- 支持自动生成大量主流编程语言/框架的server端
- 界面清晰，无论是editor的实时展示还是ui的展示都十分人性化，其他的API编写工具基本上都做不到这一点，如果自己仅仅用markdown来编写，又要纠结该如何展现，十分痛苦。
- 官网有直接的demo，甚至都可以不用自己搞一套服务器

缺点:

- 貌似无法更改主题
- 中英文的文档都比较少，其主要原因应该是官网的文档本身就不完善，只有针对不同模块儿的介绍，却没有针对具体用户的文档
- yaml文件只能和API项目本身放在一起，这一点暂时还不知道有什么解决方案

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

虽然`json`比`yaml`好用，但是在这里我还是觉得`yaml`更好看，更方便，所以我这里都用`yaml`来用，并且如果要`json`，它都是可以互相转换的，语法都一样。

```yaml
swagger: '2.0'
info:
  title: 文档标题
  description:  描述
  version: "v1.0"					# 版本号

host: api.haofly.net				# 域名

schemes:							# http和https都可以
  - http
  - https
  
securityDefinitions:				# 用于OAuth2
  Bearer:
    type: apiKey
    name: Authorization
    in: header
    
basePath: /							# 前缀，比如/v1

consumes:
  - application/json				# 接收响应的Content-Type
  
produces:
  - application/vnd.knight.v1+json	# 请求头的Accept值
  
paths:
  /projects/{projectName}:			# 接口后缀，可以定义参数
    get:
      summary: 接口描述
      security:						# OAuth2认证用
        - Bearer: []
      parameters:					# 接口的参数
        - name: projectName			# 参数名
          in: path					# 该参数应该在哪个地方，例如path、body、query等
          type: string				# 参数类型
          description: 项目名		  # 参数描述
          required: true			# 是否必须
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
```





