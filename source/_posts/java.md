---
title: "java 手册"
date: 2016-06-27 22:52:39
updated: 2019-01-24 22:58:00
categories: java
---

### 安装方法

参考[How To Install Java with Apt-Get on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04)

### 数据类型

#### Integer/Long数字

```java
a.longValue();	// 整型转长整型
longValue.intValue;	// long转换为int
```

#### String/StringBuffer字符串

与`String`不同的是，`StringBuffer`和`StringBuilder`类的对戏那个能够被多次修改，并且不产生新的未使用的对戏那个。

```java
// String
String a = "World";
String b = new String(array);	// 将array拼接成字符串
int len = b.length();			// 得到字符串长度
b.concat(a);					// 连接字符串
b + a;							// 连接字符串
System.out.printf("test %s", a);
System.out.format("test %s", a);// 格式化字符串
b.charAt(0);					// 得到指定索引的字符
a.compareTo(Object o);			
a.compareToIgnoreCase(String str);// 比较字符串
a.startsWith(String prefix);
a.endsWith(String suffix);			// 验证字符串是否以某个子字符串结尾
a.indexOf(String str);				// 返回子字符串首次出现的位置
a.matches(".*?");					// 验证字符串是否复合正则表达式
a.replaceAll(String regex, String replacement); // 替换字符串
a.split(String regex);			// 拆分字符串
a.trim();						// 移除首尾空白
Integer.parseInt(str);		// 字符串转整型
Long.parseLong(str);		// 字符串转Long型

// 判断字符串是否为空
str == null;
"".equals(str);
str.length <= 0;
str.isEmpty();

// StringBuffer
StringBuffer c = new StringBuffer('Hello World');
c.append(String s);		// 在字符串尾部追加
c.reverse();			// 反转字符串
c.capacity();			// 返回当前字符串的容量

// 日期时间
Date date = new Date();
System.out.println(date.toString());
```

#### Array/Vector/Stack/Enumeration数组

```java
// Array
typeName[] arrayName; // 声明数组的基本方式，也可以typeName arrayName[]
typeName arrayName[][] = new typeName[3][4];	// 定义多维数组
double[] myList = new double[5];
List<String> name = Arrays.asList("xxx","yyy","zzz");	// 直接初始化固定长度的数组
for (double element: myList) {}	// 遍历数组

// Vector类，动态数组
// Stack栈
Stack<Integer> d = new Stack<integer>();
d.push(int a);

// Enumeration枚举类型
Enumeration<String> days;	// 定义枚举变量
Vector<String> dayNames = new Vector<StringL>();
dayNames.add("Sunday");	// 添加枚举元素
days = dayNames.elements();
```

#### Dictionary/Hashtable字典

```java
// Dictionary字典
// Hashtable
```

#### 类和对象

```java
// 一个类可以有多个构造方法
public class Sample {
    public Sample() {}	// 不带参数的构造方法
    public Sample(String param1) {}	// 带参数的构造方法
}
```

#### 包

```java
import java.io.*;		// 导入java_installation/java/io下的所有类
```

### 三方库

#### Jsch SSH连接工具

一个很老很久没有更新的工具，[文档example比较全](https://www.programcreek.com/java-api-examples/?class=com.jcraft.jsch.ChannelExec&method=connect)，但是只有这个工具用户量大一点，其他的用户量太少不敢用(Apache sshd则是因为文档太少，官方文档是针对它的server端)。执行`shell`命令的时候建议使用`ChannelExec`而不是`ChannelShell`(因为后者的输出流里面类似于一个终端，会包含一些没用的命令提示符).

```java
Jsch jSch = new JSch();
jSch.addIdentity("name", prvKeyStr.getBytes, pubKeyStr.getBytes, keyPass.getBytes);	// 加载私钥公钥和私钥密码
Session session = jSch.getSession(username, ip, port);	// 新建session
session.setConfig("StrictHostKeyChecking", "no");	// 不进行静态host-key校验，否则可能出现UnknownHostKey错误
session.setTimeout(10000);	// 设置连接超时时间毫秒
session.connect();	// 连接

// 执行命令并获取返回结果
ChannelExec channelExec = (ChannelExec) this.session.openChannel("exec");
ByteArrayOutputStream out = new ByteArrayOutputStream();
ByteArrayOutputStream error = new ByteArrayOutputStream();
channelExec.setCommand("ls");	// 实际执行的命令
channelExec.setOutputStream(out);
channelExec.setErrStream(error);
channelExec.connect();
int sleepCount = 0;
do {		// 等待命令返回，官方手册是用的这种方法
    try {
        Thread.sleep(100);
    } catch (InterruptedException e) {
        result.setExitCode(1);
        result.setStderr(SERVER_EXEC_ERROR + e.getMessage());
        return result;
    }
} while (!channelExec.isClosed() && sleepCount++ < 60);
out.toString();	// 标准输出
error.toString();	// 标准错误输出
channelExec.getExitStatus();	// 获取返回状态码
```









