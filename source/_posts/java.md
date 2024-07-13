---
title: "java 手册"
date: 2016-06-27 22:52:39
updated: 2023-07-26 11:56:00
categories: java
---

### 安装方法

参考[How To Install Java with Apt-Get on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04)

- JDK是Java开发的一个工具包，其他的工具包还有J2SE、JAVA SE

- JDK8和JDK1.8是两种新旧的命名方式，其实是一个东西

  | Java SE    | JDK     | 发布时间 |
  | ---------- | ------- | -------- |
  | Java SE 8  | JDK 1.8 | 2014     |
  | Java SE 11 | JDK11   | 2018     |
  | Java SE 17 | JDK 17  | 2021     |

### 数据类型

- `final`关键字: 修饰类表示该类不能被继承，内部所有成员变量都是final的; 类的`private`方法也会隐式地指定为`final`方法。修饰变量时，如果是基本数据类型的变量，则其数值在初始化之后就不能更改; 如果是引用类型的变量，则初始化后不能被指向另一个对象。

- `object.getField() == 1`: 这种比较可能出现空指针异常

- 获取对象的类: `object.getClass()`

- 使用`Optional`来减少空指针异常:

  ```java
  public static Optional<List<String>> getA(boolean a) {
    if (a) {
      String [] results = {"a", "b", "c"};
      return Optional.of(Arrays.asList(results));
    }
    return Optional.empty();	// 不用返回null或者空数组了
  }
  
  public static void test() {
    Optional<List<String>> re = getA(true);
    re.isPresent();	// 对象是否存在
    re.ifPresent(result -> {
      console.log(result);
    });
  }
  ```

#### Integer/Long/Double/Float/BigDecimal/AtomicInteger数字

- 千万不要用`Double/Float`来定义金额，因为经常会出现浮点数的精度问题，最好用大数类，例如`BigDecimal/BigInteger`
- AtomicInteger是一个线程安全整数类，同时只有一个线程可以对其操作

```java
a.longValue();	// 整型转长整型
longValue.intValue();	// long转换为int
1L;	// 直接将数字转换成Long型
String.valueOf(123); // 整型转字符串，避免用toString出现空指针异常
(byte)1;	// int to byte，int转字节
(int) myByte;	// byte to int，字节转int
(float) 1;	// int to float
new Long(12);	// Integer转Long

Math.ceil(9.2);	// 向上取整
Math.floor(9.2);// 向下取整
Math.round(9.2); // 四舍五入
Math.abs(-0.9);	// 取绝对值

a == 0 ? false : true;	// 整型转换为布尔
a ? 1 : 0;	// 布尔转换为整型

BigDecimal.ZERO;	// 直接就是BigDecimal类型的0
a.add(b);	// BigDecimal加法
a.subtract(b);	// BigDecimal减法
a.multiply(b);	// BigDecimal乘法
a.divide(b);	// BigDecimal除法
a.compareTo(b); // 比较BigDecimal，结果为0表示相当，为-1表示小于，为1表示大于，>-1表示大于等于，小于1表示小于等于。不要用equals方法来比较BigDecimal对象，如果scale不一样，会直接返回false
a.setScale(2);	// 四舍五入保留两位小数
a.setScale(2, BigDecimal.ROUND_DOWN); // 向下取整
a.setScale(2, BigDecimal.ROUND_UP); // 向上取整
```

#### String/StringBuffer字符串

与`String`不同的是，`StringBuffer`和`StringBuilder`类的对戏那个能够被多次修改，并且不产生新的未使用的对戏那个。

