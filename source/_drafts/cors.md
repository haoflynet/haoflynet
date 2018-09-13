http://www.ruanyifeng.com/blog/2016/04/cors.html





开启CORS容易造成CSRF攻击。。。





再一个就是如果程序猿偷懒将Access-Control-Allow-Origin设置为允许来自所有域的跨域请求。那么cors的安全机制几乎就无效了。不过先别高兴的太早。其实这里在设计的时候有一个很好的限制。xmlhttprequest发送的请求需要使用“withCredentials”来带上cookie，如果一个目标域设置成了允许任意域的跨域请求，这个请求又带着cookie的话，这个请求是不合法的。（就是如果需要实现带cookie的跨域请求，需要明确的配置允许来源的域，使用任意域的配置是不合法的）浏览器会屏蔽掉返回的结果。javascript就没法获取返回的数据了。这是cors模型最后一道防线。假如没有这个限制的话，那么javascript就可以获取返回数据中的csrf token，以及各种敏感数据。这个限制极大的降低了cors的风险。



所以开启CORS必须Access-Control-Allow-Origin: www.xxxhack.com

指定域，不然会被别人跨域攻击，这也就要求我们不要将用户输入的html或者script直接拿来执行了，否则仍然会有csrf攻击