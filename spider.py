import urllib3
from urllib3 import *
import xml.etree.ElementTree as ET
from lxml import etree
from xml.parsers import expat
import re

class user:
    userAge = 0
    postNumb = 0
    def __init__(self):
        pass
    def __init__(self,userAge,postNum):
        self.userAge = userAge
        self.postNumb = postNum
        pass

class post:
    title = ""
    href = ""
    author = user(0,0)
    def __init__(self):
        pass
    def __init__(self,titleValue,hrefValue):
        self.title = titleValue
        self.href = hrefValue
        pass
    def setTitle(self,titleValue):
        self.title = titleValue
        pass
    def setHref(self,hrefValue):
        self.href = hrefValue
        pass
    def getTitle(self):
        return self.title
    def getHref(self):
        return self.href

def buildConnection(url):
    httpPoll = urllib3.HTTPConnectionPool(url, maxsize=1)
    return httpPoll

def sendRequest(connection,url,fields):
    page = connection.request(method="GET",url=url,fields=fields)
    return page

def main():
    httpPoll = buildConnection("tieba.baidu.com")
    fields={"kw":"花泽香菜"}
    page = sendRequest(httpPoll,"/f",fields=fields)
    content = page.data.decode("utf-8")


    pattern = re.compile(r"<a.*class=\"j_th_tit \".*>")
    posts = pattern.findall(content)
    #href contains /p/  exist title
    postList = []
    hrefPattern = re.compile(r"(?<=href=\").*?(?=\")")
    titlePattern = re.compile(r"(?<=title=\").*?(?=\")")


    for i in posts:
        href = hrefPattern.findall(i)
        title = titlePattern.findall(i)
        curPost = post(href,title)
        postList.append(curPost)


    print(page)

if __name__=="__main__":
    main()
