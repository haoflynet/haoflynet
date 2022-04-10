- 这是MongoDb官方出的rust驱动[mongo-rust-driver](https://github.com/mongodb/mongo-rust-driver)

## 安装配置

```rust
use mongodb::{Client, Collection, Database};

let client = Client::with_uri_str("mongodb://localhost:27017")?;
let database = client.database("mydb");

let collection: Collection = database.collection("col1")
```

## 增删改查

```rust
// 查询
// 单个查询，返回的是Result<Option<T>
let doc = collection.find_one(doc! {"_id": &id}, None).await;

// nightly中可以map_err和ok_or_else直接抛出错误
let doc = collection.find_one(doc! {"_id": &id}, None).await.map_err(|e| {...})?.ok_or_else(|| Error::Notfound)?;

// 批量查询，返回的是Result<Cursor<T>>
let cursor = collection.find(doc! {"name": "abc"}, None).await?;
for result in cursor {
  println!("title: {}", result?.title);
}

// 聚合查询
let pipeline = vec![
  doc! {
    "$match": {
			"status": true
    }
  }
  doc! {
    "$lookup": {
    	"from": "users",
    	"localField": "user_id",
      "foreignField": "_id",
      "as": "user"
    }
  }
]
collection.aggregate(pipeline, None).await?


// 创建
let docs = vec![
  User {
    name: "abc".to_string()
  },
  User {
    name: "def".to_string()
  }
]
collection.insert_many(docs, None).await?


// 更新


// 删除
```