```java
// String
String a = "World";
String b = new String(array);	// 将array拼接成字符串
String[] c = new String[] {"A", "B", "C"};
List<String> list = Arrays.asList(c);	// String[] 转换为 List<String>
int len = b.length();			// 得到字符串长度
b.concat(a);					// 连接字符串
b + a;							// 连接字符串
System.out.printf("test %s", a);
String.format("test %s", a);// 格式化字符串
b.charAt(0);					// 得到指定索引的字符
a.compareTo(Object o);			
a.compareToIgnoreCase(String str);// 比较字符串
a.startsWith(String prefix);
a.endsWith(String suffix);			// 验证字符串是否以某个子字符串结尾
a.indexOf(String str);				// 返回子字符串首次出现的位置，验证是否包含某个子字符串，没找到返回-1
a.contains(str);			// 直接检验是否包含某个子字符串
a.matches(".*?");					// 验证字符串是否复合正则表达式
a.replaceAll(String regex, String replacement); // 替换字符串
String[] strArr = a.split(String regex);			// 拆分字符串，字符串分隔/字符串分割
a.trim();						// 移除首尾空白
Integer.parseInt(str);		// 字符串转整型
Long.parseLong(str);		// 字符串转Long型
String.join(",", new String[]{"foo", "bar"})	// 合并字符串，类似PHP的implode，字符串中间添加空格
new BigDecimal("1.00"); // String转BigDecimal
  
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

// 字符数组转字符串，不用toString方法
char[] data = {'a', 'b', 'c'};
String str = new String(data);

// ArrayList<Chracter> to String 
String getStringRepresentation(ArrayList<Character> list)
{    
    StringBuilder builder = new StringBuilder(list.size());
    for(Character ch: list)
    {
        builder.append(ch);
    }
    return builder.toString();
}

// 字符串反转
StringBuilder sb = new StringBuilder("content");
StringBuilder re = sb.reverse();

List list = new ArrayList(myCollections);	// Collections转list

// URLDecode/URLEncode，需要注意的是，如果出现特殊符号%，后面跟着中文，那么decode居然会报错
URLDecode.decode("test", "utf-8");
```

##### JSON

```java
// Json字符串转换为Dto
MyDto myDto = new Gson().fromJson(jsonString, MyDto.class);
new JsonParser().parse(jsonString).getAsJsonObject().get("key1").toString();	// 直接获取指定的key的值，而不用新建一个对象。但是有个坑是这样得到的字符串两边会带上引号。。。

// 验证是否是Json字符串
try {
  JSONObject result = JSONObject.parseObject(string);
  return null != result;
} catch (Exception e) {
  return false;
}

// 任意对象转JSON字符串
import com.google.gson.Gson;
Gson gson = new Gson();
String jsonString = gson.toJson(myObj);
System.out.println(jsonString);
```

##### 正则匹配

- java的正则匹配没有`findAll`的概念，需要自己在正则中加入类似`()*`来实现多次匹配

```java
Pattern p = Pattern.compile("(a.*?a)*", Pattern.CASE_INSENSITIVE|Pattern.MULTILINE);	// 可以配置大小写不敏感;查找多行
Matcher matcher = p.matcher("content");
// 遍历匹配结果方式一
while (matcher.find()) {
  System.out.println(matcher.group());
}
// 遍历匹配结果方式二
if (matcher.find() && matcher.groupCount() >= 1) {
  matches = new ArrayList();
  for (int i = 1; i <= matcher.groupCount(); i++) {
    System.out.println(matcher.group(i));
  }
}

// 正则替换
str.replaceAll(reg, "");
```

#### Array/Vector/Stack/Enumeration/Collections/ArrayList数组

- 数组的大小是无法改变的，如果要实现改变数组长度，可以采取新建一个数组然后返回新数组的指针的方式。

```java
// 初始化&赋值
typeName[] arrayName; // 声明数组的基本方式，也可以typeName arrayName[]
typeName arrayName[][] = new typeName[3][4];	// 定义多维数组
double[] myList = new double[5];	// 创建指定长度的数组
List<String> names = Arrays.asList("xxx","yyy","zzz");	// 直接初始化固定长度的数组，但是要超过一个元素才行
List<String> list1 = new ArrayList<>();	// 初始化一个空数组，之后用add添加元素
list1.addAll(list2);	// 将数组2合并到数组1
List<String> names = new ArrayList<String>() {
  {
    for (int i = 0; i< 10; i++) {
      add("add"+i);
    }
  }
};

Arrays.asList("a", "b").size(); // 获取数组长度length
Arrays.asList("a", "b").contains("c"); // 数组是否包含某个值

// 遍历数组
for (double element: myList) {}
for (int i = 0 ; i < myList.size(); i++) {}

// 遍历数组并移除元素
Iterator<String> iterator = myList.iterator();
while (iterator.hasNext()) {
    String item = iterator.next();
    if (item.equals("banana")) {
        iterator.remove(); // 根据条件删除元素
    }
}


// Vector类，动态数组
// Stack栈
Stack<Integer> d = new Stack<integer>();
d.push(int a);

// Enumeration枚举类型
Enumeration<String> days;	// 定义枚举变量
Vector<String> dayNames = new Vector<StringL>();
dayNames.add("Sunday");	// 添加枚举元素
days = dayNames.elements();

// 数组反转
List<String> new = Lists.reverse(lists1);

// 数组分片
List<E> subList(fromIndex, toIndex);
```

