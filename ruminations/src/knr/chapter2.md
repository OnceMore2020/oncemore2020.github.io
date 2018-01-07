## Chapter 2 - Types, Operators, and Expressions

* **变量** 和 **常量** 时程序处理的两种基本数据对象
* **声明** 语句说明变量的名字及类型，也可以指定变量的初值
* **运算符** 指定将要进行的操作
* **表达式** 把变量和常量组合起来生成新的值
* 对象的类型决定该对象可取值的集合以及可以对该对象执行的操作

### Section 2.1 Variable Names

**重要细节**

* 变量名字是字母、数字和下划线组成的序列
* 由于库例程的名字通常以下划线开头，因此变量名不要以下划线开头
* C 对大小写敏感
* 选择变量名要能够尽量从字面上表达变量的用途，这样不容易引起混淆
* **局部变量一般使用较短的变量名（尤其是循环控制变量），外部变量使用较长的名字**

### Section 2.2 Data Types and Sizes

**重要细节**

* 基本数据类型：

|`char`|字符型（一字节）|
|`int`|整型|
|`float`|单精度浮点型|
|`double`|双精度浮点型|

* 限定符

|`long`|限定`int`和`double`|
|`short`|限定`int`|
|`signed`|限定`char`和`int`|
|`unsigned`|限定`char`和`int`|

