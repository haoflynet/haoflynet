## 请求与响应

```python
request.body # 获取binary的请求体
request.data	# 获取json格式的请求体，是一个dict
request.data.get('field')	# 获取POST的请求
```

### 序列化

- 同时还能支持字段验证

```python
# ModelSerializer可以直接针对model进行序列化，不用定义每一个字段了
class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'name', 'age']
        
# dict转换为对象
data = {'name': 'John', 'age': 30}
serializer = MySerializer(data)
if serializer.is_valid():
  validated_data = serializer.validated_data
  instance = serializer.save()	# 如果是model可以直接这样save
else:
  print(serializer.errors)
return Response(serializer.data)
```

## 视图view

### Generic Views

- 标准view/通用view，允许快速构建与数据库模型密切映射的API视图

#### Mixins

```python
# ListModelMixin，实现列出结果集，返回200 OK响应
def list(request, *args, **kwargs):
  pass

# CreateModelMixin，实现创建和保存一个新的model实例，返回201 Created响应，如果序列化的表示中包含名为url的键，则相应的Location头将填充该值
def create(request, *args, **kwargs):
  pass

# RetrieveModelMixin，实现返回响应中现有模型的实例，返回200 OK响应，否则404 Not Found
def retrieve(request, *args, **kwargs):
  pass

# UpdateModelMixin，实现更新和保存现有模型实例
def update(request, *args, **kwargs):	# PUT更新全部
  pass
def partial_update(request, *args, **kwargs)	# PATCH更新部分
	pass

# DestroyModelMixin，删除模型实例
def destroy(request, *args, **kwargs):
  pass
```

#### Concrete View Classes

```python
class UserList(generics.ListCreateAPIView):
    queryset = User.objeclass UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

    def list(self, request):	# 覆盖视图上默认的方法
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)cts.all()
```

### API View

- 如果通用视图不适合API的需求，可以选择使用常规`APIView`类

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class ListUsers(APIView):
	authentication_classes = (authentication.TokenAuthentication,)	# 需要token认证
  permission_classes = (permissions.IsAdminUser,)	# 只有管理员用户可以访问这个视图。
  
  def get(self, request, format=None):
    usernames = [user.username for user in User.objects.all()]
    return Response(usernames)
```

### ViewSets(Controller)

- 允许将一组相关视图的逻辑组合在单个类中，类似于其它框架的`Resources`或`Controllers`
- `ViewSet`只是一种基于类的视图，不提供任何方法处理程序，而是提供诸如`.list()`和`.create()`之类的操作
- `ViewSet`的方法处理程序仅使用`as_view()`方法绑定到完成视图的响应操作
- 除了默认的几个restful路由外，如果需要其它的特别的路由，可以使用`@detail_route/@list_route`来标记，前一个在`url`中包含`pk`用于单个实例，后一个用于列表操作
- 如果继承自ModelViewSet，那么如果不重写，就不用去写create/udpate等方法了

例如: 

```python
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
      
    def create(self, request):
      pass
    def update(self, request, pk=None):
      pass
    def partial_update(self, request, pk=None):
      pass
    def destroy(self, request, pk=None):
      pass
    
    @detail_route(methods=['post'])	# 会被路由为^users/{pk}/set_password/$
    def set_password(self, request, pk=None):
      pass
    
    @list_route()
    def recent_users(self, request):
      pass
      
# 或者继承ModelViewSet，可以减少额外操作
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
      
router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls
```



# [Django rest framework, use different serializers in the same ModelViewSet](https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset)





```
class ProductMessageSettingsViewSet(viewsets.ModelViewSet): 继承这个类就能自动实现rest的集中方法
	def update
	def perform_update
	def partial_update
	def retrieve 获取单个
	def list 获取列表
```