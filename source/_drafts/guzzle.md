---
title: "PHP http请求库Guzzle使用手册"
date: 2018-05-14 10:32:00
updated: 2020-02-24 11:00
categories: php
---

## Guzzle使用

```php
$client = new GuzzleHttp\Client();
$client = new GuzzleHttp\Client([
  'base_uri' => 'http://httpbin.org',
  'timeout' => 3.0
]);

$res = $client->request('POST', 'https://api.github.com/user', [
    'auth' => ['user', 'pass'],
  	'query' => ['foo' => 'bar'],	// Query String
  	'form_params' => [], // 发送application/x-www-form-urlencoded请求
  	'multipart' => [	// 发送multipart/form-data请求
				[
            'name'     => 'foo',
            'contents' => 'data',
            'headers'  => ['X-Baz' => 'bar']
        ],
        [
            'name'     => 'baz',
            'contents' => Psr7\Utils::tryFopen('/path/to/file', 'r')
        ],
        [
            'name'     => 'qux',
            'contents' => Psr7\Utils::tryFopen('/path/to/file', 'r'),
            'filename' => 'custom_filename.txt'
        ],
    ]
]);

// 获取响应结果
$res->getStatusCode();	// 获取http status code
$res->getHeader('content-type')[0];	// 获取content-type
$res->getBody();	// 获取body，但是这里只是返回的是stream
$res->getBody()->getContent();	// 获取String格式的返回
json_decode($res->getBody());	// 获取JSON格式的返回
```

### Restful风格的请求

```php
$client->get('https://haofly.net/get');
$client->delete('https://haofly.net/delete');
$client->head('https://haofly.net/get');
$client->options('https://haofly.net/get');
$client->patch('https://haofly.net/patch');
$client->post('https://haofly.net/post');
$client->put('https://haofly.net/put');
```





发送空的request，在pool的时候如果generator循环一直不yield request的话会造成cpu一直被占用，这时候需要可以发送空的promise，代码如下

```php
      yield function() {
        return new Promise();
      };
```

每250毫秒去检查一下curl_multi_exec中的线程的执行结果

