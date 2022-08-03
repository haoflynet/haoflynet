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

```jsx
const {
  data,	// 实际的返回值
  error, // 错误对象
  status, // 可以是loading/error
  fetchStatus, // 可以是fetching、paused、idle
  isLoading, isError, isSuccess} = useQuery(['todos'], fetchTodoList)

useQuery(['todo', todoId, { preview: true }], ...)	// 复杂的key
```



