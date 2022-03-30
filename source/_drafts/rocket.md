rust rocket

rust的rest api框架



```rust
// main.rs

routes::mount(rocket)
	.mount("/", rocket_cors::catch_all_options_routes())
	.manage(cors.clone())	// 托管状态state
	.launch()
	.await
	.unwrap();
```

## Request

### Request Guards

- 定义一个FromRequest，并指定类型，当在接口中要使用该类型的时候，会先执行其from_request
- 可以用于验证api或者用户的token
- 如果我们在同一个请求每次都会执行所有代码，如果我们要去数据库查询token次数就比较多了，所以框架还提供了一个cache的方法，不过这个方法好像依然是针对同一个请求进行cache的

```rust
struct ApiKey(String);

#[derive(Debug)]
enum ApiKeyError {
    BadCount,
    Missing,
    Invalid,
}

impl<'a, 'r> FromRequest<'a, 'r> for ApiKey {
    type Error = ApiKeyError;

    fn from_request(request: &'a Request<'r>) -> request::Outcome<Self, Self::Error> {
        let keys: Vec<_> = request
      		.headers()	// rocket::http::HeaderMap对象，常用方法有.contains("key")、.get("key")是一个迭代器、.get_one("key")
      		.get("x-api-key")
      		.collect();
        match keys.len() {
            0 => Outcome::Failure((Status::BadRequest, ApiKeyError::Missing)),
            1 => Outcome::Failure((Status::BadRequest, ApiKeyError::Invalid)),
            _ => Outcome::Failure((Status::BadRequest, ApiKeyError::BadCount)),
        }
      
      	// 使用local_cache缓存request local state
      	let user_result = request.local_cache(|| {
            let db = request.guard::<Database>().succeeded()?;
            request.cookies()
                .get_private("user_id")
                .and_then(|cookie| cookie.value().parse().ok())
                .and_then(|id| db.get_user(id).ok())
        });
      	// 异步的request local cache
      	let user_result = request.local_cache_async(async {})

      	Outcome::Success(val)	// 返回正确的对象
    }
}

#[get("/sensitive")]
fn sensitive(key: ApiKey) -> &'static str {	// 每次都会先执行上面的from request
    "Sensitive data."
}
```

## 状态 State

- 默认就是线程安全的
- 托管状态是全局的，请求本地状态是当前线程/当前请求的，相当于当前请求的一个上下文

```rust
use std::sync::atomic::AtomicUsize;

struct HitCount {
    count: AtomicUsize
}

rocket::ignite()
	.manage(HitCount { count: AtomicUsize::new(0) })
	.manage(Config::from(user_input));

// 在接口中获取State
use rocket::State;

#[get("/count")]
fn count(hit_count: State<HitCount>, config: State<Config>) -> String {
    let current_count = hit_count.count.load(Ordering::Relaxed);
    format!("Number of visits: {}", current_count)
}
```

