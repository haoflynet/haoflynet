美国的号码不能简单的用正则来判断，最好用twilio提供的接口https://www.twilio.com/docs/lookup/api



twilio的webhook有两种，一种是直接在console配置，但是只能监控异常，且时间维度是Day或者month，另外一种是发送sms的时候直接指定url。无法防止别人拿到你的密钥做坏事的情况