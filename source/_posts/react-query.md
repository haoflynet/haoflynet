---
title: "React Query 使用手册"
date: 2022-08-05 18:02:30
updated: 2022-08-29 22:40:00
categories: nodejs
---
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
- **useQuery如果命中缓存，那么onSuccess这些方法是不会被调用的**
- 默认在以下几种情况下，数据会自动重新获取(即会重新调用请求获取数据)
  - 重新挂载当前组件实例
  - 窗口重新聚焦
  - 网络重新连接
  - 配置了最短refetch时间
- 需要为不同的请求，设置唯一的key值，如果是带参数的，可以作为数组的第二个参数第三个参数即可，甚至可以是数字、object等对象。
- 对于`enabled=false`的请求，如果之前已经缓存过数据了，那么会直接使用缓存的数据，并且`status === 'success', isSuccess=true`
- query function要么返回内容，要么抛出错误，不能返回undefined，否则会返回一个warning: `query data cannot be undefined`

<!--more-->

```javascript
const {
  data,	// 实际的返回值
  error, // 错误对象
  status, // 可以是loading/error
  refetch, // 用于重新获取数据的方法，可以直接调用refetch()对数据手动刷新，即使enabled=false也可以
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
    enabled: !!userId, // 如果一个请求依赖于另外一个请求或者另外一个状态，可是用enabled参数，只有当enabled的时候才回去查询，并且只要enabled满足条件会立马查询，如果不设置，每次进入页面也会立马查询，所以当把input作为条件的时候一定要看清楚，否则每次变化都会触发查询的
    refetchOnWindowFocus: false, // 在窗口获得焦点的时候是否重新获取数据，默认为true。还可以使用focusManager.setEventListener自定义focus监听事件
    retry : false, // 出错后不重试
    retry: 6, // 设置出错后重试次数
    notifyOnChangeProps: string[] | "all"	// 指定哪个属性更改后需要重新渲染，默认会自动跟踪想要的字段。这里可以配合onSuccess来优化渲染逻辑，不用每次改变都重新渲染，而是只是在onSuccess里面setStatus
    retry: (failureCount, error) => {}, // 自定义出错后逻辑
    retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000), // 设置重试的间隔时间
    keepPreviousData: true, // 在翻页查询的时候不用一次又一次地loading
    initialData: [], // 初始值，会保存在cache中，如果同时设置了staleTime，那么第一次仍然现实initialData，staleTime时间后才首次去获取数据
    initialDataUpdatedAt: 1234567890,  // 使用某个时间戳的缓存数据来初始化
    initialData: () => {	// 通过函数来初始化
      return getExpensiveTodos()
    },
    initialData: () => {	// 从另一个查询结果的缓存中获取初始化值
      return queryClient.getQueryData(['todos'])?.find(d => d.id === todoId)
    },
    placeholderData: [], // 默认值，和initialData不同的是它不会保存在cache中
    placeholderData: useMemo(() => generateFakeTodos(), []), // 也可以是个函数
    placeholderData: () => {	// 也可以从之前的缓存中取
      return queryClient
        .getQueryData(['blogPosts'])
        ?.find(d => d.id === blogPostId)
    },
    staleTime: 1000,	// 在cache中的缓存时间，过期时间内不会重新请求
    refetchInterval: 6000, // 设置自动刷新，自动刷新间隔时间
  }
)
```

### useQueries

- 写多个`useQuery`默认就是并发执行的，但是如果想要实现`Promise.all(users.map(async(user) => {}))`这样的并发可以使用`useQueries`
- 返回的是一个list，每一个item都是一个useQuery的结果

```javascript
const userQueries = useQueries({
    queries: users.map(user => {
      return {
        queryKey: ['user', user.id],
        queryFn: () => fetchUserById(user.id),
        onSuccess: (data) => {}
      }
    })
  })
```

### useMutation

- 写操作，比如create/update/delete等

```javascript
// 这里的mutation同样有isLoading、isSuccess，isError等状态
const mutation = useMutation(newTodo => {
  return axios.post('/todos', newTodo)
})
const mutation = useMutation(() => {}, {
  onMutate: variables => {return newVariables},
  onError: (error, variables, context) => {},
  onSuccess: (data, variables, context) => {
  	queryClient.invalidateQueries(['todos'])	// 可以在成功时让之前缓存的数据过期
    queryClient.setQueryData(['todo', { id: variables.id }], data) // 可以在成功时直接设置新的缓存数据
  },
  onSettled: (data, error, variables, context) => {}
})
mutation.mutate({ 参数 }) // 当执行mutate方法的时候才会去执行
await mutation.mutateAsync(todo) // 可以当Promise这样使用

// 如果一次mutation请求后想要重置error或者data，比如submit失败，重新输入后需要清除那些错误状态
mutation.reset()
```

### useIsFetching

- 全局的`isFetching`状态，表示当前是否有请求在后台执行

```javascript
const isFetching = useIsFetching()
```

### useInfiniteQuery

- 无限翻页查询

### prefetchQuery/setQueryData

- 预抓取
- 如果该query已经在缓存中则不会执行，可以设置一个staleTime来指定时间

```javascript
const prefetchTodos = async () => {
  await queryClient.prefetchQuery(['todos'], fetchTodos)	// 和正常的useQuery一样被缓存
}

queryClient.setQueryData(['todos'], todos) // 手动设置缓存数据
```

### invalidateQueries

- 使缓存的数据过期

```javascript
queryClient.invalidateQueries()	// 过期所有
queryClient.invalidateQueries(['todos'])	 // 过期指定的key

// 下面两个都会失效
const todoListQuery = useQuery(['todos'], fetchTodoList)
const todoListQuery = useQuery(['todos', { page: 1 }], fetchTodoList)

```



