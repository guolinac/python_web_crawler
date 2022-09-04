import re
# 导入获取html的库
from urllib import request

class Spider():
    url = 'https://www.huya.com/g/lol'
    # 根正则表达式
    root_pattern = '<li class="game-live-item" data-gid=[\s\S]*?</li>'
    

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
        root_html = re.findall(Spider.root_pattern, htmls)
        print(root_html[0])
        # 断点
        a = 1

    # Spider的入口方法
    def go(self):
        htmls = self.__fetch_content()
        self.__analysis(htmls)

spider = Spider()
spider.go()