http://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html

- JWT(JSON Web Token)，是目前最流行的跨域认证解决方案

- 以前的Session方式扩展性不好，比如在集群上就比较难做到session的共享，或者不同网站之间共享

- 只需要客户端保存用户信息即可，服务器在认证成功后，会生成一个JSON对象，返回给用户，JSON中一般包含几个关键信息，比如用户ID、用户名、用户角色、过期时间等，之后服务器在获取到该值时只需解密即可

- JWT token一般是放在header头中，当然也可以放在POST请求体中

  ```shell
  Authorization: Bearer <token>
  ```

- 缺点是token一经生成，是无法中途将某个token设置为无效的，除非有额外的逻辑