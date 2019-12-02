---
title: "java 手册"
date: 2016-06-27 22:52:39
updated: 2019-11-30 21:21:00
categories: java
---

### 安装方法

参考[How To Install Java with Apt-Get on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04)

### 数据类型

- `final`关键字: 修饰类表示该类不能被继承，内部所有成员变量都是final的; 类的`private`方法也会隐式地指定为`final`方法。修饰变量时，如果是基本数据类型的变量，则其数值在初始化之后就不能更改; 如果是引用类型的变量，则初始化后不能被指向另一个对象。

#### Integer/Long数字

```java
a.longValue();	// 整型转长整型
longValue.intValue;	// long转换为int
1L;	// 直接将数字转换成Long型
long.toString(123);	// 整型转字符串
(byte)1;	// int to byte，int转字节
```

#### String/StringBuffer字符串

与`String`不同的是，`StringBuffer`和`StringBuilder`类的对戏那个能够被多次修改，并且不产生新的未使用的对戏那个。

```java
// String
String a = "World";
String b = new String(array);	// 将array拼接成字符串
String[] c = new String[] {"A", "B", "C"};
int len = b.length();			// 得到字符串长度
b.concat(a);					// 连接字符串
b + a;							// 连接字符串
System.out.printf("test %s", a);
System.format("test %s", a);// 格式化字符串
b.charAt(0);					// 得到指定索引的字符
a.compareTo(Object o);			
a.compareToIgnoreCase(String str);// 比较字符串
a.startsWith(String prefix);
a.endsWith(String suffix);			// 验证字符串是否以某个子字符串结尾
a.indexOf(String str);				// 返回子字符串首次出现的位置
a.matches(".*?");					// 验证字符串是否复合正则表达式
a.replaceAll(String regex, String replacement); // 替换字符串
String[] strArr = a.split(String regex);			// 拆分字符串，字符串分隔/字符串分割
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

// Json字符串转换为Dto
MyDto myDto = new Gson().fromJson(jsonString, MyDto.class);
```

#### Array/Vector/Stack/Enumeration数组

```java
// 初始化&赋值
typeName[] arrayName; // 声明数组的基本方式，也可以typeName arrayName[]
typeName arrayName[][] = new typeName[3][4];	// 定义多维数组
double[] myList = new double[5];	// 创建指定长度的数组
List<String> names = Arrays.asList("xxx","yyy","zzz");	// 直接初始化固定长度的数组，但是要超过一个元素才行
List<String> names = new ArrayList<>();	// 初始化一个空数组，之后用add添加元素
list1.addAll(list2);	// 将数组2合并到数组1
List<String> names = new ArrayList<String>() {
  {
    for (int i = 0; i< 10; i++) {
      add("add"+i);
    }
  }
};

// 数组是否包含某个值
Arrays.asList("a", "b").contains("c");

// 遍历数组
for (double element: myList) {}
for (int i = 0 ; i < myList.size(); i++) {}


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

#### Dictionary/Hashtable/Map字典

```java
// Dictionary字典
// Hashtable

// map的初始化
HashMap<String, String> map = new HashMap<String, String>();
map.put("key", "value");
HashMap<String, String> map = new HashMap<String, String>() {
  {
    map.put("key1", "value1");
    map.put("key2", "value2");
  }
};

// Map的遍历
Map<String, String> map = new HashMap<String, String>();
// 遍历方法一
for (Map.Entry<String, String> entry : map.entrySet()) {
  System.out.println(entry.getKey(), entry.getValue);
}
// 遍历方法二
for (String key : map.keySet()) {String value = map.get(Key);}
for (String value : map.values()) {}

// Map转为Json格式字符串
String jsonStr = new Gson().toJson(myMap);
```

#### 时间处理

```java
Date date = new Date();	// 获取时间对象
Long timestamp = date.getTime();			// 获取时间戳(毫秒)
System.currentTimeMillis();	// 毫秒级时间戳
Date date = new Date(1234567890000); // 毫秒级时间戳转Date对象

