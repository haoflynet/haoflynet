---
title: "[转]函数式编程——CoolShell"
date: 2015-07-25 16:35:42
categories: 韦编三绝
---
原文地址：<http://coolshell.cn/articles/10822.html>

> 本篇文章写于2013年底，而今天我看来，依然是精华中的精华，就喜欢这种深入浅出的文章，带我们对函数式编程更深入的理解，并且本篇文章采用多种语言多种角度来
向我们讲解了到底什么才是函数式编程，再加上最近工作上很多的问题，才发现，其实公司之前的代码有很多优秀的地方。



原文地址：<http://coolshell.cn/articles/10822.html>

> 本篇文章写于2013年底，而今天我看来，依然是精华中的精华，就喜欢这种深入浅出的文章，带我们对函数式编程更深入的理解，并且本篇文章采用多种语言多种角度来
向我们讲解了到底什么才是函数式编程，再加上最近工作上很多的问题，才发现，其实公司之前的代码有很多优秀的地方。



当我们说起函数式编程来说，我们会看到如下函数式编程的长相：

  * 函数式编程的三大特性：  
**immutable data 不可变数据**：像Clojure一样，默认上变量是不可变的，如果你要改变变量，你需要把变量copy出去修改。这样一来，可以让你的程序少很多Bug。因为，程序中的状态不好维护，在并发的时候更不好维护。（你可以试想一下如果你的程序有个复杂的状态，当以后别人改你代码的时候，是很容易出bug的，在并行中这样的问题就更多了）  
**first class functions**：这个技术可以让你的函数就像变量一样来使用。也就是说，你的函数可以像变量一样被创建，修改，并当成变量一样传递，返回或是在函数中嵌套函数。这个有点像Javascript的Prototype（[参看Javascript的面向对象编程](http://coolshell.cn/articles/6668.html)）  
**尾递归优化**：我们知道递归的害处，那就是如果递归很深的话，stack受不了，并会导致性能大幅度下降。所以，我们使用尾递归优化技术——每次递归时都会重用stack，这样一来能够提升性能，当然，这需要语言或编译器的支持。Python就不支持。

  * 函数式编程的几个技术  
**map & reduce** ：这个技术不用多说了，函数式编程最常见的技术就是对一个集合做Map和Reduce操作。这比起过程式的语言来说，在代码上要更容易阅读。（传统过程式的语言需要使用for/while循环，然后在各种变量中把数据倒过来倒过去的）这个很像C++中的STL中的foreach，find_if，count_if之流的函数的玩法。  
**pipeline**：这个技术的意思是，把函数实例成一个一个的action，然后，把一组action放到一个数组或是列表中，然后把数据传给这个action list，数据就像一个pipeline一样顺序地被各个函数所操作，最终得到我们想要的结果。  
**recursing 递归** ：递归最大的好处就简化代码，他可以把一个复杂的问题用很简单的代码描述出来。注意：递归的精髓是描述问题，而这正是函数式编程的精髓。  
**currying**：把一个函数的多个参数分解成多个函数， 然后把函数多层封装起来，每层函数都返回一个函数去接收下一个参数这样，可以简化函数的多个参数。在C++中，这个很像STL中的bind_1st或是bind2nd。  
**higher order function 高阶函数**：所谓高阶函数就是函数当参数，把传入的函数做一个封装，然后返回这个封装函数。现象上就是函数传进传出，就像面向对象对象满天飞一样。
  * 还有函数式的一些好处  
**parallelization 并行**：所谓并行的意思就是在并行环境下，各个线程之间不需要同步或互斥。**lazy evaluation 惰性求值**：这个需要编译器的支持。表达式不在它被绑定到变量之后就立即求值，而是在该值被取用的时候求值，也就是说，语句如x:=expression; (把一个表达式的结果赋值给一个变量)明显的调用这个表达式被计算并把结果放置到 x 中，但是先不管实际在 x 中的是什么，直到通过后面的表达式中到 x 的引用而有了对它的值的需求的时候，而后面表达式自身的求值也可以被延迟，最终为了生成让外界看到的某个符号而计算这个快速增长的依赖树。**determinism 确定性**：所谓确定性的意思就是像数学那样 f(x) = y ，这个函数无论在什么场景下，都会得到同样的结果，这个我们称之为函数的确定性。而不是像程序中的很多函数那样，同一个参数，却会在不同的场景下计算出不同的结果。所谓不同的场景的意思就是我们的函数会根据一些运行中的状态信息的不同而发生变化。

上面的那些东西太抽象了，还是让我们来循序渐近地看一些例子吧。

我们先用一个最简单的例子来说明一下什么是函数式编程。

先看一个非函数式的例子：

1

2

3

4

|

int cnt;

void increment()\{

cnt++;

\}  

---|---  

那么，函数式的应该怎么写呢？

1

2

3

|

int increment(int cnt)\{

return cnt+1;

\}  

---|---  

你可能会觉得这个例子太普通了。是的，这个例子就是函数式编程的准则：**不依赖于外部的数据，而且也不改变外部数据的值，而是返回一个新的值给你**。

我们再来看一个简单例子：

1

2

3

4

5

6

7

8

9

10

|

def inc(x):

def incx(y):

return x+y

return incx

inc2 = inc(2)

inc5 = inc(5)

print inc2(5) # 输出 7

print inc5(5) # 输出 10  

---|---  

我们可以看到上面那个例子inc()函数返回了另一个函数incx()，于是我们可以用inc()函数来构造各种版本的inc函数，比如：inc2()和inc5()
。这个技术其实就是上面所说的Currying技术。从这个技术上，你可能体会到函数式编程的理念：**把函数当成变量来用，关注于描述问题而不是怎么实现**，这样
可以让代码更易读。

## Map & Reduce

在函数式编程中，我们不应该用循环迭代的方式，我们应该用更为高级的方法，如下所示的Python代码

1

2

3

|

name_len = map(len, ["hao", "chen", "coolshell"])

print name_len

# 输出 [3, 4, 9]  

---|---  

你可以看到这样的代码很易读，因为，**这样的代码是在描述要干什么，而不是怎么干**。

我们再来看一个Python代码的例子：

1

2

3

4

5

6

|

def toUpper(item):

return item.upper()

upper_name = map(toUpper, ["hao", "chen", "coolshell"])

print upper_name

# 输出 ['HAO', 'CHEN', 'COOLSHELL']  

---|---  

顺便说一下，上面的例子个是不是和我们的STL的transform有些像？

1

2

3

4

5

6

7

8

9

10

11

12

|

#include <iostream>

#include <algorithm>

#include <string>

using namespace std;

int main() \{

string s="hello";

string out;

transform(s.begin(), s.end(), back_inserter(out), ::toupper);

cout << out << endl;

// 输出：HELLO

\}  

---|---  

在上面Python的那个例子中我们可以看到，我们写义了一个函数toUpper，这个函数没有改变传进来的值，只是把传进来的值做个简单的操作，然后返回。然后，我
们把其用在map函数中，就可以很清楚地描述出我们想要干什么。而不会去理解一个在循环中的怎么实现的代码，最终在读了很多循环的逻辑后才发现原来是这个或那个意思。
下面，我们看看描述实现方法的过程式编程是怎么玩的（看上去是不是不如函数式的清晰？）：

1

2

3

4

|

upname =['HAO', 'CHEN', 'COOLSHELL']

lowname =[]

for i in range(len(upname)):

lowname.append( upname[i].lower() )  

---|---  

对于map我们别忘了lambda表达式：你可以简单地理解为这是一个inline的匿名函数。下面的lambda表达式相当于：def func(x):
return x*x

1

2

3

|

squares = map(lambda x: x * x, range(9))

print squares

# 输出 [0, 1, 4, 9, 16, 25, 36, 49, 64]  

---|---  

我们再来看看reduce怎么玩？（下面的lambda表达式中有两个参数，也就是说每次从列表中取两个值，计算结果后把这个值再放回去，下面的表达式相当于：(((
(1+2)+3)+4)+5) ）

1

2

|

print reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])

