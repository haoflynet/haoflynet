## 循环

```jinja2
loop.index0	# 按0开始的索引
loop.index # 按1开始的索引
loop.first	# 是否是第一个
loop.last	# 是否是最后一个
loop.length	# 长度

{% set outer_loop = loop %}	# 循环嵌套，内层循环如何设置外层的索引值
{% for j in a %}
    {{ outer_loop.index }}
{% endfor %}
```

