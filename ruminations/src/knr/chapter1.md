## Chapter 1 - A Tutorial Introduction

### Section 1.1 - Getting Started

**重要细节**：

1. 一个 C 程序，无论其大小如何，都是由 **函数** 和 **变量** 组成的;
2. **main函数** 比较特殊，程序总从 main 函数的开头开始执行，这意味着每一个程序都必须在某个地方具有 main 函数;
3. **C 本身没有提供输入/输出功能**，需要调用 **标准输入/输出库** 头文件 `stdio.h` 中的函数实现输入/输出;
4. 类似于 `\n` 的 **转义字符** 为表示无法输入的字符或不可见的字符提供了一种通用的可扩充的机制。

**练习题**:

> Exercise 1-1. Run the "hello, world" program on your system. Experiment with leaving out parts of the program, to see what error messages you get.

参考程序：

```cpp
#include <stdio.h>

int main(void)
{
	printf("hello, world\n");
	return 0;
}
```

**Remark**:

* 加入了 `return` 语句，因为 `main` 函数总是返回 `int` 型变量(告诉操作系统程序运行的状态)，参考：[Exit Codes With Special Meanings](http://www.tldp.org/LDP/abs/html/exitcodes.html)。显式地 return 是一种比较好的编码风格。
* 使用 gcc 编译文件，在不指定参数的情况下，会得到 `a.out` 可执行文件，输入 `./a.out` 运行程序，或者在 gcc 编译时用`-o`选项指定目标程序，编译完成后执行目标程序。

```bash
$ gcc helloworld.c
$ ./a.out
Hello,world!

$ gcc helloworld.c -o hello
$ ./hello
Hello,world!
```

> Exercise 1-2. Experiment to find out what happens when printf's argument string contains \c, where c is some character not listed above.

参考程序：

```cpp
#include <stdio.h>

int main(void)
{
	printf("响铃或视觉警告. \a\n");
	printf("换页. \f\n");
	printf("\r将光标移向行首.\n");
	printf("垂直制表符\v换行并缩进到上一行行尾后一个字符.\n");
	return 0;
}
```

**Remark**：

* `\v`的行为依赖于操作系统

### Section 1.2 - Variables and Arithmetic Expressions

**重要细节**：

1. C 的所有变量都必须先声明后使用；
1. 尽管 C 编译器并不关心程序的外观形式，但正确的缩进以及保留适当空格的程序设计风格对程序的易读性非常重要;
2. 建议每行只书写一条语句，并在运算符两边各加上一个空格字符，这样可以使得运算的结合关系更清楚明了;
3. 整型除法存在舍位截断;
3. 虽然 C 本身未定义标准输入/输出，但是 ANSI 标准定义了 `printf()` 等函数的行为；
4. 在格式化输出中，指明打印宽度可以实现右对齐，并且，指定的宽度是 **最小** 宽度;
5. 即使浮点数常量取的是整型值，在书写时最好还是为它加上一个显式的小数点，这样可以强调其浮点性质，便于阅读。

**不重要的细节**: 摄氏度和华氏度之间的转换关系  °C=(5/9)\*(°F-32)

**练习题**：

> Exercise 1-3. Modify the temperature conversion program to print a heading above the table.

参考程序：

```cpp
#include<stdio.h>

int main(void)
{
	float fahr, celsius;
	int lower, upper, step;

	lower = 0;
	upper = 300;
	step = 20;
	printf("%3c %6c\n",'F','C');
	fahr = lower;
	while(fahr <= upper) {
		celsius = (5.0 / 9.0) * (fahr - 32.0);
		printf("%3.0f %6.1f\n", fahr, celsius);
		fahr = fahr + step;
	}
	return 0;
}
```

> Exercise 1-4. Write a program to print the corresponding Celsius to Fahrenheit table.

参考程序：

```cpp
#include<stdio.h>

int main(void)
{
	float fahr, celsius;
	int lower, upper, step;

	lower = 0;
	upper = 300;
	step = 20;
	printf("%3c %6c\n",'C','F');
	celsius = lower;
	while(celsius <= upper) {
		fahr = (9.0 / 5.0) * celsius + 32.0;
		printf("%3.0f %6.1f\n", celsius, fahr);
		celsius = celsius + step;
	}
	return 0;
}
```

### Section 1.3 - The For Statement

**重要细节**：

1. 在允许使用某种类型变量值的代码上下文，都可以使用该类型的更复杂的表达式；
2. 选择 `while` 还是 `for`，判断标准是其是否能清晰地表达当前逻辑；
3. `for` 语句比较适合初始化和增加步长都是单条语句并且逻辑相关的情形，因为它将循环控制语句集中放在一起，且比`while`语句更紧凑。

**练习题**：

> Exercise 1-5. Modify the temperature conversion program to print the table in reverse order,that is, from 300 degrees to 0.

参考程序：

`for`版本：

```cpp
#include <stdio.h>

int main(void)
{
	float fahr, celsius;
	int lower, upper, step;

	lower = 0;
	upper = 300;
	step = 20;

	printf("%3c%6c",'C','F');
	for(celsius = upper; celsius >= lower; celsius -= step) {
		fahr = (9.0 / 5.0) * celsius + 32.0;
		printf("%3.0f%6.1f\n", celsius, fahr);
	}
	return 0;
}
```

`while`版本:

```cpp
#include <stdio.h>

int main(void)
{
	float fahr, celsius;
	int lower, upper, step;

	lower = 0;
	upper = 300;
	step = 20;

	printf("%3c%6c\n",'C','F');
	celsius = upper;
	while(celsius >= lower) {
		fahr = (9.0 / 5.0) * celsius + 32.0;
		printf("%3.0f %6.1f\n", celsius, fahr);
		celsius -= step;
	}

	return 0;
}
```

### Section 1.4 Symbolic Constants

**重要细节**：

1. 在程序中使用300、20等类似的 **幻数(magic numbers)** 并不是一个好习惯，它们几乎无法向以后阅读该程序的人提供什么信息，而且使程序的修改变得更加困难;
2. 符号常量名通常用 **大写** 字母拼写，这样可以很容易与用小写字母拼写的变量名相区别;
3. `#define` 指令行的末尾没有分号。

### Section 1.5 Character Input and Output

**重要细节**：

1. **文本流(text stream)** 是由多行字符构成的字符序列，每行字符由 0 个或更多字符组成，行末为换行符，标准库输入/输出库负责使输入/输出流都遵守这一模型，以保持一致性；
2. `EOF` 定义在 `stdio.h` 中。使用 `while (c != EOF)`时，需要将 `c` 声明为 `int` 类型的变量而不是 `char` 类型的，因为它必须足够大，除了能存储任何可能的字符外还要能存储文件结束符 `EOF`；
3. 赋值语句可以作为一个更大的表达式的一部分出现，赋值语句的值是赋值操作的左值；
4. `!=` 优先级高于 `=`；
5. 在兼有值与赋值两种功能的表达式中，赋值结合次序是由右至左，例如，`nl = nw = nc = 0;` 等效于 `nl = (nw = (nc = 0));`；
6. 逻辑运算的短路性：逻辑表达式从左至右求值，并保证在求值过程中只要能够判断最终的结果为真或假，求值就立即终止。

**不重要的细节**：

* “单词”定义：任何不包含空格、制表符或换行符的字符序列。

**练习题**：

> Exercsise 1-6. Verify that the expression getchar() != EOF is 0 or 1.

参考程序：

```cpp
#include<stdio.h>

int main(void)
{
	printf("Press a key. ENTER would be nice :-)\n\n");
	printf("The expression \"getchar() != EOF\" is: %d", getchar() != EOF);
	return 0;
}
```

Linux下使用 `Ctrl-D` 结束输入，当输入有效字符时，表达式值为1，否则为0.

> Exercise 1-7. Write a program to print the value of EOF.

参考程序：

```cpp
#include<stdio.h>

int main(void)
{
	printf("The value of EOF is %d\n\n", EOF);
	return 0;
}
```

Linux 下 `stdio.h` 中定义的 `EOF` 值为-1。

> Exercise 1-8. Write a program to count blanks, tabs, and newlines.

参考程序：

```cpp
#include<stdio.h>

int main(void)
{
    int blanks = 0, tabs = 0, newlines = 0;
    int c;
    int done = 0;
    int lastchar = 0;
    while(done == 0) {
        c = getchar();
        if(c == ' ') ++blanks;
        if(c == '\t') ++tabs;
        if(c == '\n') ++newlines;
        if(c == EOF) {
            if(lastchar != '\n') {
                ++newlines;
            }
            done = 1;
        }
        lastchar = c;
    }
    printf("\nBlanks:%d\nTabs:%d\nNewlines:%d\n", blanks, tabs, newlines);
    return 0;
}
```

在判断 `EOF` 时测试倒数第二个字符是为了处理某些不以换行符结束的情况。是否需要加入这一个扰动条件的处理，取决于对 **newlines** 的理解：理解为行数的话，就应该处理；反之，像中文版翻译的 “换行符个数”，则不用处理。

> Exercise 1-9. Write a program to copy its input to its output, replacing each string of one or more blanks by a single blank.

方法一：设置一个标志变量 `inspace` 来标志当前处理的字符是否为空格。

```cpp
#include <stdio.h>

int main(void)
{
    int c;
    int inspace = 0;

    while((c = getchar()) != EOF) {
        if(c == ' ') {
            if(inspace == 0) {
                inspace = 1;
                putchar(c);
            }
        }

        if(c != ' ') {
            inspace = 0;
            putchar(c);
        }
    }

  return 0;
}
```

方法二：记录之前的一个字符来判断是否输出当前空格。

```cpp
#include <stdio.h>

int main(void)
{
    int c, pc;

    pc = EOF;

    while ((c = getchar()) != EOF) {
        if (c == ' ')
            if (pc != ' ')
                putchar(c);

        if (c != ' ')
            putchar(c);
        pc = c;
    }

   return 0;
}
```

方法三：出现空格后，就把其后可能出现的空格全部跳过。注意为什么使用`break`那里还需要判定是否为`EOF`.

```cpp
#include<stdio.h>

int main(void)
{
	int c;

	while((c = getchar()) != EOF) {
		if(c==' ') {
			putchar(c);
			while((c=getchar())==' '&&c!=EOF)
			;
		}
		if(c==EOF)
			break;
		putchar(c);
	}
	return 0;
}
```

方法四：最简洁，思想也是记录前两个字符，程序紧凑的原因是使用逻辑运算符 `&&` 抽象了 `if` 分支。

```cpp
#include <stdio.h>

int main(void){
    int c, d;
    d = EOF;
    while ((c = getchar()) != EOF){
        if (!((d == ' ') && (c == ' ')))
            putchar(c);
        d = c;
    }
}
```

> Exercise 1-10. Write a program to copy its input to its output, replacing each tab by \t, each backspace by \b, and each backslash by \\. This makes tabs and backspaces visible in an unambiguous way.

方法一：变量`d`用来标志是否出现了需要处理的三种符号，如果出现则进行处理并将`d`置1。

```cpp
#include<stdio.h>

int main(void)
{
	int c,d;

	while((c = getchar()) != EOF) {
		d=0;
		if(c=='\\') {
			putchar('\\');
			putchar('\\');
			d=1;
		}
		if(c=='\t') {
			putchar('\\');
			putchar('t');
			d=1;
		}
		if(c=='\b') {
			putchar('\\');
			putchar('b');
			d=1;
		}
		if(d==0)
			putchar(c);
	}
	return 0;
}
```

方法二：定义一个符号常量`ESC_CHAR`来识别反斜杠。

```cpp
#include <stdio.h>

#define ESC_CHAR '\\'

int main(void)
{
	int c;

	while((c = getchar()) != EOF) {
    	switch(c) {
      		case '\b':
        		putchar(ESC_CHAR);
        		putchar('b');
        		break;
      		case '\t':
        		putchar(ESC_CHAR);
        		putchar('t');
        		break;
      		case ESC_CHAR:
        		putchar(ESC_CHAR);
        		putchar(ESC_CHAR);
        		break;
      		default:
        		putchar(c);
        		break;
    	}
  	}
  	return 0;
}
```

> Exercise 1-11. How would you test the word count program? What kinds of input are most likely to uncover bugs if there are any?

可以采用下面的测试用例(有点单元测试的思想)：

* 包含0个单词的输入文件
* 包含一个非常长的单词而不换行的输入文件
* 包含所有空白符(‘\f’,'\t','\v')而没有换行符的输入文件
* 包含66000个换行符的输入文件(注意`unsigned int`可以表示的整数范围)
* 在单词之间设置大量的空白符号序列
* 包含66000个只有一个字母的单词，每行66个
* 包含66000个单词，没有换行
* 采用`/usr/dict`目录下的文件作为输入(在ubuntu中为`/usr/share/dict/words`)
* 输入文件包含大量的长单词
* 将可执行文件(二进制)作为输入
* 将`dev/null`作为输入

生成测试用例的程序：

```cpp
#include <assert.h>
#include <stdio.h>

int main(void)
{
	FILE *f;
	unsigned long i;
	static char *ws = " \f\t\v";
	static char *al = "abcdefghijklmnopqrstuvwxyz";
	static char *i5 = "a b c d e f g h i j k l m "
					  "n o p q r s t u v w x y z "
					  "a b c d e f g h i j k l m "
					  "n o p q r s t u v w x y z "
					  "a b c d e f g h i j k l m "
					  "n\n";

	f = fopen("test0", "w");
	assert(f != NULL);
	fclose(f);

	f = fopen("test1", "w");
	assert(f != NULL);
	for (i = 0; i < ((66000ul / 26) + 1); i++)
		fputs(al, f);
	fclose(f);

	f = fopen("test2", "w");
	assert(f != NULL);
	for (i = 0; i < ((66000ul / 4) + 1); i++)
		fputs(ws, f);
	fclose(f);

	f = fopen("test3", "w");
	assert(f != NULL);
	for (i = 0; i < 66000; i++)
		fputc('\n', f);
	fclose(f);

	f = fopen("test4", "w");
	assert(f != NULL);
	fputs("word", f);
	for (i = 0; i < ((66000ul / 26) + 1); i++)
		fputs(ws, f);
	fputs("word", f);
	fclose(f);

	f = fopen("test5", "w");
	assert(f != NULL);
	for (i = 0; i < 1000; i++)
		fputs(i5, f);
	fclose(f);

	f = fopen("test6", "w");
	assert(f != NULL);
	for (i = 0; i < 66000; i++)
		fputs("word ", f);
	fclose(f);

	return 0;
}
```

> Exercise 1-12. Write a program that prints its input one word per line.

使用 `inspace` 变量标识当前字符是否在单词之间，在必要的时候换行。

```cpp
#include<stdio.h>

int main(void)
{
	int c;
	int inspace = 0;

	while((c=getchar()) != EOF) {
		if(c==' '||c=='\t'||c=='\n') {
			if(inspace==0) {
				inspace=1;
				putchar('\n');
			}
		}
		else {
			inspace=0;
			putchar(c);
		}
	}
	return 0;
}
```

### Section 1.6 Arrays

**重要细节**：

* 数组存在的合理性示例：在 `wc` 示例中，用数组来记录结果要比采用 10 个变量来记录 10 个数字要好；
* 数组下标可以是任何整型表达式，索引从0开始；
* `if (c >= '0' && c <= '9')` 用来测试 `c` 是否是一个数字，如果是，则其实际数值为 `c - '0'`；
* 在多分支甚至存在分支嵌套的情况下，严格使用缩进是比较好的编码风格。

> Exercise 1-13. Write a program to print a histogram of the lengths of words in its input. It is easy to draw the histogram with the bars horizontal; a vertical orientation is more challenging.

```cpp
#include<stdio.h>
#include<string.h>

#define MAXLEN 10

int main(void)
{
	int c;
	int inspace = 0;
	int firstletter = 1;
	int wordlen = 0;
	int maxval = 0;
	int thisval = 0;
	int thisindex;
	int lengtharr[MAXLEN + 1];
	int done = 0;

	memset(lengtharr, 0, sizeof(lengtharr));

	while(!done){
		c=getchar();
		if(c==' '||c=='\t'||c=='\n'||c==EOF){
			if(inspace == 0){
				firstletter = 0;
				inspace = 1;

				if(wordlen <= MAXLEN){
					if(wordlen > 0){
						thisval = ++lengtharr[wordlen - 1];
						if(thisval > maxval){
							maxval = thisval;
						}
					}
				}
				else{
					thisval = ++lengtharr[MAXLEN];
					if(thisval > maxval){
						maxval = thisval;
					}
				}
			}
			if(c == EOF){
				done = 1;
			}
		}
		else{
			if(inspace == 1 || firstletter == 1){
				wordlen = 0;
				firstletter = 0;
				inspace = 0;
			}
			++wordlen;
		}
	}

	for(thisval = maxval;thisval > 0;thisval--){
		printf("%4d|",thisval);
		for(thisindex = 0;thisindex <= MAXLEN;thisindex++){
			if(lengtharr[thisindex] >= thisval){
				printf("   *");
			}
			else{
				printf("    ");
			}
		}
		printf("\n");
	}
	printf("    +");
	for(thisindex = 0;thisindex <= MAXLEN;thisindex++){
		printf("----");
	}
	printf("\n     ");
	for(thisindex = 0;thisindex < MAXLEN;thisindex++){
		printf("%4d", thisindex + 1);
	}
	printf("  >%d\n", MAXLEN);
	return 0;
}
```

> Exercise 1-14. Write a program to print a histogram of the frequencies of different characters in its input.

并非所有字符都是可见的，采用其 ASCII 码作为字符标识符，是比较合理的方法。

```cpp
#include<stdio.h>
#include<string.h>

#define NUM_CHARS 256

int main(void)
{
	int c;
	long freqarr[NUM_CHARS + 1];		/* 记录统计信息 */

	long thisval = 0;
	long maxval = 0;
	int thisidx = 0;

	memeset(freqarr, 0, sizeof(freqarr));

	while((c = getchar()) != EOF){
		if(c < NUM_CHARS){
			thisval = ++freqarr[c];
			if(thisval > maxval){
				maxval = thisval;
			}
		}
		else{
			thisval = ++freqarr[NUM_CHARS];
			if(thisval > maxval){
				maxval = thisval;
			}
		}
	}

	for(thisval = maxval;thisval > 0;thisval--){
		printf("%4ld |",thisval);
		for(thisidx = 0;thisidx < NUM_CHARS;thisidx++){
			if(freqarr[thisidx] >= thisval){
				printf("*");
			}
			else if(freqarr[thisidx] > 0){
				printf(" ");
			}
		}
		printf("\n");
	}
	printf("     +");
	for(thisidx = 0;thisidx <= NUM_CHARS;thisidx++){
		if(freqarr[thisidx] > 0){
			printf("-");
		}
	}
	printf("\n      ");

	for(thisidx = 0;thisidx < NUM_CHARS;thisidx++){
		if(freqarr[thisidx] > 0){
			printf("%d",thisidx/100);
		}
	}
	printf("\n      ");
	for(thisidx = 0;thisidx < NUM_CHARS;thisidx++){
		if(freqarr[thisidx] > 0){
			printf("%d", (thisidx - (100 * (thisidx / 100))) / 10);
		}
	}
	printf("\n      ");
	for(thisidx = 0;thisidx < NUM_CHARS;thisidx++){
		if(freqarr[thisidx] > 0){
			printf("%d", thisidx - (10 * (thisidx / 10)));
		}
	}

	if(freqarr[NUM_CHARS] > 0){
		printf(">%d\n", NUM_CHARS);
	}
	printf("\n");
	return 0;
}
```

### Section 1.7 Functions

**重要细节**

* **函数** 提供了封装运算操作的方法，使用函数时不用考虑它是如何实现的。

> With properly designed functions, it is possible to ignore **how** a job is done; knowing  **what** is done is sufficient.

* 合理使用函数，可使代码更清晰易读；
* 函数参数名字仅函数内部有效，不会与其它函数的参数名字冲突；
* **形式参数**：函数定义中圆括号内列表中出现的变量；
* **实际参数**: 函数调用中与形式参数对应的值；
* 函数采用 `return expression;` 来返回值给调用者，`expression`可以省略，此时`return;`只起控制作用，不返回任何值；
* **函数原型(function prototype)** 需要和定义以及调用相匹配，但参数名字并不需要匹配，并且在函数原型中可以省略；
* 合适的参数名能够起到很好的说明性作用，因此我们在函数原型中总是指明参数名。

> Exercise 1-15. Rewrite the temperature conversion program of Section 1.2 to use a function for conversion.

```cpp
#include<stdio.h>

float FtoC(float f)
{
	float c;
	c = (5.0 / 9.0) * (f - 32.0);
	return c;
}

int main(void)
{
	float fahr, celsius;
	int lower, upper, step;

	lower = 0;
	upper = 300;
	step = 20;

	printf("F    C\n\n");
	fahr = lower;
	while(fahr <= upper)
	{
		celsius = FtoC(fahr);
		printf("%3.0f %6.1f\n", fahr, celsius);
		fahr = fahr + step;
	}
	return 0;
}
```

### Section 1.8 Arguments - Call by Value

**重要细节**:

* C 的所有函数参数都通过 **值传递(passed by value)**，这意味着被调用的函数接收了存在临时变量中的参数值而不是原始变量；

> It usually leads to more compact programs with fewer extraneous variables,because parameters can be treated as conveniently initialized local variables in the called routine.

* 必要的时候也需要在调用过程中修改一个变量的值，这时调用函数需要提供目标变量的 **地址(address)**(**指针(pointer)**)，并且调用函数必须将参数声明为指针类型，然后间接地通过这个指针来访问变量；
* 数组名字用作参数时，传递给函数的值是 **数组起始元素的地址**，而不会另外创建数组的拷贝。

### Section 1.9 Character Arrays

C程序中出现类似于 `"hello\n"` 的字符串常量时，以字符数组的形式存储，数组的元素分别存储各个字符并以 `\0` 标志字符串的结束。

> Exercise 1-16. Revise the main routine of the longest-line program so it will correctly print the length of arbitrary long input lines, and as much as possible of the text.

修改 `getline()` 函数，使之返回文本行的实际长度而不是写入数组的字符个数。`getline_1()` 的命名方式可以避免编译器报错。程序每读入一行，就输出当前行的长度及字符串，在输入结束以后，输出最长行及其长度。

```cpp
#include <stdio.h>

#define MAXLINE 1000 /* maximum input line size */

int getline_1(char line[], int maxline);
void copy(char to[], char from[]);

/* print longest input line */
int main(void)
{
	int len; /* current line length */
	int max; /* maximum length seen so far */
	char line[MAXLINE];	/* current input line */
	char longest[MAXLINE]; /* longest line saved here */

	max = 0;

	while((len = getline_1(line, MAXLINE)) > 0)
	{
		printf("%d: %s", len, line);

		if(len > max)
		{
			max = len;
			copy(longest, line);
		}
	}
	if(max > 0)
	{
		printf("Longest is %d characters:\n%s", max, longest);
	}
	printf("\n");
	return 0;
}

/* getline_1: read a line into s, return length */
int getline_1(char s[], int lim)
{
	int c, i, j;

	for(i = 0, j = 0; (c = getchar())!=EOF && c != '\n'; ++i)
	{
		if(i < lim - 1)
		{
			s[j++] = c;
		}
	}
	if(c == '\n')
	{
		if(i <= lim - 1)
		{
			s[j++] = c;
		}
		++i;
	}
	s[j] = '\0';
	return i;
}

/* copy: copy 'from' into 'to'; assume 'to' is big enough */
void copy(char to[], char from[])
{
	int i;

	i = 0;
	while((to[i] = from[i]) != '\0')
	{
		++i;
	}
}
```

> Exercise 1-17. Write a program to print all input lines that are longer than 80 characters.

需要注意边界情况，输出长度大于 80 的字符串，设置符号常量 `MINLENGTH` 为 81，当输入字符串包括 80 个有效字符加一个换行符的边界情况时，`readbuff()`会在遇到换行符时返回0，这样 `main()` 不会判定为满足长度条件。程序的思想是先调用 `readbuff()` 尝试读取字符串，如果读到81个有效字符而没有遇到EOF或是 `\n` 时，继续调用 `copyline()` 来输出之前保存在 `buffer[]` 中的字符以及剩余的字符。

```cpp
#include <stdio.h>

#define MINLENGTH 81

char buffer[MINLENGTH];

int readbuff(char *buffer);
int copyline(char *buffer);

int main(void)
{
	int status = 0;
	while(status != -1){
		status = readbuff(buffer);
		if(status == 1){
			status = copyline(buffer);
		}
	}
	return 0;
}

int readbuff(char *buffer)
{
	size_t i = 0;
	int c;

	while(i < MINLENGTH){
		c = getchar();
		if(c == EOF) return -1;
		if(c == '\n') return 0;
		buffer[i++] = c;
	}
	return 1;
}

int copyline(char *buffer)
{
	size_t i;
	int c;
	int status = 1;

	for(i = 0;i < MINLENGTH;i++)
		putchar(buffer[i]);
	while(status ==1){
		c = getchar();
		if(c == EOF)
			status = -1;
		else if(c == '\n')
			status = 0;
		else
			putchar(c);
	}
	putchar('\n');
	return status;
}
```

> Exercise 1-18. Write a program to remove trailing blanks and tabs from each line of input, and to delete entirely blank lines.

```cpp
#include <stdio.h>
#define MAXLINE 1000

int mygetline(char line[], int max);
int format(char line[], int len);

int main(void)
{
    int len = 0;
    int newlen = 0;
    char line[MAXLINE];

    while((len = mygetline(line, MAXLINE)) > 1 ) {
        newlen = format(line, len);
        printf("Length before and after formatting: %d-%d, \n [%s]\n", len, newlen, line);
    }
}


int mygetline(char line[], int max)
{
    int i = 0;
    char c;
    for (i; i<max && ((c=getchar()) != '\n' && c != EOF); i++) {
        line[i] = c;
    }
    line[i++] = '\0';
    return i;
}


int format(char line[], int len)
{
    int i = len-1;
    for(i; i >=0 && (line[i]=='\0' || line[i]==' ' || line[i]=='\t'); i--)
        ;
    if (i < 1)
        i = 0;
    line[++i] = '\0';
    return i;
}
```

> Exercise 1-19. Write a function `reverse(s)` that reverses the character string `s`. Use it to write a program that reverses its input a line at a time.

```cpp
#include <stdio.h>

#define MAX_LINE 1024

int reverse(char s[]);
int getaline(char s[],int lim);

int main(void)
{
	char line[MAX_LINE];

	while(getaline(line,MAX_LINE)>0)
	{
		reverse(line);
		printf("%s",line);
	}
	return 0;
}

int reverse(char s[])
{
	char ch;
	int i,j;

	for(j=0; s[j] != '\n'; j++)
		;
	--j;
	for(i = 0; i < j; i++){
		ch = s[i];
		s[i] = s[j];
		s[j] = ch;
		--j;
	}
	return 0;
}

int getaline(char s[], int lim)
{
	int c,i;
	for(i=0; i < lim - 1 && (c = getchar()) != EOF && c != '\n'; ++i)
		s[i] = c;
	if(c =='\n'){
		s[i] = c;
		++i;
	}
	s[i] = '\0';
	return i;
}
```

### Section 1.10 External Variables and Scope

**重要细节**:

* **局部变量/自动变量** 只在函数被调用时存在，函数执行完毕退出时消失；
* 函数的两次调用之间，局部变量不保留前次调用时的赋值；
* **全局变量/外部变量** 在所有的函数中都可以通过变量名访问，定义在所有函数之外，且只能定义一次；
* 每个需要访问外部变量的函数中，必须声明（`extern`显式声明，或者上下文隐式声明）相应的外部变量，并说明其类型；
* 通常把变量和函数的 `extern` 声明放在一个单独的文件中（头文件），并在源文件开头包含必要的头文件。

> In fact, common practice is to place definitions of all external variables at the beginning of the source file, and then omit all extern declarations.

* 过分依赖外部变量实际上 **并不好**(虽然看起来这样可以简化函数之间的通信，参数列表可以变短并且变量访问更容易)

> But external variables are always there even when you don't want them. Relying too heavily on external variables is fraught with peril since it leads to programs whose data connections are not all obvious - variables can be changed in unexpected and even inadvertent ways, and the program is hard to modify.

* **定义** 表示创建变量或分配存储单元，**声明** 只说明变量的性质，不分配存储单元

**轶闻**：[有着 1 万个全局变量的一大坨代码](http://blog.jobbole.com/100881/)

> Exercise 1-20. Write a program __detab__ that replaces tabs in the input with the proper number of blanks to space to the next tab stop. Assume a fixed set of tab stops, say every n columns. Should n be a variable or a symbolic parameter?

```cpp
#include <stdio.h>
#define MAXLINE 1000
#define COLUMNS 4

int mygetline(char line[], int max);
void detab(char buf[], char line[], int cols);

int main(void)
{
    int len = 0;
    char buffer[MAXLINE];
    char line[MAXLINE];

    while ((len = mygetline(buffer, MAXLINE)) > 1 ) {
        detab(buffer, line, COLUMNS);
        printf("%s\n", line);
    }

}

int mygetline(char buf[], int max)
{
    char c;
    int i = 0;
    for (i; i<max && ((c=getchar()) != EOF && c != '\n'); i++) {
        buf[i] = c;
    }
    buf[i] = '\0';
    return i;
}

void detab(char buf[], char line[], int cols)
{
    int i, j, k;
    i = j = k = 0;
    char c;
    char space = ' ';

    for (i; k<MAXLINE && (c=buf[i]) != '\0'; i++) {
        if (c == '\t') {
            for (j=0; j<cols; j++) {
                line[k++] = space;
            }
        }
        else
            line[k++] = c;
    }
    line[k] = '\0';
}
```

> Exercise 1-21. Write a program entab that replaces strings of blanks by the minimum number of tabs and blanks to achieve the same spacing. Use the same tab stops as for detab. When either a tab or a single blank would suffice to reach a tab stop, which should be given preference?

不太清楚最后一句话是什么意思，程序设定为需要达到4个连续SPACE时才用TAB替换，否则保留SPACE。

```cpp
#include <stdio.h>

#define MAXLEN 1000
#define TABLEN 4
#define TAB '\t'
#define SPACE ' '

int mygetline(char line[], int max);
void entab(char buffer[], char line[]);

int main(void)
{
    int len = 0;
    char buffer[MAXLEN];
    char line[MAXLEN];

    while ( (len = mygetline(buffer, MAXLEN)) > 1) {
        entab(buffer, line);
        printf("%s\n", line);
    }
}

int mygetline(char line[], int max)
{
    char c;
    int i = 0;
    for (i; ((c = getchar()) != EOF) && c != '\n'; i++) {
        line[i] = c;
    }
    line[++i] = '\0';
    return i;
}

void entab(char buffer[], char line[])
{
    char c;
    int count, i, j, k;
    count = i = j = k = 0;
    char tabbuf[5];

    for (i; buffer[i] != '\0'; i++) {
        if (count == TABLEN) {
            line[k++] = TAB;
            count = 0;
        }

        if (buffer[i] == SPACE) {
            tabbuf[count++] = buffer[i];	// push SPACEs into buffer
        }
        else {
            for (j = 0; j<count; j++) {		// release SPACEs from buffer
                line[k++] = tabbuf[j];
            }
            count = 0;
            line[k++] = buffer[i];
        }
    }
    line[k] = '\0';
}
```

> Exercise 1-22. Write a program to ``fold'' long input lines into two or more shorter lines after the last non-blank character that occurs before the n-th column of input. Make sure your program does something intelligent with very long lines, and if there are no blanks or tabs before the specified column.

**last non-blank character that occurs before the n-th column of input** 的理解是从给定长度开始往后遍历直到遇到SPACE或者TAB，如果没有找到，则往后找到第一个SPACE或者TAB为止，总之原则是不会把一个单词打断。

```cpp
#include<stdio.h>
#include<string.h>

// max length of getline function
#define MAXLINE 10000
// threshold of line length
#define LIMIT 20

unsigned int mygetline(char s[], unsigned int lim);
int cut(char s[], unsigned int start);

int main(void)
{
    unsigned int length;
    char string[MAXLINE];

    while ((length = mygetline(string, MAXLINE)) > 0) {
        if (length > LIMIT) {
            cut(string, 0);
            printf("%s",string);
        }
        else
            printf("%s",string);
    }
    return 0;
}

int cut(char s[], unsigned int start)
{
    unsigned int i;

    for(i = start + LIMIT; i > start && s[i] != ' ' && s[i] != '\t'; --i);
    printf("%d\n", i);

    if (i == start) {
        for(i = start; s[i] != ' ' && s[i] != '\t' && s[i] != '\n'; ++i);
        s[i] = '\n';
    }

    if ((strlen(s) - i) <= LIMIT) {
        s[i] = '\n';
    }
    else if (i > start && i != start) {
        s[i] = '\n';
        cut(s, i);
    }
    return 0;
}

unsigned int mygetline(char s[], unsigned int lim)
{
    int c;
    unsigned int i;
    for (i=0; i<lim-1 && (c=getchar())!=EOF && c!='\n'; ++i)
        s[i] = c;
    if (c == '\n')
        s[i++] = c;
    s[i] = '\0';
    return i;
}
```

> Exercise 1-23. Write a program to remove all comments from a C program. Don't forget to handle quoted strings and character constants properly. **C comments don't nest**.

设置一个状态机来处理读入的字符。

贴出 Thomas van der Burgt 的代码。可以使用源代码本身来验证，将代码存成`main.cpp`，编译并调用：

```bash
$ gcc main.cpp -o main
$ ./main < main.cpp
```

```cpp
/*
 * Filename:    rmcomments.c
 * Author:      Thomas van der Burgt <thomas@thvdburgt.nl>
 * Date:        27-FEB-2010
 *
 * The C Programming Language, second edition,
 * by Brian Kernighan and Dennis Ritchie
 *
 * Exercise 1-23, page 34
 *
 * Write a program to remove all comments from a C program. Don't forget
 * to handle quoted strings and character constants properly. C comments
 * do not nest.
 */

#include <stdio.h>
#include <stdlib.h>

#define PROGRAM 0
#define COMMENT 1
#define QUOTE   2
#define SLASH   3
#define STAR    4
#define LITERAL 5

int main(void)
{
    int c, state;
    char quote;

    state = PROGRAM;
    while ((c = getchar()) != EOF) {
        if (state == PROGRAM) {
            /* Within the program code. */
            if (c == '/')
                state = SLASH;
            else {
                if (c == '"' || c == '\'') {
                    /* Start of a quote of character constant */
                    state = QUOTE;
                    quote = c;
                }
                putchar(c);
            }
        } else if (state == COMMENT) {
            /* Within a comment. */
            if (c == '*')
                state = STAR;
        } else if (state == QUOTE) {
            /* Within a quote. */
            if (c == '\\')
                state = LITERAL;
            else if (c == quote)
                state = PROGRAM;
            putchar(c);
        } else if (state == SLASH) {
            /* Following a slash (/). */
            if (c == '*')
                state = COMMENT;
            else if (c == '"' || c == '\'') {
                /* Start of a quote of character constant */
                state = QUOTE;
                quote = c;
            } else {
                state = PROGRAM;
                putchar('/');
                putchar(c);
            }
        } else if (state == STAR) {
            if (c == '/')
                state = PROGRAM;
            else if (state != '*')
                state = COMMENT;
        } else if (state == LITERAL) {
            /* Within quoted string or char constant, following \.*/
            putchar(c);
            state = QUOTE;
        }
    }
    return EXIT_SUCCESS;
}
```

> Exercise 1-24. Write a program to check a C program for rudimentary syntax errors like unmatched parentheses, brackets and braces. Don't forget about quotes, both single and double, escape sequences, and comments. (This program is hard if you do it in full generality.)

贴代码。。。

```cpp
/* This is my first rudimentary C syntax checker. It checks for syntax errors,
 * like closing a set of brackets using the wrong type. It is not *very* good
 * at it, but it does not bother about comments, and it does know something
 * about escape sequences and character strings/constants.
 *
 * It uses a simple static stack to keep track of the braces, and it also uses
 * a stack to keep track of the errors on each line. Someday I might change
 * that to use a queue for the error-tracking, because as it is now, it outputs
 * the rightmost error on the line first, and then it steps leftwards (if there
 * is more than one error on each line).
 *
 * I might also implement my dynamically allocated stack and queue implementa-
 * tions, so that running out of space in the stack is not an issue. I might
 * also skip it, since it has little to do with the exercise in question.
 *
 * The program is especially bad at error-recovery. If it finds an error, (or
 * something it believes to be an error) subsequent errors reported might be a
 * bit dubious.
 */

#include <stdio.h>

#define MAXVAL 1000
#define MAXLINE 1000

typedef struct {
    int top;
    int val[MAXVAL];
    int pos[MAXVAL];
} stackstr;

/* very simple stack push function */
int push(stackstr *stk, int foo, int bar)
{
    if (stk->top == MAXVAL) {
        printf("stack overflow. NOT putting more values on the stack.\n");
        return 1;
    }
    stk->val[stk->top] = foo;
    stk->pos[stk->top] = bar;
    stk->top++;

    return 0;
}

/* very simple function to pop values off a stack */
int pop(stackstr *stk, int *foo, int *bar)
{
    if (stk->top == 0) {
        return 1;
    }
    stk->top--;
    *foo = stk->val[stk->top];
    *bar = stk->pos[stk->top];

    return 0;
}

/* we go through the input one line at a time, and this function
 * gets the line to test
 */
int getline(char *s, int lim)
{
    int i, c;

    for (i = 0; i < lim - 1 && (c = getchar()) != EOF && c != '\n'; i++)
        *(s + i) = c;

    if (c == '\n')
        *(s + i++) = c;
    *(s + i) = '\0';

    return i;
}

void scanline(stackstr *stk, stackstr *errstk, char *s, int len)
{
    int i, c, d, foo;
    static int string = 0, comment = 0, isconst = 0, escape = 0;

    for (i = 0; i < len; i++) {
        c = *(s + i);

        if (!comment) {
            if (c == '\\') { /* we have an escape */
                /* test for a valid escape sequence */
                if ((d = *(s + ++i)) == '\\' || d == 'n' || d == '0' || d == 'r' || d == '?'
                        || d == 't' || d == '\'' || d == '\"' || d == 'b' || d == 'x') {
                    continue; /* ok, valid escape sequence -- don't bother about it */
                } else {
                    push(errstk, 5, i); /* illigal escape sequence */
                }
            } else if (c == '\"') { /* is it a text string then? */
                if (!string)
                    string = 1;
                else
                    string = 0;
            } else if (c == '\'') { /* is it a constant? */
                if (!isconst)
                    isconst = 1;
                else
                    isconst = 0;
            }
        }

        if (!isconst && !string && !comment && c == '/') {
            if ((d = *(s + ++i)) == '*')
                comment = 1;
        } else if (comment && c == '*') {
            if ((d = *(s + ++i)) == '/') {
                comment = 0;
                continue; /* done with the comment stuff -- start over */
            }
        }

        /* only bother about ({[ ]})'s that's not in
         * a string, constant or comment
         */
        if (!isconst && !string && !comment) {
            if (c == '(' || c == '{' || c == '[') {
                push(stk, c, 0);
            } else if (c == ']' || c == '}' || c == ')') {
                if (pop(stk, &d, &foo)) {
                    push(errstk, 4, i);
                }
                if (c == ')' && d != '(') {
                    push(stk, d, 0);
                    push(errstk, 1, i);
                } else if (c == ']' && d != '[') {
                    push(stk, d, 0);
                    push(errstk, 2, i);
                } else if (c == '}' && d != '{') {
                    push(stk, d, 0);
                    push(errstk, 3, i);
                }
            }
        }
    }
}


/* print errors on the line (if there were any) */
void print_err(stackstr *errstk, int lineno)
{
    int errno, pos;

    /* yes I know... this way the errors come "backwards" :) */
    while (!pop(errstk, &errno, &pos)) {
        printf("on line number %d: ", lineno);
        switch(errno) {
            case 1:
                printf("closing unopened parantheses, column %d\n", pos+1);
                break;
            case 2:
                printf("closing unopened square bracket, column %d\n", pos+1);
                break;
            case 3:
                printf("closing unopened curly braces, column %d\n", pos+1);
                break;
            case 4:
                printf("trying to close unopened block/control structure, column %d\n", pos+1);
                break;
            case 5:
                printf("illigal escape sequence, column %d\n", pos+1);
                break;
            default:
                printf("undeterminable error\n");
                break;
        }
    }
}

int main(void)
{
    stackstr errstk = {0}, stk = {0};
    int c, linenbr = 0, errcount = 0, linelen;
    char line[MAXLINE];

    while ((linelen = getline(line, MAXLINE)) > 0) {
        linenbr++;
        scanline(&stk, &errstk, line, linelen);
        if (errstk.top) {
            print_err(&errstk, linenbr);
            errcount++;
        }
    }

    if (errcount)
        printf("%d lines contained error(s)\n", errcount);
    else
        printf("Well, *I* didn't find any syntax errors, but don't take my word for it...:)\n");

    return 0;
}
```