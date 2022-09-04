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
        return htmls

    # 分析函数
    def __analysis(self, htmls):
        pass

    # Spider的入口方法
    def go(self):
        htmls = self.__fetch_content()
        self.__analysis(htmls)

spider = Spider()
spider.go()