# 输出 15  

---|---  

Python中的除了map和reduce外，还有一些别的如filter, find, all,
any的函数做辅助（其它函数式的语言也有），可以让你的代码更简洁，更易读。 我们再来看一个比较复杂的例子：

计算数组中正数的平均值

1

2

3

4

5

6

7

8

9

10

11

12

13

|

num =[2, -5, 9, 7, -2, 5, 3, 1, 0, -3, 8]

positive_num_cnt = 0

positive_num_sum = 0

for i in range(len(num)):

if num[i] > 0:

positive_num_cnt += 1

positive_num_sum += num[i]

if positive_num_cnt > 0:

average = positive_num_sum / positive_num_cnt

print average

# 输出 5  

---|---  

如果用函数式编程，这个例子可以写成这样：

1

2

|

positive_num = filter(lambda x: x>0, num)

average = reduce(lambda x,y: x+y, positive_num) / len( positive_num )  

---|---  

C++11玩的法：

1

2

3

4

5

6

7

8

9

10

11

12

|

#include <iostream>

#include <algorithm>

#include <numeric>

#include <string>

#include <vector>

using namespace std;

vector num \{2, -5, 9, 7, -2, 5, 3, 1, 0, -3, 8\};

vector p_num;

copy_if(num.begin(), num.end(<span class="crayon-sy" sty
