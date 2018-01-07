---
layout: post
title: 'Github Pages 更新到 Jekyll 3.0'
modified: 2016-02-25
feature: octodex.jpg
description: Github Pages 使用的 Jekyll 版本号终于进入 3.0 时代了！本文介绍新的特性及需要注意的事项。
tags: [Valyria Steel]
---

2016年2月2号，Github Pages 的一篇 Blog : [GitHub Pages now faster and simpler with Jekyll 3.0](https://github.com/blog/2100-github-pages-now-faster-and-simpler-with-jekyll-3-0) 宣布 Github Pages 使用的 Jekyll 版本号进入 3.0 时代，带来的影响比较大的变化包括：

* 将只支持 kramdown 作为 Markdown 引擎
* 将仅支持 Rouge 进行代码高亮
* 大幅提升构建速度
* 不再支持相对 Permalinks 以及 Textile

这可能会导致之前使用 Pygments 进行代码高亮的托管在 Github Pages 上的网页的代码高亮出现问题，以及一些其他的问题。这次升级调整，是上游的 Jekyll 演进的自然结果。这里主要记录一下升级到 Jekyll 3.0+ (目前的最新版本为 3.1.2) 后做的一些调整。

## 配置文件
首先是 Jekyll 的配置文件 `_config.yml`，`markdown` 选项强制使用 `kramdown`，另外，之前的 `highlighter` 和 `syntax_highlighter` 都必须修改为 `rouge`。

```
highlighter: rouge
markdown: kramdown
kramdown:
  input: GFM
  syntax_highlighter: rouge
```

实际上 Github Pages 固定了一些用户不能修改的配置，具体可以参考 [Configuring Jekyll](https://help.github.com/articles/configuring-jekyll/)。

## Rouge 高亮
首先需要说明的是，Liquid 语法的高亮代码块今后最好不要再用了，使用 Rouge 将直接支持 Backtick 风格的代码块，这无疑优化了 Markdown 书写的体验。关于 Backtick 风格的代码块，参考：[Creating and highlighting code blocks](https://help.github.com/articles/creating-and-highlighting-code-blocks/)。

在本地使用 gem 安装 `rouge` 后，附带的 `rougify` 工具可以用来生成多种高亮主题的CSS文件，首先安装 `rouge`：

```bash
$ gem install rouge
```

然后使用

```bash
$ rougify help style

usage: rougify style [<theme-name>] [<options>]

Print CSS styles for the given theme.  Extra options are
passed to the theme.  Theme defaults to thankful_eyes.

options:
  --scope       (default: .highlight) a css selector to scope by

available themes:
  base16, base16.dark, base16.monokai, base16.monokai.light, base16.solarized, base16.solarized.dark, colorful, github, molokai, monokai, monokai.sublime, thankful_eyes
```

可以查看目前可用的高亮主题，例如对于我最喜爱的 monokai.sublime 主题，使用

```bash
$ rougify style monokai.sublime > assets/css/syntax.css
```

即可生成一个CSS文件，将这个CSS文件放到html中，即可实现对代码块的高亮。

```html
<link href="/assets/css/syntax.css" rel="stylesheet">
```

这样的方式还是比较直观的，但是可能会存在一个坑，先看看 Rouge 对 Backtick 代码块生成的 html 代码

```html
<div class="highlighter-rouge">
    <pre class="highlight">
        <code>
            ...
        </code>
    </pre>
</div>
```

可见 Rouge 应用了一个 `highlighter-rouge` 类的 `<div></div>` 以及 `highlight` 类的 `<pre></pre>`，再看看 rougify 之前生成的 CSS 文件的头部

```css
.highlight table td { padding: 5px; }
.highlight table pre { margin: 0; }
.highlight .gh {
  color: #999999;
}
...
```

并没有对 `highlighter-rouge` 类的 `<div></div>` 或是 `highlight` 类的 `<pre></pre>` 进行样式说明，这直接可能导致代码块的 `background-color` 属性被覆盖（如 Bootstrap），若是恰好被覆盖为浅色背景，对于 monokai 这样的前景色为浅色的高亮主题，可能会导致代码块看不清楚，就像下面这个样子

![light-bg]({{ site.qnurl }}/media/upgrade-jekyll/light-bg.png){:.img-responsive}

坑爹啊！要修复这个问题，需要对之前生成的 `syntax.css` 做一点小改动，加入一行

```css
pre[class='highlight'] {background-color:#000000;}
```

这样来设置 `highlight` 类的 `<pre></pre>` 标签的背景为黑色。

## 语法进化
要让之前使用 Liquid 语法的代码块正常亮起来，需要把所有的 `highlight` Liquid 标签替换为 Backtick 风格。这类机械化的工作当然需要交给一个脚本来处理，下面放一个 Python 脚本以供参考。

{% raw %}
```python

#!/usr/bin/env python
# encoding: utf-8

import sys

def helpfunc():
    print('A Python Script which can convert liquid highlight tags to backtick-style fenced code blocks.\n')
    print('Usage:\n')
    print('  python tobacktick.py <inputfile> [outputfile]\n')


def main():
    if len(sys.argv) < 2 or sys.argv[1]=='help':
        helpfunc()
        return

    input_fn = sys.argv[1]
    if len(sys.argv) < 3:
        output_fn = input_fn.split('.')[0]+'-converted.'+input_fn.split('.')[1]
    else:
        output_fn = sys.argv[2]

    with open(input_fn, 'r') as inputfile, open(output_fn, 'w') as outputfile:
        for line in inputfile:
            judge_condition = line.split()
            if len(judge_condition) > 1 and judge_condition[0] == r'{%':
                if judge_condition[1] == r'highlight':
                    identifier = judge_condition[2]
                    outputfile.write('\n```'+identifier+'\n')
                elif judge_condition[1] == r'endhighlight':
                    outputfile.write('```\n')
            else:
                outputfile.write(line)

        print('Complete! Saved to:' + output_fn)


if __name__ == '__main__':
    main()
```
{% endraw %}

脚本会根据输入的 `*.md` 文件中的代码高亮 Liquid 标签信息，自动替换为 Backtick 风格的代码块，加上 `converted` 后缀输出到输入文件的目录中（通常是 `_posts`），使用输出文件替换掉原来的 `*.md` 文件即可。

## 拥抱变化
作为开发者级别的用户，遭遇到自己使用的产品进行重要更新，几乎是不可避免的事情。我们当然不能立即破口大骂，讲道理的话，就这次 Github Pages 的更新来说，确实优化了 Markdown 的书写体验，使用 Backtick 风格的代码块，确实比生硬地引入 Liquid 标签要优雅多了。开发者的基本素养至少应该包括：

* 能够心怀喜悦地观赏 Changlog
* 能够心态平和地 RTFM 以及 RTFS

倘若觉得功能升级不能理解了，大概需要先思考一下，自己是不是疏忽了更先进的思维方式。
