---
title: Python原生爬虫
date: 2022-09-03 22:37:38
tags: 
  -Python
  -爬虫
categories: 爬虫

---

# 爬虫前奏

明确目的：爬取虎牙直播LOL板块主播人气排行

找到数据对应的网页

分析网页的结构找到数据所在的标签位置

模拟HTTP请求，向服务器发送这个请求，获取到服务器返回给我们的HTML

用正则表达式提取我们要的数据（名字，人气）

# 初始化获取html的类和方法

```python
# 导入获取html的库
from urllib import request

class Spider():
    url = 'https://www.huya.com/g/lol'

    # 私有方法，获取网页的内容
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()

    # Spider的入口方法
    def go(self):
        self.__fetch_content()

spider = Spider()
spider.go()
```

# vscode断点调试

如果Python和Pylance插件版本太高，断点可能会停不下来。

解决方案，Python退回到2020.9月版本，Pylance退回到2020.9.5版本

## 快捷键

启动调试：F5

单步调试：F10

从一个断点跳到下一个断点：F5

进入某个函数或者对象的内部：F11

# 编码转换

将字节码转换为字符串

```python
# 导入获取html的库
from urllib import request

class Spider():
    url = 'https://www.huya.com/g/lol'

    # 私有方法，获取网页的内容
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        # bytes
        htmls = r.read()
        # 将字节码转换为字符串
        htmls = str(htmls, encoding='utf-8')
        # 断点
        a = 1

    # Spider的入口方法
    def go(self):
        self.__fetch_content()

spider = Spider()
spider.go()
```

# 分析爬到的内容

## 寻找合适的定位标签

找离需要爬取的数据最近的一个标签，并且标签要具有唯一性

标签最好是选择能够闭合的标签(父级标签)

逐级精确定位，三层结构：

![image-20220904115855637](https://typora1321.oss-cn-beijing.aliyuncs.com/image-20220904115855637.png)

![image-20220904115030241](https://typora1321.oss-cn-beijing.aliyuncs.com/image-20220904115030241.png)

## 编写正则表达式

### 根正则表达式

```python
root_pattern = '<li class="game-live-item" data-gid=([\s\S]*?)</li>'
```

分析成功：

<img src="https://typora1321.oss-cn-beijing.aliyuncs.com/image-20220904121104213.png" alt="image-20220904121104213" style="zoom: 67%;" />

### 姓名和人数的正则表达式

```python
name_pattern = '<i class="nick" title="([\s\S]*?)">'
number_pattern = '<i class="js-num">([\s\S]*?)</i>'
```

```python
import re
# 导入获取html的库
from urllib import request

class Spider():
    url = 'https://www.huya.com/g/lol'
    # 根正则表达式
    root_pattern = '<li class="game-live-item" data-gid=([\s\S]*?)</li>'
    name_pattern = '<i class="nick" title="([\s\S]*?)">'
    number_pattern = '<i class="js-num">([\s\S]*?)</i>'
    

    # 私有方法，获取网页的内容
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        # bytes
        htmls = r.read()
        # 将字节码转换为字符串
        htmls = str(htmls, encoding='utf-8')
        return htmls

    # 分析函数
    def __analysis(self, htmls):
        # 匹配根正则
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        # 循环匹配姓名和人气
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name':name, 'number':number}
            # 将组合成的字典，加入列表中
            anchors.append(anchor)
        print(anchors)
        # 断点
        a = 1

    # Spider的入口方法
    def go(self):
        htmls = self.__fetch_content()
        self.__analysis(htmls)

spider = Spider()
spider.go()
```

# 数据精炼

strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列

```python
import re
# 导入获取html的库
from urllib import request

class Spider():
    url = 'https://www.huya.com/g/lol'
    # 根正则表达式
    root_pattern = '<li class="game-live-item" data-gid=([\s\S]*?)</li>'
    name_pattern = '<i class="nick" title="([\s\S]*?)">'
    number_pattern = '<i class="js-num">([\s\S]*?)</i>'
    

    # 私有方法，获取网页的内容
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        # bytes
        htmls = r.read()
        # 将字节码转换为字符串
        htmls = str(htmls, encoding='utf-8')
        return htmls

    # 分析函数
    def __analysis(self, htmls):
        # 匹配根正则
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        # 循环匹配姓名和人气
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name':name, 'number':number}
            # 将组合成的字典，加入列表中
            anchors.append(anchor)
        return anchors

    # 数据精炼
    def __refine(self, anchors):
        #  strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
        l = lambda anchor: {
            'name':anchor['name'][0].strip(),
            'number':anchor['number'][0].strip()
            }
        # map(函数, 集合)，map会把集合里面的所有元素都传入函数，然后返回一个map对象，里面保存了结果
        return map(l, anchors)

    # Spider的入口方法
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        print(anchors)


spider = Spider()
spider.go()
```

# 排序

排序函数：

sorted(集合, key=排序的种子, 升序还是降序)

sorted(anchors, key=self.__sort_seed, reverse=True)

```python
from os import read, readlink
import re
# 导入获取html的库
from urllib import request

class Spider():
    url = 'https://www.huya.com/g/lol'
    # 根正则表达式
    root_pattern = '<li class="game-live-item" data-gid=([\s\S]*?)</li>'
    name_pattern = '<i class="nick" title="([\s\S]*?)">'
    number_pattern = '<i class="js-num">([\s\S]*?)</i>'
    

    # 私有方法，获取网页的内容
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        # bytes
        htmls = r.read()
        # 将字节码转换为字符串
        htmls = str(htmls, encoding='utf-8')
        return htmls

    # 分析函数
    def __analysis(self, htmls):
        # 匹配根正则
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        # 循环匹配姓名和人气
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name':name, 'number':number}
            # 将组合成的字典，加入列表中
            anchors.append(anchor)
        return anchors

    # 数据精炼
    def __refine(self, anchors):
        #  strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
        l = lambda anchor: {
            'name':anchor['name'][0].strip(),
            'number':anchor['number'][0].strip()
            }
        # map(函数, 集合)，map会把集合里面的所有元素都传入函数，然后返回一个map对象，里面保存了结果
        return map(l, anchors)

    # 排序
    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    # 比较大小的种子
    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        r = r[0] + '.' + r[2]
        number = float(r)
        if '万' in anchor['number']:
            number *= 10000
        return number

    # 打印结果
    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('rank: ' + str(rank + 1)
            + ' | name: ' + anchors[rank]['name']
            + ' | number: ' + anchors[rank]['number'])

    # Spider的入口方法
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()
```

