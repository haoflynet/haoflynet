---
title: "暴力破解linux密码程序"
date: 2014-02-07 14:08:22
updated: 2016-09-30 13:46:00
categories: 编程之路
---
这里介绍一下怎么用程序包里破解linux加密的  就写一个程序来实现如何暴力破解它。当然，这个程序的前提是你能够拿到对方的root权限并查看到/etc/shadow里面的内容，linux当然不会让你那么轻易地拿到的。所以这里只是出于兴趣破解一下本机上的密码而已。代码如
下：

```c
#define _GNU_SOURCE  
#include <stdio.h>  
#include <stdlib.h>  
#include <unistd.h>  
#include <string.h>

char letter[37] = "abcdefghijklmnopqrstuvwxyz0123456789"; // 存放所有可能的字符，不包含特殊字符以及大小写
char result[10]; 	// 存放最终结果，假设不超过十个字符  
int minlen = 1; 	// 密码的最小长度  
int maxlen = 10; 	// 密码的最大长度  

// 这是通过/etc/shadow所获取的加密后的文本  
char *encrypted = "$6$jMzjGK/$0QVw8FM87jd3yF0wvzgXPPe1l3FOfrIA7LhGPIVCbum9es5 /tQsGMJqmaQ78IY.Hv4h6UWnvTs4cLntrPMSfM/";  
char *salt = "$6$jMzjGK//$"; 	// 由上面的文本所得到的值，crypt函数的第二个参数

// 递归尝试  
void try_next(int index, int length)  
{  
	int i;  
	if(index == length)  
		return ; // 递归结束条件  
	for(i = 0; i< 36; i++) // 把当前位置的所有情况试完  
	{  
		result[index] = letter[i]; // 给当前位置赋值  
		memset(result + index +1, letter[0], length – index -1); // index之后，length之前的字符都用character[0]即a来代替  
		if(i != 0) // i=0的情况已经判断过了  
		{  
			printf("尝试：%s\n", result);  
			if(! strcmp(encrypted, crypt(result, salt)))  
			{  
				printf("发现密码：%s\n", result);  
				exit (0);  
			}  
		}  
		try_next(index + 1, length); // 递归替换下一个位置的字符，直到找到密码或者index==length为止  
	}  
}

void try(int length, int begin, int end)  
{  
	int i;  
	for(i = begin; i<= end; i++)  
	{  
		result[0] = letter[i]; // 这一步只确定第一个字符  
		memset(result + 1, letter[0], length-1); // 第一个字符后面length前面的字符就用character[0]即a来代替  
		printf("尝试：%s\n", result);  
		if(!strcmp(encrypted, crypt(result, salt))) // 如果这时候就能够匹配那么直接推出  
		{  
			printf("发现密码：%s\n", result);  
			exit (0);  
		}  
		try_next(1, length); // 递归尝试第一个字符之后的字符  
	}  
}

int main()  
{  
	int len;  
	for(len = minlen; len <= maxlen; len++){  
		printf("\n正在尝试长度为%d的密码\n", len);  
		memset(result, 0, 10); // 初始化result数组为全0,这里并不是指字符0  
		try(len, 0, 36);  
	}  
	return 0;  
}
```

这是我第一次尝试暴力破解，虽然没有用多线程，但还是能明显感觉到其效率之低，以后得学学其他的方法。
