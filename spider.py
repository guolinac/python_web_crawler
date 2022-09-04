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