#### Set/HashSet/Stream集合

```java
String[] myList = new String[] { "a", "b" };
Set<String> mySet = new HashSet<String>(Arrays.asList(myList));	// 初始化
```

##### Stream API

- 是一系列对集合便利操作的工具集，类似`Laravel`里面的`Collection`
- Concat: 合并两个流: `Stream.concat(stream1, stream2)`
- foreach: 遍历
- map: 映射，返回新的元素
- mapToInt/mapToDouble/mapToLong: 映射成指定的数字类型，映射完成后可以使用`summaryStatistics`方法得到统计的结果然后使用`getMax/getMin/getSum/getAverage`等方法
- filter: 过滤，仅保留返回true的元素
- limit: 仅保留指定数量的元素
- sorted: 排序
- Collectors: 用于返回列表或字符串

```java
// 过滤
Record record = list.stream()
  .filter(record -> "name".equals(record.getName()))
  .findFirst()
  .orElse(null);

// 排序
Record record = list.stream()
  .sorted(Comparator.comparingInt(Record::getTime))
  .reversed()
  .collect(Collectors.toList());
```

#### Dictionary/Hashtable/Map/ConcurrentHashMap字典

- `ConcurrentHashMap`是线程安全的

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

map.containsKey(Object key);	// 是否包含某个key
map.containsValue(Object value);	// 是否包含某个value
map.equals(Object o);	// 比较指定的对象与此映射是否相等个
map.get(Object key);	// 获取某个key的值
map.isEmpty();	// 是否为空
map.put(K key, V value);	// 设置值
map.remove(Object key);	// 移除某个键值对
map.size();	// 获取键值对数量
map.values();	// 返回所有的value，是一个Collection对象

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

#### Queue队列

```java
Queue<String> queue = new LinkedList<String>();	// 定义队列
queue.offer("a");	// 添加元素，如果无法添加会返回false
queue.add("a");	// 添加元素，如果无法添加会抛出来异常
queue.poll();	// 返回第一个元素，并在队列中删除，没有会返回null
queue.remove();	// 从队列删除第一个元素，没有会抛出异常
queue.element();	// 返回第一个元素，没有会抛出异常
queue.peek();	// 返回第一个元素，没有会返回null
```

#### 时间处理

```java
Date date = new Date();	// 获取时间对象
Long timestamp = date.getTime();			// 获取时间戳(毫秒)
System.currentTimeMillis();	// 毫秒级时间戳
Date date = new Date(1234567890000); // 毫秒级时间戳转Date对象
Date date = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse("2020-05-01 00:00:00");	// 获取指定日期的date

// 获取今天开始的时间
Calendar calendar = Calendar.getInstance();
calendar.setTime(new Date());
calendar.set(Calendar.HOUR_OF_DAY, 0);
calendar.set(Calendar.MINUTE, 0);
calendar.set(Calendar.SECOND, 0);
Date zero = calendar.getTime();

// 获取ISO8601格式的时间，类似2019-12-12T12:12:12Z
TimeZone tz = TimeZone.getTimeZone("UTC");
DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
df.setTimeZone(tz);
return df.format(new Date());

// 解析CST格式的时间
String dateStr = "Wed Sep 11 10:10:10 CST 2020"; 
Date date = (Date) df.parse(df);

// 时间计算
date1.before(date2);	// 判断date1是否在date2之前

Calendar now = Calendar.getInstance()
now.setTime(date);	// 可以指定其他的date，不用非要是进Tina
now.set(Calendar.DATE, now.get(Calendar.DATE) + 7);	// 计算7天后的时间
```

