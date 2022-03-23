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
```

- `Cargo.toml`：类似于`package.json`文件

```shell
[package]
name = "my_project"
version = "0.0.0.0"

[dependencies]	# 这里可以添加依赖项
dotenv = "0.15.0"
```

## 基本语法

```rust
obj.field.is_some()	// 判断某个option的字段是否有值

result.is_ok()	// 该结果是否是ok的，常用语函数返回Ok(result)，可以这样判断
```

### 文件操作

```rust
let my_str = include_str!("filename");	// 将文件内容读取为字符串
```



## TroubleShooting

- **failed to run custom build command for `openssl-sys v0.9.66`**: 执行`sudo apt install libssl-dev pkg-config -y`
