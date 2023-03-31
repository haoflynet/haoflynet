## 循环

```jinja2
loop.index0	# 按0开始的索引
loop.index # 按1开始的索引
loop.first	# 是否是第一个
loop.last	# 是否是最后一个
loop.length	# 长度

{% set outer_loop = loop %}	# 循环嵌套，内层循环如何设置外层的索引值
{% set key = value %}
{% for j in a %}
    {% set key = value1 %} # 注意这里和外面是不同的scope 
    {{ outer_loop.index }}
{% endfor %}

# 可以使用namespace来实现不同的namespace的变量或者说全局变量
{% set ns = namespace(found=false) %}
{% for item in items %}
    {% if item.check_something() %}
        {% set ns.found = true %}
    {% endif %}
    * {{ item.title }}
{% endfor %}
```