#### 类/对象/方法

- 类中可以使用`static {}`设置静态代码块，有助于优化程序性能，`static块`可以放置于类中的任何地方，当类初次被加载的时候，会按照`static块`的顺序来执行每个块，并且只会执行一次。
- 泛型类使用`<T>`来表示，`? extends 类名`(上边界限定)表示只要继承某个类的都可以，`? super 类名`(下边界限定)表示只要是某个类的父类都可以，单独的`?`(无边界限定)表示没有任何限制

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

#### Function接口

- `Java8`新增的函数式编程方法，主要用来做lambda表达式

- 任何标注了`@FunctionalInterfaced`都接口都表示是一个函数式的接口

- `Functiond`源码简介:

  ```java
  @FunctionalInterface
  public interface Function<T, R> {	// T表示入参，R表示出参
    R apply(T t);
    // compose接收一个Function参数，返回时先用传入的逻辑执行apply，然后在执行当前Function的apply，
    // 相当于 a.compose(b).apply(1) = a.apply(b.apply(1))
    default <V> Function<V, R> compose(Function<? super V, ? extends T> before) {
          Objects.requireNonNull(before);
          return (V v) -> apply(before.apply(v));
    };
    // andTthen是先执行当前的逻辑，再执行传入的逻辑。
    // 相当于a.andThen(b).apply(1) = b.apply(a.apply(1))
    default <V> Function<T, V> andThen(Function<? super R, ? extends V> after) {
          Objects.requireNonNull(after);
          return (T t) -> after.apply(apply(t));
    };
    static <T> Function<T, T> identity() {
      return t -> t;
    };
  }
  ```

- 例子:

```java
Function<Integer,Integer> test=i->i+1;
test.apply(1);	// 会得到2
```

#### 异常处理

- 异常类的`getMessage()`和`toString()`方法的区别，前者仅仅返回错误的信息，如果是空指针异常，一般返回的是null，而后者则会包含异常类的类型信息。建议如果是打印日志则使用`toString()` 方法，因为更详细，如果是给用户看的信息可以使用`getMessage`方法仅展示给用户关键信息

#### 文件/文件夹

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

// 写入文件/新建文件
File file = new File(path);	// new File第二个参数如果为true，表示追加
if (!file.exists()) {
  file.createNewFile();
}
FileWriter fw = new FileWriter(file.getAbsoluteFile());
BufferedWriter bw = new BufferedWriter(fw);
bw.write(content);
bw.close();

// 新建文件夹
File dir = new File("/tmp/test/deep");
if (!dir.exists()) {
  dir.mkdirs();
}
```

#### Shell

```java
// Java执行shell命令
String cmd = "ls | grep abc";
String[] commands = {"/bin/sh", "-c", cmd}; // 加入/bin/sh可以防止很多命令执行出错或者转义出错
Process process = Runtime.getRuntime().exec(commands);
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

- **Unchecked assignment for 'java.util.ArrayList' to 'java.util.ArrayList <...>**: 可能是定义`ArrayList`的时候没有使用`<>`，可以用下面两种方法进行定义:

  ```java
  ArrayList<MyList> myList = new ArrayList<>();
  ArrayList<MyList> myList = new ArrayList<MyList>();
  ```

- **com.alibaba.fastjson.JSONException: default constructor not found.  **: `fastjson`的坑，要求对应class必须有默认的构造函数(空参数) 

- **fastjson出现$ref: $.data[2].indexs[0]**: 又是`fastjson`的坑，如果是需要序列化的对象中有对同一个对象的依赖，那么在JSON序列化中可能会将后续的对象转成这种字符串

##### 扩展阅读

- [JdbcUtils.java，用于动态连接多个数据库，并执行简单的增删改查](https://blog.csdn.net/cleanness/article/details/43231473)
- [Java实现DFA算法对敏感词、广告词过滤功能示例](https://www.jb51.net/article/128990.htm)
- [Java实现DFA算法敏感词过滤(参照上面代码的改进版，支持字符串替换)](https://gist.github.com/haoflynet/428ca120ea4669c03e3ce989997fef5b)