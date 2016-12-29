---
title: "《C和指针》——C语言补漏(函数篇)"
date: 2014-05-14 19:06:28
updated: 2016-12-29 11:13:00
categories: 韦编三绝
---
1. strcpy: 复制字符串,`char * strcpy(char _dst, char const _src);  `
   如果字符串比数组长，多余的字符仍被复制，它们将覆盖原先存储于数组后面的内存空间的值。strcpy无法解决这个问题，因为它无法判断目标字符数组的长度 

2. strncpy: 复制指定长度的字符串，比strcpy安全，`char _strncpy(char _dst, char const _src, size_t len);`

3. 其它的和上面两口子类似的有:
   剪切: `char _strcat(char _dst, char const _src); `

   比较: `int strcmp(char const _s1, char const _s2); `
   ​	`int strncmp(char const _s1, char const _s2, size_t len); `

4. 字符串查找

   ```c
   char _strchr(char const _str, int ch);第二个参数其实是字符  
   char _strrchr(char const _str, int ch);这是查找字符最后一次出现的位置  
   char _strpbrk(char const _str, char const_group);这是在查找str中第一个匹配group中任何一个字符的字符位置  
   char _strstr(char const _s1, char const_s2);在s1中查找整个s2第一次出现的起始位置，并返回一个指向该位置的指针
   size_t strspn(char const _str, char const _group);对字符计数  
   size_t strcspn(char const _str, char const _group);  
   ```

5. 上面这些都只能处理字符串，下面的可以处理任意的字节序列

   ```C
   void _memcpy(void _dst, void const _src, size_t length);  
   void _memmove(void _dst, void const _src, size_t length);  
   void _memcmp(void const _a, void const _b, size_t length);  
   void _memchr(void const _a, int ch, size_t length);  
   void _memset(void _a, int ch, size_t length);
   ```

6. 动态内存分配:

   ```C
   void _malloc(size_t size);动态内存分配  
   void free(void _pointer);内存释放  
   如果操作系统无法向malloc提供更多的内存，malloc就返回一个NULL指针  
   void _calloc(size_t num_elements, size_t element_size);与malloc的区别是能够在返回指向内存的指针之前把它初始化为零，参数表示所需元素的数量和每个元素的字节数  
   void realloc(void _ptr, size_t new_size);用于新修改一个原先已经分配的内存块的大小  
   ```

7. ungetc: 撤销字符I/O，`int ungetc( int character, FILE * stream );`，把一个先前读入的字符返回到流中，这样它可以在以后被重新读入

8. fflush: 迫使一个输出流的缓冲区内的数据进行物理写入，不管它是否已经写满，`int fflush(FILE _stream)`

9. 文件指针的定位

   ```C
   long ftell( FILE _stream );返回流的当前位置，即下一个读取或写入将要开始的位置距离文件起始位置的偏移量  
   int fseek( FILE _stream, long offset, int from);在一个流中定位。  
   void rewind( FILE * stream );将读/写指针设置回指定流的起始位置  
   int fgetpos( FILE _stream, fpos_t _position );在这个位置存储文件的当前位置  
   int fsetpos( FILE _stream, fpos_t const _position );把文件位置设置为存储在这个位置的值
   ```

10. 改变缓冲方式

   ```C
   void setbuf( FILE _stream, char _buf);设置了另一个数组，用于对流进行缓冲，为一个流自行指定缓冲区可以防止I/O函数库为它动态分配一个缓冲区  
   int setvbuf( FILE _stream, char _buf, int mode, size_t size );参数中mode用于指定缓冲的类型
   ```

11. 临时文件

   ```C
   FILE _tmpfile(void);会创建一个文件，当文件被关闭或程序终止时这个文件便自动删除  
   char _tmpnam(char _name);临时文件的名字
   ```

12. 删除文件

   ```C
   int remove(char const _filename);删除文件  
   int rename(char const _oldname, char const _newname);文件重命名
   ```

13. 随机数<stdlib.h>

   ```C
   int rand(void);  
   void srand(unsigned int seed); 
   // 上面两句会产生伪随机数，如果实现真正的随即需要再加一句：  
   srand( (unsigned int)time( 0 ) );
   ```

14. 字符串与数值的相互转换

   ```C
   int atoi(char const _string);转换为十进制  
   long int atol(char const _string);转换为十进制  
   long int strtol(char const string, char * __unused, int base);可指定基数  
   unsigned long int strtoul( char const string, char * __unused, int base);可指定基数  
   double atof(char const _string);转换为float  
   double strtod(char const string, char _***unused);转换为double
   ```

15. 执行系统命令(stdlib.h)，`void system( char const _command );`可以执行cmd的命令

16. 排序和查找

   ```c
   void qsort(void base, size_t n_elements, size_t el_size, int (compare)(void const _, void const _));第一个参数指向需要排序的数组，第二个参数指定数组中元素的数目，第三个参数指定每个元素的长度，第四个参数是一个比较函数  
   void _bsearch(void const _key, void const _base, size_t n_elements, size_t el_size, int (_compare)(void const _, void const _));在一个已经排好序的数组中用二分法查找一个特定的元素  
   ```