* `short`与`int`类型至少为16位，`long`类型至少为32位，`short`类型不得长于`int`类型，`int`类型不得长于`long`类型
* `short`和`long`限定`int`时关键字`int`可以省略
* 不带限定符的`char`类型对象是否带符号取决于具体机器，但是 **可打印字符总是正值** 
* `float`,`double`与`long double`类型可以表示相同的长度，也可以表示两种或三种不同的长度。实际上，gcc、MSVC等编译环境和x86、x64、ARM等平台上，`float`按照IEEE单精度浮点数实现(`binary32`)，即:1符号位+8指数位+23尾数位;`double`按照IEEE双精度浮点数实现(`binary64`),即:1符号位+11指数位+52尾数位;32位系统上`long double`映射为`double`，64位系统上`long double`可能包括:1符号位+15指数位+64尾数位(10字节)，参考[MSVC浮点表示形式](https://msdn.microsoft.com/zh-cn/library/0b34tf65.aspx)，也可能包括:1符号位+63指数位+64位数位(16字节)，参考[What is long double on x86-64?](http://stackoverflow.com/questions/15176290/what-is-long-double-on-x86-64)；具体`long double`占多少字节，依赖于编译环境，但主要是10字节和16字节两个版本。
* 有关类型长度定义以及其它与机器和编译器有关的属性可以在`<limits.h>`和`<float.h>`中找到

> Excercise 2-1. Write a program to determine the ranges of `char` , `short` , `int` , and `long` variables, both `signed` and `unsigned` , by printing appropriate values from standard headers and by direct computation. Harder if you compute them: determine the ranges of the various floating-point types.

手动计算需要一些数字电路方面的概念。`float`和`double`这一块，参考 [Explain this code in K&R 2-1](http://stackoverflow.com/questions/24144274/explain-this-code-in-kr-2-1)，`1111e28`这个数没什么非常特别的地方，是一个属于可用区间的 *cute number*。

> delta needs to be small enough so if `fla` is the 2nd largest number, adding delta, would not sum right up to float.infinity and skip FLT_MAX

```cpp
#include <stdio.h>
#include <limits.h>
#include <float.h>

int main() {
    unsigned char uc;
    signed char sc;
    unsigned short us;
    signed short ss;
    unsigned int ui;
    signed int si;
    unsigned long ul;
    signed long sl;
    unsigned long long ull;
    signed long long sll;
    float fl, fla, fll;
    double db, dba, dbl;
    long double ldb, ldba, ldbl;

    printf("Let's compute the minimums and maximums of each type!\n");
    uc = sc = us = ss = ui = si = ul = sl = sll = ull = 0;
    fl = fla = fll = db = dba = dbl = ldb = ldba = ldbl = 0.0;

    /* signed char (minimum, maximum), unsigned char(0, maximum) */

    sc++;
    signed char tmp_sc;
    while ((tmp_sc = sc * 2) > sc)
        sc *= 2;

    printf("`signed char` maximum: %d\n", sc = sc * 2 - 1);
    printf("`signed char` minimum: %d\n", ++sc);
    printf("`unsigned char` maximum: %u\n", --uc);

    /* short int, unsigned short */

    ss++;
    signed short tmp_ss;
    while ((tmp_ss = ss * 2) > ss)
        ss *= 2;

    printf("`signed short` maximum: %d\n", ss = ss * 2 - 1);
    printf("`signed short` minimum: %d\n", ++ss);
    printf("`unsigned short` maximum: %u\n", --us);

    /* signed int, unsigned int */

    si++;
    signed int tmp_si;
    while ((tmp_si = si * 2) > si)
        si *= 2;

    printf("`signed int` maximum: %d\n", si = si * 2 - 1);
    printf("`signed int` minimum: %d\n", ++si);
    printf("`unsigned int` maximum: %u\n", --ui);

    /* signed long, unsigned long */

    sl++;
    signed long tmp_sl;
    while ((tmp_sl = sl * 2) > sl)
        sl *= 2;

    printf("`signed long` maximum: %li\n", sl = sl * 2 - 1);
    printf("`signed long` minimum: %li\n", ++sl);
    printf("`unsigned long` maximum: %lu\n", --ul);

    /* signed long long, unsigned long long */

    sll++;
    signed long long tmp_sll;
    while ((tmp_sll = sll * 2) > sll)
        sll *= 2;

    printf("`signed long long` maximum: %lli\n", sll = sll * 2 - 1);
    printf("`signed long long` minimum: %lli\n", ++sll);
    printf("`unsigned long long` maximum: %llu\n", --ull);

    /* float */
    while (fl == 0.0) {
        fll = fla;
        fla = fla + 1111e28;
        fl = (fl + fla) - fla;
    }

    printf("`float` maximum: %e\n", fll);
    printf("`float` minimum: %e\n", 0 - fll);

    /* double */
    while (db == 0.0) {
        dbl = dba;
        dba = dba + 1111e297;
        db = (db + dba) - dba;
    }

    printf("`double` maximum: %e\n", dbl);
    printf("`double` minimum: %e\n", 0 - dbl);

    printf("\nNow, let's cheat and use the helpful headers!\n");
    printf("`char`s go from %d to %d (unsigned, up to %u)\n", SCHAR_MIN, SCHAR_MAX, UCHAR_MAX);
    printf("`short`s go from %d to %d (unsigned, up to %u)\n", SHRT_MIN, SHRT_MAX, USHRT_MAX);
    printf("`int`s go from %d to %d (unsigned, up to %u)\n", INT_MIN, INT_MAX, UINT_MAX);
    printf("`long`s go from %ld to %ld (unsigned, up to %lu)\n", LONG_MIN, LONG_MAX, ULONG_MAX);
    printf("`float`s range from %e to %e\n", 0.0 - FLT_MAX, FLT_MAX);
    printf("`double`s range from %e to %e\n", 0.0 - DBL_MAX, DBL_MAX);
    return 0;
}
```

### Section 2.3 Constants

**重要细节**

### Section 2.4 Declarations

**重要细节**

### Section 2.5 Arithmetic Operators

**重要细节**

### Section 2.6 Relational and Logical Operators

**重要细节**

### Section 2.7 Type Conversions

**重要细节**

### Section 2.8 Increment and Decrement Operators

**重要细节**

### Section 2.9 Bitwise Operators

**重要细节**

### Section 2.10 Assignment Operators and Expressions

**重要细节**

### Section 2.11 Conditional Expressions

**重要细节**

### Section 2.12 Precedence and Order of Evaluation

**重要细节**

