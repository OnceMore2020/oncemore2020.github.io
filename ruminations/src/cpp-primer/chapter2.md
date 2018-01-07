## Chapter 2. Variables and Basic Types

### Exercise 2.1
> What are the differences between `int`, `long`, `long long`, and `short`? Between an `unsigned` and a `signed` type? Between a `float` and a `double`?

C++ 规定`short`和`int`至少16位(2字节),`long`至少32位(4字节),·`long long`至少64位(8字节)。

**注意**：`long long`为C++11新特性。

`signed`能表示负数、正数和零，`unsigned`只能表示非负数。

C/C++标准并未指定`float`、`double`和`long double`的大小，可能按照IEEE双精度浮点数标准实现。实际上，gcc、MSVC等编译环境和x86、x64、ARM等平台上，`float`按照IEEE单精度浮点数实现(`binary32`)，即:1符号位+8指数位+23尾数位;`double`按照IEEE双精度浮点数实现(`binary64`),即:1符号位+11指数位+52尾数位;32位系统上`long double`映射为`double`，64位系统上`long double`可能包括:1符号位+15指数位+64尾数位(10字节)，参考[MSVC浮点表示形式](https://msdn.microsoft.com/zh-cn/library/0b34tf65.aspx)，也可能包括:1符号位+63指数位+64位数位(16字节)，参考[What is long double on x86-64?](http://stackoverflow.com/questions/15176290/what-is-long-double-on-x86-64)；具体`long double`占多少字节，依赖于编译环境，但主要是10字节和16字节两个版本。

用法：
* 采用`int`做整型运算，`short`往往过小，而`long`通常和`long long`大小相同，如果数据值范围超过`int`，则使用`long long`。
* 数据值**不可能**为负数时，使用`unsigned`
* 直接`double`用来做浮点数运算，`float`精度往往不够，并且`double`和`float`的运算消耗相差不大，甚至在一些机器上，双精度浮点运算性能要高于单精度浮点运算，`long double`不太必要，并且计算消耗大(特别优化过的机器除外)。

参考：

- [What are the criteria for choosing between short / int / long data types?](http://www.parashift.com/c++-faq/choosing-int-size.html)
- [Difference between float and double](http://stackoverflow.com/questions/2386772/difference-between-float-and-double)
- 本书2.1.1节的Advice: Deciding which Type to Use。

程序验证(g++ GCC-5.2.0)`ex2_1.cpp`
```cpp
#include <iostream>
int main()
{
    short short_data;
    int int_data;
    long long_data;
    long long long_long_data;

    unsigned int uint_data;
    signed int sint_data;

    float float_data;
    double double_data;
    long double long_double_data;

    std::cout << "Size of datatypes:" << std::endl;
    std::cout << "short:" << sizeof(short_data) << std::endl;
    std::cout << "int:" << sizeof(int_data) << std::endl;
    std::cout << "long:" << sizeof(long_data) << std::endl;
    std::cout << "long long:" << sizeof(long_long_data) << std::endl;
    std::cout << "unsigned int:" << sizeof(uint_data) << std::endl;
    std::cout << "signed int:" << sizeof(sint_data) << std::endl;
    std::cout << "float:" << sizeof(float_data) << std::endl;
    std::cout << "double:" << sizeof(double_data) << std::endl;
    std::cout << "long double:" << sizeof(long_double_data) << std::endl;
    return 0;
}
```

编译运行
```bash
$ g++ -std=c++11 -o ex2_1 ex2_1.cpp
$ ./ex2_1
Size of datatypes:
short:2
int:4
long:8
long long:8
unsigned int:4
signed int:4
float:4
double:8
long double:16
```

注意到`long double`为16字节,`long long`和`long`都是8字节。`unsigned`和`signed`不影响字节大小，只影响固定字节长度下能表示的范围。

### Exercise 2.2
>To calculate a mortgage payment, what types would you use
for the rate, principal, and payment? Explain why you selected each type.

这是一个忧伤的问题，首先参考一下 **按揭贷款(mortgage)** 是如何计算的:

* [房贷计算器](http://fang.com/house/tools.htm)

通常会精确到小数点后两位，用`float`可以满足，但是正如前面所讲，直接采用`double`或许是最省事的方法。

### Exercise 2.3
> What output will the following code produce?
```cpp
unsigned u = 10, u2 = 42;
std::cout << u2 - u << std::endl;
std::cout << u - u2 << std::endl;
int i = 10, i2 = 42;
std::cout << i2 - i << std::endl;
std::cout << i - i2 << std::endl;
std::cout << i - u << std::endl;
std::cout << u - i << std::endl;
```

见下题

### Exercise 2.4
> Write a program to check whether your predictions were
correct. If not, study this section until you understand what the problem is.

输出(gcc 5.2.0):
```
32
4294967264
32
-32
0
0
```

### Exercise 2.5
> Determine the type of each of the following literals. Explain
the differences among the literals in each of the four examples:
- (a) 'a', L'a', "a", L"a"
- (b) 10, 10u, 10L, 10uL, 012, 0xC
- (c) 3.14, 3.14f, 3.14L
- (d) 10, 10u, 10., 10e-2

(a): 字面字符, 宽字面字符, 字面字符串, 宽字面字符串.

(b): 十进制, unsigned十进制, long十进制, unsigned long十进制, 八进制, 十六进制.

(c): double, float, long double.

(d): 十进制, unsigned十进制, double, double.

### Exercise 2.6
> What, if any, are the differences between the following
definitions:
```cpp
int month = 9, day = 7;
int month = 09, day = 07;
```

第一行为十进制整型。

第二行`int month = 09`错误，因为八进制数不接受`9`，`day`为八进制整型
```bash
ex2_6.cpp:5:17: 错误：invalid digit "9" in octal constant
     int month = 09, day = 07;
                 ^
```

### Exercise 2.7
> What values do these literals represent? What type does each
have?
- (a) "Who goes with F\145rgus?\012"
- (b) 3.14e1L
- (c) 1024f
- (d) 3.14L

(a): Who goes with Fergus?(new line) 字符串

参考:
> [ASCII Table](http://www.theasciicode.com.ar/)

**注意**:转义字符输出时`\x`后接数字按照十六进制计算，`\`后接数字按照 **八进制** 计算，而不是十进制计算，`\0`后接数字也按照八进制计算。
所以`\145`实际上对应64+4\*8+5\*1=101，对应字母`e`。

(b): 31.4 `long double`

(c): 1024 `float`

(d): 3.14 `long double`


### Exercise 2.8
> Using escape sequences, write a program to print 2M followed
by a newline. Modify the program to print 2, then a tab, then an M, followed
by a newline.

同样注意，是按照八进制给出ASCII码的，源码`ex2_8.cpp`
```cpp
#include <iostream>

int main()
{
    std::cout << "\62\115\012";
    std::cout << "\62\t\115\012";
    return 0;
}
```

### Exercise 2.9
>Explain the following definitions. For those that are illegal,
explain what’s wrong and how to correct it.
- (a) std::cin >> int input_value;
- (b) int i = { 3.14 };
- (c) double salary = wage = 9999.99;
- (d) int i = 3.14;

(a): 错误：expected primary-expression before ‘int’，先定义再使用
```cpp
int input_value = 0;
std::cin >> input_value;
```

(b): 没有开启`-std=c++11`时，编译器只会给出一个警告，提示: warning: implicit conversion from 'double' to 'int' changes value from 3.14 to 3。开启了`-std=c++11`后，由于**列表初始化**特性，编译器会报错，提示无法将`double`转换为`int`
```cpp
double i = { 3.14 };
```

(c): 若已经声明了`wage`变量，不会报错，否则会提示使用了没有声明的变量`wage`
```cpp
double wage;
double salary = wage = 9999.99;
```

(d): 不会报错，但会被截断为3赋值给`i`
```cpp
double i = 3.14;
```

### Exercise 2.10
>What are the initial values, if any, of each of the following variables?
```cpp
std::string global_str;
int global_int;
int main()
{
    int local_int;
    std::string local_str;
}
```

`global_str`为全局变量，默认初始化为空`std::string`, `global_int`为全局变量，默认初始化为0
`local_int`为局部变量，未初始化，具有不确定值。
`local_str`为局部变量，未初始化，但是其值为`std::string`类定义的空`std::string`

**注意**: 定义于函数体内的内置类型的对象如果没有初始化，则其值未定义。类的对象如果没有显式地初始化，则其值由类决定。**建议初始化每一个内置类型的变量**。

### Exercise 2.11
> Explain whether each of the following is a declaration or a
definition:
```cpp
(a) extern int ix = 1024;
(b) int iy;
(c) extern int iz;
```

(a): 定义(`extern`但是初始化了，相当于定义)

(b): 定义

(c): 声明

**注意**: 变量可以被多次声明，但是只能定义一次。

### Exercise 2.12
>Which, if any, of the following names are invalid?
```cpp
(a) int double = 3.14;
(b) int _;
(c) int catch-22;
(d) int 1_or_2 = 1;
(e) double Double = 3.14;
```

`a`(使用了关键字`double`), `c`(使用了`-`), `d`(以数字开头)

### Exercise 2.13
>What is the value of j in the following program?
```cpp
int i = 42;
int main()
{
    int i = 100;
    int j = i;
}
```

`100`, 全局变量值被局部变量值覆盖。

### Exercise 2.14
>Is the following program legal? If so, what values are printed?
```cpp
int i = 100, sum = 0;
for (int i = 0; i != 10; ++i)
    sum += i;
std::cout << i << " " << sum << std::endl;
```

合法，输出为
```bash
100 45
```

**注意**: 这样写代码容易挨揍

### Exercise 2.15
>Which of the following definitions, if any, are invalid? Why?
```cpp
int ival = 1.01;
int &rval1 = 1.01;
int &rval2 = ival;
int &rval3;
```

(a): 合法

(b): 非法，引用初始值必须是一个对象

(c): 合法

(d): 非法，引用必须初始化

### Exercise 2.16
>Which, if any, of the following assignments are invalid? If they are valid, explain what they do.
```cpp
int i = 0, &r1 = i; double d = 0, &r2 = d;
r2 = 3.14159;
r2 = r1;
i = r2;
r1 = d;
```

(a): 合法，给`d`赋值3.14159

(b): 合法，会自动转换为`double`

(c): 合法，但是会被截断

(d): 合法，但是会被截断

### Exercise 2.17
>What does the following code print?
```cpp
int i, &ri = i;
i = 5; ri = 10;
std::cout << i << " " << ri << std::endl;
```

输出
```bash
10 10
```

### Exercise 2.18
>Write code to change the value of a pointer. Write code to
change the value to which the pointer points.

源码`ex2_18.cpp`
```cpp
int a = 0, b = 1;
int *p1 = &a, *p2 = p1;

// 修改指针p1的值
p1 = &b;
// 修改p2指向的值
*p2 = b;
```

### Exercise 2.19
>Explain the key differences between pointers and references.

**定义**:
* 指针指向其它对象
* 引用是对象的别名

**区别**:
1. 引用是 **已经存在** 的对象的别名，本身不是对象，指针本身是对象。
2. 一旦初始化，引用和对象绑定，不能再绑定到其它对象，指针可以被赋值和拷贝，也可以指向不同的对象。
4. 引用必须初始化，指针在定义的时候不必初始化

**使用建议**:
* Use reference wherever you can, pointers wherever you must.
* Avoid pointers until you can't.

### Exercise 2.20
>What does the following program do?
```cpp
int i = 42;
int *p1 = &i; *p1 = *p1 * *p1;
```

`p1`指向整型变量`i`，`i`的值变为1764(42\*42)。

### Exercise 2.21
>Explain each of the following definitions. Indicate whether any are illegal and, if so, why.
```cpp
int i = 0;
(a) double* dp = &i;
(b) int *ip = i;
(c) int *p = &i;
```

(a): 非法，不能用`int *`类型初始化`double *`类型

(b): 非法，不能用`int`类型初始化`int *`

(c): 合法

### Exercise 2.22
Assuming p is a pointer to int, explain the following code:
```cpp
if (p) // ...
if (*p) // ...
```

第一行判断`p`是否为`nullptr`

第二行判断`p`指向的变量是否非零

### Exercise 2.23
>Given a pointer p, can you determine whether p points to a valid object? If so, how? If not, why not?

不能。

### Exercise 2.24
>Why is the initialization of p legal but that of lp illegal?
```cpp
int i = 42;
void *p = &i;
long *lp = &i;
```

继承于C的`void*`可以指向任何类型的变量，故`p`合法。

而C++规定不能隐式地进行`int *`向`long *`的转换，故`lp`非法。

### Exercise 2.25
>Determine the types and values of each of the following
variables.
```cpp
(a) int* ip, i, &r = i;
(b) int i, *ip = 0;
(c) int* ip, ip2;
```

(a): `ip` 指向`int`型变量的指针，`i`为`int`型变量，`r`为对`i`的引用

(b): `ip` 为空指针,`i`为`int`型变量

(c): `ip` 指向`int`型变量的指针，`ip2`为`int`型变量

**注意** : `*`为类型修饰符，只对`ip`起作用。

### Exercise 2.26
>Which of the following are legal? For those that are illegal,
explain why.
```cpp
(a) const int buf;
(b) int cnt = 0;        
(c) const int sz = cnt;
(d) ++cnt; ++sz;        
```

(a): 非法，`const` 必须初始化

(b): 合法

(c): 合法

(d): 非法，不能修改`const`对象`sz`

### Exercise 2.27
> Which of the following initializations are legal? Explain why.
```cpp
(a) int i = -1, &r = 0;         
(b) int *const p2 = &i2;       
(c) const int i = -1, &r = 0;  
(d) const int *const p3 = &i2;
(e) const int *p1 = &i2;       
(f) const int &const r2;       
(g) const int i2 = i, &r = i;  
```

(a): 非法，`r`必须引用一个对象

(b): 合法

(c): 合法

(d): 合法

(e): 合法

(f): 非法，`const`限定符不能应用到`const int&`上

(g): 合法

### Exercise 2.28
>Explain the following definitions. Identify any that are illegal.
```cpp
(a) int i, *const cp;       // illegal, cp must initialize.
(b) int *p1, *const p2;     // illegal, p2 must initialize.
(c) const int ic, &r = ic;  // illegal, ic must initialize.
(d) const int *const p3;    // illegal, p3 must initialize.
(e) const int *p;           // legal. a pointer to const int.
```

(a): 非法，`cp`必须初始化

(b): 非法，`p2`必须初始化

(c): 非法，`ic`必须初始化

(d): 非法，`p3`必须初始化

(e): 合法，`p`指向`const int`

### Exercise 2.29
>Uing the variables in the previous exercise, which of the
following assignments are legal? Explain why.
```cpp
(a)i = ic;     
(b)p1 = p3;    
(c)p1 = &ic;   
(d)p3 = &ic;   
(e)p2 = p1;    
(f)ic = *p3;   
```

(a): 合法

(b): 非法，`p3`指向`const int`，`p1`指向`int`

(c): 非法，`ic`为`const int`

(d): 非法，`p3`为`const`指针

(e): 非法，`p2`为`const`指针

(f): 非法，`ic`为`const int`

### Exercise 2.30
>For each of the following declarations indicate whether the
object being declared has top-level or low-level const.
```cpp
const int v2 = 0; int v1 = v2;
int *p1 = &v1, &r1 = v1;
const int *p2 = &v2, *const p3 = &i, &r2 = v2;
```

`v2` 为顶层const，`p2`为底层const
`p3` 既是顶层const也是底层const
`r2` 为底层const

### Exercise 2.31
>Given the declarations in the previous exercise determine
whether the following assignments are legal. Explain how the top-level or
low-level const applies in each case.
```cpp
(a)r1 = v2;
(b)p1 = p2;
(c)p2 = p1;
(d)p1 = p3;
(e)p2 = p3;
```

(a): 合法，顶层const不影响拷贝

(b): 非法，`p2`底层const但是`p1`不是

(c): 合法，`int*`转换为`const int*`

(d): 非法，`p3`底层const但是`p1`不是

(e): 合法，`p2`和`p3`都是底层const

### Exercise 2.32
>Is the following code legal or not? If not, how might you
make it legal?
```cpp
int null = 0, *p = null;
```

非法，从`int`到`int *`的转换无效，要创建空指针，三种方法:
* 用C++11引入的`nullptr`
* 直接赋值0
* 或者引入`cstdlib`头文件，使用`NULL`预处理变量。

参考修改：
```cpp
int null = 0, *p = nullptr;
```

### Exercise 2.33
>Using the variable definitions from this section, determine
what happens in each of these assignments:
```cpp
a=42; // 给a赋值42
b=42; // 给b赋值42
c=42; // 给c赋值42
d=42; // 错误，d为int *，应改为*d = 42;
e=42; // 错误，e为const int *，应改为e = &c;
g=42; // 错误，g为const int&引用，和ci绑定，不能再绑定其它对象
```

### Exercise 2.34
>Write a program containing the variables and assignments from the previous exercise. Print the variables before and after the assignments to check whether your predictions in the previous exercise were correct. If not, study the examples until you can convince yourself you know ￼￼what led you to the wrong conclusion.

源码`ex2_34.cpp`
```cpp
#include <iostream>

int main()
{
    int i = 0, &r = i;
    auto a = r;   // a is an int (r is an alias for i, which has type int)

    const int ci = i, &cr = ci;
    auto b = ci; // b is an int (top-level const in ci is dropped)
    auto c = cr; // c is an int (cr is an alias for ci whose const is top-level)
    auto d = &i; // d is an int* (& ofan int objectis int*)
    auto e = &ci; // e is const int*(& of a const object is low-level const)

    const auto f = ci; // deduced type of ci is int; f has type const int
    auto &g = ci; // g is a const int& that is bound to ci

    a = 42; b = 42; c = 42; *d = 42; e = &c;

    return 0;
}
```

注意`auto`类型指示符是C++11新特性，编译时需要打开`-std=c++11`

### Exercise 2.35
>Determine the types deduced in each of the following definitions. Once you’ve figured out the types, write a program to see whether you were correct.
```cpp
const int i = 42;
auto j = i; const auto &k = i; auto *p = &i; const auto j2 = i, &k2 = i;
```

`j` 为`int`,`k`为`const int&`，`p`为`const int *`，`j2`为`const int`，`k2`为`const int&`。

源码`ex2_35.cpp`
```cpp

#include <iostream>
#include <typeinfo>

int main()
{
    const int i = 42;
    auto j = i;
    const auto &k = i;
    auto *p = &i;
    const auto j2 = i, &k2 = i;

    // print i means int, and PKi means pointer to const int.
    std::cout   << "j is "      << typeid(j).name()
                << "\nk is "    << typeid(k).name()
                << "\np is "    << typeid(p).name()
                << "\nj2 is "   << typeid(j2).name()
                << "\nk2 is "   << typeid(k2).name()
                << std::endl;

    return 0;
}
```

编译和运行
```bash
$ g++ -std=c++11 ex2_35.cpp
$ ./a.out
j is i
k is i
p is PKi
j2 is i
k2 is i
```
其中`i`表示`int`，`PKi`表示指向`const int`的指针。

### Exercise 2.36
>In the following code, determine the type of each variable
and the value each variable has when the code finishes:
```cpp
int a = 3, b = 4;
decltype(a) c = a;
decltype((b)) d = a;
++c;
++d;
```

`c`为`int`，`d`为`a`的引用，所有变量的值为4。

### Exercise 2.37
>Assignment is an example of an expression that yields a reference type. The type is a reference to the type of the left-hand operand. That is, if i is an int, then the type of the expression i = x is int&. Using that knowledge, determine the type and value of each variable in this code:
```cpp
int a = 3, b = 4;
decltype(a) c = a;
decltype(a = b) d = a;
```

`c`为`int`,`d`为`int`的引用。

a=3, b=4, c=3, d=3

**注意**: 编译器只分析`decltype`括号内表达式的类型，并不实际计算表达式的值，也不会实际调用括号内的函数。

### Exercise 2.38
>Describe the differences in type deduction between decltype and auto. Give an example of an expression where auto and decltype will deduce the same type and an example where they will deduce differing types.

`decltype`处理顶层const和引用的方式与`auto`有些许不同，前者会把顶层const和引用包括在内。即`auto`处理后往往还是一个对象，而`decltype`会保留引用和顶层const信息。

```cpp
int i = 0, &r = i;
// 相同
auto a = i;
decltype(i) b = i;
// 不同，c为int，而d为int&
auto c = r;
decltype(r) d = r;
```

参考stackoverflow上的两个问答: [What is the difference between auto and decltype(auto) when returning from a function?](http://stackoverflow.com/questions/21369113/what-is-the-difference-between-auto-and-decltypeauto-when-returning-from-a-fun)和 [decltype vs auto](http://stackoverflow.com/questions/12084040/decltype-vs-auto)

### Exercise 2.39
>Compile the following program to see what happens when
you forget the semicolon after a class definition. Remember the message for
future reference.
```cpp
struct Foo { /* empty  */ } // Note: no semicolon
int main()
{
    return 0;
}
```

错误信息
```bash
$ g++ ex2_39.cpp
ex2_39.cpp:1:27: 错误：结构定义后需要‘;’
 struct Foo { /* empty  */ } // Note: no semicolon
                           ^
```

### Exercise 2.40
>Write your own version of the Sales_data class.

注意使用到了C++11的新特性: **类内初始值**
```cpp
struct Sales_data
{
    std::string bookNo;
    std::string bookName;
    unsigned units_sold = 0;
    double revenue = 0.0;
    double price = 0.0;
    //...
}
```

### Exercise 2.41
>Use your Sales_data class to rewrite the exercises in §
1.5.1(Exercise 1.20-1.22), § 1.5.2(Exercise 1.23-1.24), and § 1.6(Exercise 1.25). For now, you should define
your Sales_data class in the same file as your main function.

重写`1_20.cpp`
```cpp
#include <iostream>
#include <string>

struct Sales_data
{
    std::string bookNo;
    unsigned units_sold = 0;
    double price = 0.0;
};

int main()
{
    for (Sales_data book;
         std::cin >> book.bookNo >> book.units_sold >> book.price;
         std::cout << book.bookNo << " " << book.units_sold << " " << book.price << std::endl);
    return 0;
}
```

重写`1_21.cpp`
```cpp
#include <iostream>
#include <string>

struct Sales_data
{
    std::string bookNo;
    unsigned units_sold = 0;
    double revenue = 0.0;
};

int main()
{
    Sales_data book1, book2;
    std::cin >> book1.bookNo >> book1.units_sold >> book1.revenue;
    std::cin >> book2.bookNo >> book2.units_sold >> book2.revenue;

    if (book1.bookNo == book2.bookNo)
    {
        Sales_data book_sum;
        book_sum.bookNo = book1.bookNo;
        book_sum.units_sold = book1.units_sold + book2.units_sold;
        book_sum.revenue = book1.revenue + book2.revenue;
        std::cout << book_sum.bookNo << " " <<
                     book_sum.units_sold << " " <<
                     book_sum.revenue << std::endl;
    }
    else
    {
        std::cerr << "Data must refer to same ISBN." << std::endl;
        return -1;
    }
}
```

重写`1_22.cpp`
```cpp
#include <iostream>
#include <string>

struct Sales_data
{
    std::string bookNo;
    unsigned units_sold = 0;
    double revenue = 0.0;
};

int main()
{
    Sales_data total;
    if (std::cin >> total.bookNo >> total.units_sold >> total.revenue) {
        Sales_data trans;
        while (std::cin >> trans.bookNo >> trans.units_sold >> trans.revenue) {
            if (total.bookNo == trans.bookNo) {
                total.units_sold += trans.units_sold;
                total.revenue += trans.revenue;
            }
            else
            {
                std::cout << total.bookNo << " " <<
                             total.units_sold << " " <<
                             total.revenue << std::endl;
                total = trans;
            }
        }
        std::cout << total.bookNo << " " <<
                     total.units_sold << " " <<
                     total.revenue << std::endl;
    }
    else
    {
        std::cerr << "No data?!" << std::endl;
        return -1;
    }

    return 0;
}
```

重写`ex1_23.cpp`
```cpp
#include <iostream>
#include <string>

struct Sales_data
{
    std::string bookNo;
    unsigned units_sold = 0;
    double revenue = 0.0;
};

int main()
{
    Sales_data curr_book, val_book;
    if (std::cin >> curr_book.bookNo >> curr_book.units_sold >> curr_book.revenue) {
        int cnt = 1;
        while (std::cin >> val_book.bookNo >> val_book.units_sold >> val_book.revenue) {
            if (curr_book.bookNo == val_book.bookNo) {
                ++cnt;
            }
            else {
                std::cout << curr_book.bookNo << " occurs " << cnt << " times " << std::endl;
                curr_book = val_book;
                cnt = 1;
            }
        }
        std::cout << curr_book.bookNo << " occurs " << cnt << " times " << std::endl;
    }
    return 0;
}
```


### Exercise 2.42
>Write your own version of the Sales_data.h header and use it to rewrite the exercise from § 2.6.2(p. 76)

直接把`Sales_item`的功能顺带实现，头文件`Sales_data.h`
```cpp
#ifndef CH02_EX2_42_H_
#define CH02_EX2_42_H_

#include <string>
#include <iostream>

struct Sales_data
{
    std::string bookNo;
    unsigned units_sold = 0;
    double revenue = 0.0;

    void CalcRevenue(double price);
    double CalcAveragePrice();
    void SetData(Sales_data data);
    void AddData(Sales_data data);
    void Print();
};

void Sales_data::CalcRevenue(double price)
{
    revenue = units_sold * price;
}

void Sales_data::SetData(Sales_data data)
{
    bookNo = data.bookNo;
    units_sold = data.units_sold;
    revenue = data.revenue;
}

void Sales_data::AddData(Sales_data data)
{
    if (bookNo != data.bookNo) return;
    units_sold += data.units_sold;
    revenue += data.revenue;
}

double Sales_data::CalcAveragePrice()
{
    if (units_sold != 0)
        return revenue / units_sold;
    else
        return 0.0;
}

void Sales_data::Print()
{
    std::cout << bookNo << " " << units_sold << " " << revenue << " ";
    double averagePrice = CalcAveragePrice();
    if (averagePrice != 0.0)
        std::cout << averagePrice << std::endl;
    else
        std::cout << "(no sales)" << std::endl;
}

#endif // CH02_EX2_42_H_
```

注意**头文件保护符**的使用

重写1.5.1节问题
```cpp
#include <iostream>
#include "ex2_42.h"

int main()
{
    Sales_data book;
    double price;
    std::cin >> book.bookNo >> book.units_sold >> price;
    book.CalcRevenue(price);
    book.Print();

    return 0;
}
```

重写1.5.2节问题
```cpp
#include <iostream>
#include "ex2_42.h"

int main()
{
    Sales_data book1, book2;
    double price1, price2;
    std::cin >> book1.bookNo >> book1.units_sold >> price1;
    std::cin >> book2.bookNo >> book2.units_sold >> price2;
    book1.CalcRevenue(price1);
    book2.CalcRevenue(price2);

    if (book1.bookNo == book2.bookNo)
    {
        book1.AddData(book2);
        book1.Print();
        return 0;
    }
    else
    {
        std::cerr << "Data must refer to same ISBN" << std::endl;
        return -1;  // indicate failure
    }
}
```

重写1.6节问题
```cpp
#include <iostream>
#include "ex2_42.h"

int main()
{
    Sales_data total;
    double totalPrice;
    if (std::cin >> total.bookNo >> total.units_sold >> totalPrice)
    {
        total.CalcRevenue(totalPrice);
        Sales_data trans;
        double transPrice;
        while (std::cin >> trans.bookNo >> trans.units_sold >> transPrice)
        {
            trans.CalcRevenue(transPrice);
            if (total.bookNo == trans.bookNo)
            {
                total.AddData(trans);
            }
            else
            {
                total.Print();
                total.SetData(trans);
            }
        }
        total.Print();
        return 0;
    }
    else
    {
        std::cerr << "No data?!" << std::endl;
        return -1;  // indicate failure
    }
}
```
