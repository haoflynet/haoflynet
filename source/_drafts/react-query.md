- 非常好用的query库，目的是为了缓存后端api的结果，不用像以前一样，手动将结果一个一个存储到store，并且提供了一些非常好用的hook方法
- 默认支持异步
- 它并不是用于替代axios等请求库，而只是作为外层的封装，方便控制请求与结果

## 安装配置

```shell
npm i @tanstack/react-query
```

配置就是将其作为一个provider注入到app中

```jsx
const queryClient = new QueryClient()

function App() {
  return (
    // Provide the client to your App
    <QueryClientProvider client={queryClient}>
      <Todos />
    </QueryClientProvider>
  )
}
```

## 常用方法hook

### useQuery

- 用得最多的方法，用于获取数据的请求中
- 默认在以下几种情况下，数据会自动重新获取(即会重新调用请求获取数据)
  - 重新挂载当前组件实例
  - 窗口重新聚焦
  - 网络重新连接
  - 配置了最短refetch时间
- 需要为不同的请求，设置唯一的key值，如果是带参数的，可以作为数组的第二个参数第三个参数即可，甚至可以是数字、object等对象。

```javascript
const {
  data,	// 实际的返回值
  error, // 错误对象
  status, // 可以是loading/error
  fetchStatus, // 可以是fetching、paused、idle
  isFetching, // 如果是在后台获取数据，可以用这个来表示获取中的状态
  isLoading, isError, isSuccess} = useQuery(['todos'], fetchTodoList)}

useQuery(['todo', todoId, { preview: true }], ...)	// 复杂的key
         
// query fucntion可以直接获取queryKey作为参数
useQuery(['todos', {status, page}, async ({
  queryKey,
  pageParam, // pageParam只用于Infinite Queries
  signal?: AbortSignal	// 终止信号
}) => {
  const [_key, { status, page }] = queryKey
  return new Promise()
}])


const { status, fetchStatus, data: projects } = useQuery(
  ['projects', userId],
  getProjectsByUser,
  {
    enabled: !!userId, // 如果一个请求依赖于另外一个请求或者另外一个状态，可是用enabled参数，只有当enabled的时候才回去查询
    refetchOnWindowFocus: false, // 在窗口获得焦点的时候是否重新获取数据，默认为true。还可以使用focusManager.setEventListener自定义focus监听事件
  }
)
```

### useQueries

- 写多个`useQuery`默认就是并发执行的，但是如果想要实现`Promise.all(users.map(async(user) => {}))`这样的并发可以使用`useQueries`

```javascript
const userQueries = useQueries({
    queries: users.map(user => {
      return {
        queryKey: ['user', user.id],
        queryFn: () => fetchUserById(user.id),
      }
    })
  })
```

### useIsFetching

- 全局的`isFetching`状态，表示当前是否有请求在后台执行

```javascript
const isFetching = useIsFetching()
```



