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