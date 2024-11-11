```javascript
validate(req.body, Joi.object({
  vpc_id: Joi.string().uuid({ version: 'uuidv4' }).required(),	// 验证uuid v4
}).unknown(true)) // unknown表示允许其他无需验证的字段存在

ports: Joi.array().items(
  Joi.string().pattern(/^\d+$/)
).when('need_public_ip', { // 通过其他字段判断
  is: true,
  then: Joi.array().min(1),
  otherwise: Joi.array().min(0)
}).required(),
```

