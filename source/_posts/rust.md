---
title: "Rust 手册"
date: 2022-03-24 08:50:00
updated: 2022-03-29 22:55:00
categories: rust
---

## 安装配置

- Cargo是它的包管理工具，类似于npm，可以在这里搜索包[crates.io](https://crates.io/)
- 安装完成后`cargo, rustc, rustup`工具会在`~/.cargo/bin`中，可以讲他们加入到环境变量中

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh	# 安装rust及对应的工具链

cargo new my_project --bin	# 新建项目，如果是二进制程序就--bin，如果是创建库就--lib
cargo install --locked --path .	# 根据Cargo.lock安装，相当于npm install

cargo build	# 编译
cargo build --release # 进行一些优化进行编译，相当于npm run production
./target/debug/my_project	# 运行编译后的二进制文件
cargo run	#  

# 如果出现error E0554 may not be used on the stable release channel的错误，需要使用nightly模式来安装与性能了
rustup install nightly
cargo +nightly run ...
cargo +nightly install ...
rustup install nightly-2022-03-22	# 安装指定版本的nightly
cargo +nightly-2022-03-22 run ...	# 使用指定版本的nightly
```

- `Cargo.toml`：类似于`package.json`文件

```shell
[package]
name = "my_project"
version = "0.0.0.0"

[dependencies]	# 这里可以添加依赖项
dotenv = "0.15.0"
```

<!--more-->

## 基本语法

- 数据类型
  - bool、u8、u16、u32、u64、u128、usize、i8、i16、i32、i64、i128、isize、f32、f64、char
  - Tuple、Array
- Option: 一种可能为空的值，本质上也是枚举，None表示空，Some代表又值。(好处是能够在编译阶段就能阻止可能发生的错误)，拿它的值最好的方法就是`if let`。代码量和我们平时写的`if (val !== null)`一样，只是这相当于是强制的了
- Result: 结果，本质也是枚举，Ok表示正常返回值和Err表示异常
- `?`: 如果一个函数内部有多个可能会抛出异常的地方，可以直接在结尾使用`?`表示只要抛错，那么函数返回值就是Err，而不用使用unwrap或者if let了

```rust
println!("{} days", day); // 打印变量的值

// Option
obj.field.is_some()	// 判断某个option的字段是否有值
let val: Option<u16> = get_val()	// 获取一个可能为空的u16的值
if let Some(var1) = val {
  println!("val is: {}", var1)
} else {
  println!("val is None")
}
let var1: u16 = val.unwrap() // 如果不想写if let，那么可以直接这样取值，但是如果值为空，会直接报错panic


// Result，实现了FromIter的，可以使用一些迭代器的方法
let res: Result<u16, &str> = Ok(233)	// 这里定义res是一个Result类型，正常返回u16，如果报错则是一个字符串
if let Ok(var) = res {}
let val: u16 = res.unwrap()	// 和Option的unwrap一样，直接取正常返回值，错误直接panic报错
res.is_ok()	// 该结果是否是ok的，常用语函数返回Ok(result)，可以这样判断
res.map_err(|err| err.to_string())	// 处理错误
res.map_err(|_| println!("error"))	// 如果不关心具体某个错误就用_
res.filter_map(|r| r.parse::<i32>().ok())	// 过滤结果
```

### 基本变量

```rust
// 数字
let a = 123i32;	// 定义一个i32的数字类型
let b = 123_i32;	// 同上
std::i32::MAX	// 获取某种类型的最大值
10_i8 as u16	// 隐式转换
3_u8.pow(2)	// 计算平方
3_i32.abs()	// 计算绝对值

// 布尔
if x {}

// 字符串, str是String的切片类型，是String的一部分或全部
let s = "abc"	// s的类型为&str
let s = String::from("abc")	// String类型
let s = "abc".to_string()	// 转换为String类型
s.push("a")	// push追加单个字符
s.push_str("abc")	// 追加一个字符串

// Tuple
let n = (1, 2, 3)
n.0
n.1
let (name, age): ($str, i32) = ("abc", 123);	// 居然还能类型推导

// Array，长度是固定的，不能动态增减，向量才可以做到
let arr1 = [11, 22, 33];
let arr1: [&str; 3] = ["aa", "bb", "cc"]	// 指定数组的长度
arr1.len()	// 获取数组长度
for i in arr1.iter() {} // 遍历数组
for i in &arr1() {}	// 遍历数组2
let s1 = &arr1[0..3];	// 取数组前两个元素
let s1 = &arr1[1..=3];	// 取2到4的位置的元素
let s1 = &arr[..];	// 取所有元素


// 格式转换
my_int.to_string();	// int转字符串
my_str.as_bytes();	// 字符串转bytecode
my_str.parse::<i32>().unwrap();	// 字符串转int
Optional::from();	// 将指定的s变量转换为Option<T>的形式

// JSON格式字符串
use serde_json::Value;	// serde_json = "1.0.57"
let my_json: Value = serde_json::from_str("")?;
let field_value = my_json["field"}.as_str();
Ok(json!(res))	// 将结果转换为json格式
```

### 扩展变量

#### Vec向量

```rust
let mut v1 = Vec::new();
let mut v1 = Vec::with_capacity(10);	// 指定容量
let v2 = vec![1,2,3]
let v3 = vec!(2;3)	// 即vec![2,2,2]
assert_eq!(v1, [1]); // 可以和数组进行比较
v[n]; // 获取第几个元素
v.get(n).unwrap();	// 取第n个元素，不存在则报错
for i in v {}	// 遍历vec
v.len()	// 获取长度
v.is_empty()	// 是否为空
v.push(1)	// 在向量尾部增加元素
v.pop()	// 从尾部去掉元素
v.contains(&"abc")	// 是否包含
v.insert(1, 222)	// 在位置1插入元素
v.remove(1)	// 删除置顶位置的元素
v.clear()	// 晴空
v.append(v1)	// 将另一个vec合并到v中
v.truncate(2)	// 截断，保留n个与阿奴
v.retain(|x| *x > 20) // 只保留满足条件的元素，相当于filter
v.drain(1..=3)	// 删除并返回指定范围的元素
v.split_off(2); // 删除并返回前n个元素

if !v1.is_empty() {
  let first = v1[0] // 获取第一个元素
}
```
#### Struct结构体(类)

```rust
// Struct结构体(有点像类)
#[derive(Debug)]	// 加上这一行才能正确地用println打印，println("{:?}", user)或者println("{:#?}", user)
struct User {
  name: String,
  age: u32,
  email: String
}
let email = String::from("a@b.com")
let user = User {
  name: String::from("ac"),
  age: 27,
  email,	// 居然也能和js一样简写
}
let user2 = User {
  name: String::from("ab"),
  ...user1	// 但是这种简写方式只适用于可以Copy的变量，不能Copy的变量例如String是不行的
  ...user1.clone()	// 即使是不能copy的也可以直接用
}
user.name // 访问结构体的字段

struct Color(i32, i32, i32); // 没有字段名的结构体，常用语比较简单的情况
let a = Color(0, 0, 0)
// 给结构体增加方法
impl User {
  fn func1(&self) -> i32 {
    self.age + 10
  }
}
user1.func1()	// 这样就能直接调用了，有点儿像类了
```
#### Enum枚举
```rust
enum Gender {
  Male,
  Female
}
impl Gender {
  fn isMale(&self) -> bool {
    return *self as u8
  }
}
let a: Gender = Gender::Male;
let b = Gender::Female as i32;	// 1
```
#### Trait(抽象类)
```rust
triat Playable {
  fn play(&self);
  fn pause(&self) {
    println!("pause")
  }
  fn get_duration(&self) -> f32
}
struct Audio {name: String, duration: f32}
impl Playble for Audio {	// 对，用结构体来实现
  fn play(&self) {}
  fn get_duration(&self) -> f32 {
    self.duration
  }
}
```
#### Iterator迭代器
```rust
.map(|x| x + 1)	// 这就和js中的map类似了
.next()	// 取下一个元素，一定是一个Option<T>的类型
.collect() // 将迭代器的元素收集到指定的类型中
let val2: Vec<_> = val1.iter().collect();	// 这里的<_>表示不指定类型，因为编译器能自动推导
.collect::<Vec<Document>>()	// 转换为指定的类型
```

#### BSON序列化和反序列化

- 很多类型的变量都能表示为BSON值

```rust
bson::from_bson()	// 序列化
bson::from_document()	// 反序列化
```

### 流程控制

```rust
for i in 1..5 {}	// 生成1到4的整数
for i in 1..=5 {}	// 生成1到5的整数

// if 语句
if COND1 {} else if COND2 {} else {}	// if...else if...else
// 如果分支最后一行没有分号结尾，那么表达式的值就为那一行的结果
// 每个分支的返回值的类型必须相同
// 可以每个分支都不返回结果，那么返回值为()，如果其中有一个返回了结果，那么必须有else语句，否则会报错
let a = if x < 10 {	
  x + 10
} else {
  x
}

// while循环
while x < 5 {
  break
  continue
}

// loop循环，相当于没有条件的while，只能用break来终止
loop {
  break;
}
```

### 文件操作

```rust
let my_str = include_str!("filename");	// 将文件内容读取为字符串
```

## 测试

- 可以在每个文件的下面编写针对当前文件的测试，他们只有在`cargo test`的时候才会运行，在`cargo build`的时候不会

```rust
#[cfg(test)]
mod tests {
  #[test]
  fn test1() {
    assert_eq!(2 + 2, 4);
  }
  
  #[test]
  fn test2() {
    panic!("fail"); 
  }
}
```

## TroubleShooting

- **failed to run custom build command for `openssl-sys v0.9.66`**: 执行`sudo apt install libssl-dev pkg-config -y`
- **type ascription is experimental **: 在使用某些实验方法的时候可能会有这个错误，此时只需要将`#![feature(type_ascription)]`放到整个项目入口文件的开头即可`main.rs`或者`lib.rs`
- **error: no rules expected the token `aarch64_apple`**: 目前我仅在2022-03-22后的几个版本遇到过这个问题，安装`rustup install nightly-2022-03-22`版本可以解决(注意使用的时候也需要指定版本`cargo +nightly-2022-03-22`)，当然如果最新的修复了，可以尝试一下最新的版本
