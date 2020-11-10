# [Django rest framework, use different serializers in the same ModelViewSet](https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset)





```
class ProductMessageSettingsViewSet(viewsets.ModelViewSet): 继承这个类就能自动实现rest的集中方法
	def update
	def perform_update
	def partial_update
	def retrieve 获取单个
	def list 获取列表
```