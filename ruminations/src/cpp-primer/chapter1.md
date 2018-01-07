## Chapter 1. Getting started

### Exercise 1.1

> Review the documentation for your compiler and determine what file naming convention it uses. Compile and run the main program from page 2.

源程序`ex1_1.cpp`
```cpp
int main()
{
    return 0;
}
```

编译和运行
```bash
$ g++ -o ex1_1 ex1_1.cpp
$ ./ex1_1
```

### Exercise 1.2

> Exercise 1.2: Change the program to return -1. A return value of -1 is often treated as an indicator that the program failed. Recompile and rerun your program to see how your system treats a failure indicator from main.

源程序`ex1_2.cpp`
```cpp
int main()
{
    return -1;
}
```

编译和运行
```bash
$ g++ -o ex1_2 ex1_2.cpp
$ ./ex1_2
$ echo $?
255
```
为什么返回的是255呢，因为`exit`只接收0-255之间的整型返回值，返回值-1溢出为255。详见[Exit Codes With Special Meanings](http://www.tldp.org/LDP/abs/html/exitcodes.html)。

### Exercise 1.3
> Write a program to print Hello, World on the standard output.

源码`ex1_3.cpp`
```cpp
#include <iostream>

int main()
{
    std::cout << "Hello, World" << std::endl;
    return 0;
}
```

### Exercise 1.4
> Our program used the addition operator, +, to add two numbers. Write a program that uses the multiplication operator, \*, to print the product instead.

源码`ex1_4.cpp`
```cpp
#include <iostream>

int main()
{
    std::cout << "Enter two numbers:" << std::endl;
    int v1 = 0, v2 = 0;
    std::cin >> v1 >> v2;
    std::cout << "The product is " << v1 * v2 << std::endl;

    return 0;
}
```

### Exercise 1.5

> We wrote the output in one large statement. Rewrite the program to use a separate statement to print each operand.

源码`ex1_5.cpp`
```cpp
#include <iostream>

int main()
{
    std::cout << "Enter two numbers:" << std::endl;
    int v1 = 0, v2 = 0;
    std::cin >> v1 >> v2;
    std::cout << "The product of ";
    std::cout << v1;
    std::cout << " and ";
    std::cout << v2;
    std::cout << " is ";
    std::cout << v1 * v2;
    std::cout << std::endl;
    return 0;
}
```

### Exercise 1.6
> Explain whether the following program fragment is legal.
```cpp
std::cout << "The sum of " << v1;
          << " and " << v2;
          << " is " << v1 + v2 << std::endl;
```

程序非法

**[Error] expected primary-expression before '<<' token**

修改，删除前两行的分号
```cpp
std::cout << "The sum of " << v1 << " and " << v2 << " is " << v1 + v2 << std::endl;
```

### Exercise 1.7

> Compile a program that has incorrectly nested comments.

示例:
```cpp
/*
* comment pairs /* */ cannot nest.
* "cannot nest" is considered source code,
* as is the rest of the program
*/
int main()
{
    return 0;
}
```

编译报错
```bash
$ g++ ex1_7.cpp
ex1_7.cpp:2:23: 错误：‘cannot’不是一个类型名
 * comment pairs /* */ cannot nest.
                       ^
```

### Exercise 1.8

> Indicate which, if any, of the following output statements are legal:
```cpp
std::cout << "/*";
std::cout << "*/";
std::cout << /* "*/" */;
std::cout << /* "*/" /* "/*" */;
```
> After you’ve predicted what will happen, test your answers by compiling a
program with each of these statements. Correct any errors you encounter.

修正:
```cpp
std::cout << "/*";
std::cout << "*/";
std::cout << /* "*/" */";
std::cout << /* "*/" /* "/*" */;
```

### Exercise 1.9
> Write a program that uses a `while` to sum the numbers from 50 to 100.

源程序`ex1_9.cpp`
```cpp
#include <iostream>

int main()
{
    int sum = 0, curr = 50;
    while (curr != 101) sum += curr++;
    std::cout << "sum is: " << sum << std::endl;

    return 0;
}
```

### Exercise 1.10
> In addition to the `++` operator that add 1 to its operand, there is a decrement operator (`--`) that subtracts 1. Use the decrement operator to write a `while` that prints the numbers from ten down to zero.

源程序`ex1_10.cpp`
```cpp
#include <iostream>

int main()
{
    int val = 10;
    while (val >= 0)
        std::cout << val-- << std::endl;
    return 0;
}
```

### Exercise 1.11
> Write a program that prompts the user for two integers. Print each number in the range specified by those two integers.

源程序`ex1_11.cpp`
```cpp
#include <iostream>

int main()
{
    int small = 0, big = 0;
    std::cout << "please input two integers:\n";
    std::cin >> small >> big;
    for (int curr = small; curr != big; ++curr)
        std::cout << curr;

    return 0;
}
```

### Exercise 1.12
> What does the following for loop do? What is the final value of sum?
```cpp
int sum = 0;
for (int i = -100; i <= 100; ++i)
sum += i;
```

循环将-100到100求和，结果为0。

### Exercise 1.13
> Rewrite the Exercises 1.9-1.11 using for loops.

重写`ex1_9_for.cpp`
```cpp
#include <iostream>

int main()
{
    int sum = 0;
    for (int i = 50; i <= 100; ++i) sum += i;
    std::cout << "the sum is: " << sum << std::endl;

    return 0;
}
```

重写`ex1_10_for.cpp`
```cpp
#include <iostream>

int main()
{
    for (int i = 10; i >= 0; --i)
        std::cout << i << std::endl;
    return 0;
}
```

重写`ex1_11_for.cpp`
```cpp
#include <iostream>

int main()
{
    std::cout << "please input two integers:\n";
    int small = 0, big = 0;
    std::cin >> small >> big;

    for (int i = small; i != big; ++i)
        std::cout << i << std::endl;

    return 0;
}
```

### Exercise 1.14
> Compare and contrast the loops that used a for with those
using a while. Are there advantages or disadvantages to using either form?

参考[stackoverflow上的问答](http://stackoverflow.com/questions/2950931/for-vs-while-in-c-programming)。

### Exercise 1.15
> Write programs that contain the common errors discussed in
the box on page 16. Familiarize yourself with the messages the compiler
generates.

Stupid...

### Exercise 1.16
> Write your own version of a program that prints the sum of a set of integers read from `cin`.

源程序`ex1_16.cpp`
```cpp
#include <iostream>
int main()
{
    int sum = 0;
    for (int val; std::cin >> val; sum += val);
    std::cout << sum << std::endl;

    return 0;
}
```

### Exercise 1.17

> What happens in the program presented in this section if the input values are all equal? What if there are no duplicated values?

输入值相等，则输出这个值出现的次数。没有重复值时，没有输出，但会因为执行程序输入`Enter`而换行。

### Exercise 1.18

> Compile and run the program from this section giving it only equal values as input. Run it again giving it values in which no number is repeated.

Stupid...

### Exercise 1.19
> Revise the program you wrote for the Exercise 1.11 that printed a range of numbers so that it handles input in which the first number is smaller than the second.

源程序`ex1_19.cpp`(`std::swap()`交换两个变量的值)
```cpp
#include <iostream>

int main()
{
    int small = 0, big = 0;
    std::cout << "please input two integers:\n";
    std::cin >> small >> big;
    if (small > big)
        std::swap(small, big);

    for (int curr = small; curr != big; ++curr)
        std::cout << curr;

    return 0;
}
```

### Exercise 1.20
> [http://www.informit.com/title/032174113](http://www.informit.com/title/032174113) contains a copy of Sales_item.h in the Chapter 1 code directory. Copy that file to your working directory. Use it to write a program that reads a set of book sales transactions, writing each transaction to the standard output.

源码`ex1_20.cpp`
```cpp
#include <iostream>
#include "include/Sales_item.h"

int main()
{
    for (Sales_item item; std::cin >> item; std::cout << item << std::endl);
    return 0;
}
```

注意，使用`g++`编译时需要开启C++11特性
```bash
g++ -std=c++11 -o ex1_20 ex1_20.cpp
```

### Exercise 1.21
> Write a program that reads two Sales_item objects that have the same ISBN and produces their sum.

注意需要检查两个`Sales_item`对象是否具有相同的ISBN，源码`ex1_21.cpp`
```cpp
#include <iostream>
#include "include/Sales_item.h"

int main()
{
    Sales_item item1, item2;
    std::cin >> item1 >> item2;
    if (item1.isbn() == item2.isbn())
    {
        std::cout << item1 + item2 << std::endl;
        return 0;
    }
    else
    {
        std::cerr << "Data must refer to same ISBN." << std::endl;
        return -1;
    }
}
```

### Exercise 1.22
> Write a program that reads several transactions for the same ISBN. Write the sum of all the transactions that were read.

源码`ex1_22.cpp`
```cpp
#include <iostream>
#include "include/Sales_item.h"

int main()
{
    Sales_item total;
    if (std::cin >> total)
    {
        Sales_item trans;
        while (std::cin >> trans)
        {
            if (total.isbn() == trans.isbn())
                total += trans;
            else
            {
                std::cout << total << std::endl;
                total = trans;
            }
        }
        std::cout << total << std::endl;
    }
    else
    {
        std::cerr << "No data?!" << std::endl;
        return -1;
    }

    return 0;
}
```

输入文件`book.txt`
```
0-201-78345-X 3 20
0-201-78345-X 2 25
0-201-78346-X 1 100
0-201-78346-X 2 99.9
0-201-78346-X 6 89.9
```

编译和运行
```bash
$ g++ -std=c++11 -o ex1_22 ex1_22.cpp
$ ./ex1_22 <book.txt >result.txt
$ cat result.txt
0-201-78345-X 5 110 22
0-201-78346-X 9 839.2 93.2444
```

### Exercise 1.23
> Write a program that reads several transactions and counts
how many transactions occur for each ISBN.

源码`ex1_23.cpp`
```cpp
#include <iostream>
#include "include/Sales_item.h"

int main()
{
    Sales_item currItem, valItem;
    if (std::cin >> currItem)
    {
        int cnt = 1;
        while (std::cin >> valItem)
        {
            if (valItem.isbn() == currItem.isbn())
            {
                ++cnt;
            }
            else
            {
                std::cout << currItem << " occurs " << cnt << " times " << std::endl;
                currItem = valItem;
                cnt = 1;
            }
        }
        std::cout << currItem << " occurs "<< cnt << " times " << std::endl;
    }
    return 0;
}
```

### Exercise 1.24
> Test the previous program by giving multiple transactions
representing multiple ISBNs. The records for each ISBN should be grouped
together.

见上问

### Exercise 1.25
> Using the Sales_item.h header from the Web site,
compile and execute the bookstore program presented in this section.

同 Excercise 1.22。