// 获取今天开始的时间
Calendar calendar = Calendar.getInstance();
calendar.setTime(new Date());
calendar.set(Calendar.HOUR_OF_DAY, 0);
calendar.set(Calendar.MINUTE, 0);
calendar.set(Calendar.SECOND, 0);
Date zero = calendar.getTime();
```

#### 类/对象/方法

- 类中可以使用`static {}`设置静态代码块，有助于优化程序性能，`static块`可以放置于类中的任何地方，当类初次被加载的时候，会按照`static块`的顺序来执行每个块，并且只会执行一次。

```java
// 一个类可以有多个构造方法
public class Sample {
  static {	// 静态代码块
    long a = System.nanoTime();
    testMethod();
  }
  public Sample() {}	// 不带参数的构造方法
  public Sample(String param1) {}	// 带参数的构造方法
  private static void testMethod() {}
}

// 泛型类，T可以传入任意类型
public class MyClass<T> {
  // 成员变量
  private T t;
  public MyClass(T t) {
    super();
    this.t = t;
  }
  public T getT() {return t;}
}

// 方法中使用Optinal表示可能为null，很大程度上能帮助调用者了解内部可能返回null
public Optinal<User> getUser(Long id) {
  if (null != id) {return Optinal.of(new User());}
  return Optinal.empty();
}
Optional<user> userOp = getUser(1L);
if (userOp.isPresent()) {...} else {...}
```

#### 文件

```java
// 以行为单位读取文件
File file = new File(fileName);
BufferedReader reader = null;
reader = new BufferedReader(new FileReader(file));
String tempString = null;
int line = 1;
while ((tempString = reader.readLine()) != null) {
	System.out.println("line " + line + ": " + tempString);
	line++;
}
reader.close();

// 读取整个文件
File file = new File(fileName);
if (file.isFile() && file.exists()) {
  long fileLength = file.length();
  byte[] fileContent = new byte[(int) fileLength];
  FileInputStream in = new FileInputStream(file);
  in.read(fileContent);
  in.close();
  String[] fileContentArr = new String(fileContent);	// 结果字符串数组
}
```

#### Shell

```java
// Java执行shell命令
Process process = Runtime.getRuntime().exec("ls");
BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
while ((s = stdInput.readline()) != null) {
  System.out.println(s);
}
```

#### 包

- JavaSE程序可以打包成Jar包(与平台无关的格式)，JavaWeb程序可以打包成War包

```java
import java.io.*;		// 导入java_installation/java/io下的所有类
java -jar myjar.jar;	// 直接用命令行运行jar包
java -cp myjar.jar com.example.MainClass	// 指定jar入口
```

### 线程/进程

- `ThreadLocal`: 保证线程安全(一次HTTP请求从开始到响应都是在一个线程内部，其他用户是在其他的线程里面)

```java
Thread current = THread.currentThread();	// 获取当前进程
current.getId();	// 获取当前进程Id
```

#### 多线程

- 线程池只能放入实现`Runnable/callable`类的线程，不能放入继承`Thread`的类

```java
// 方法一、继承Thread类，缺点是无法多重继承
public class MyThread extends Thread {
  @Override
  public void run()
  {
    System.out.println("线程执行");
  }
}
new MyThread().start();	

// 方法二、实现Runnable接口，适合多线程共享资源
public class MyThread implements Runnable {
  public void run () {
    System.out.println("线程执行");
  }
}

MyThread mythread = new MyThread();
new Thread(mythread).start();
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

## TroubleShooting

- **`Expected BEGIN_OBJECT but was STRING at line 1 column 1 path $`**，这是在使用`Gson`解析字符串时的报错，一般是因为字符串非标准`Json`格式造成的

##### 扩展阅读

- [JdbcUtils.java，用于动态连接多个数据库，并执行简单的增删改查](https://blog.csdn.net/cleanness/article/details/43231473)
- [Java实现DFA算法对敏感词、广告词过滤功能示例](https://www.jb51.net/article/128990.htm)