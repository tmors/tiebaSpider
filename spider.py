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

class postContent:
    #content user replied
    content = ""
    #user who post the content
    author = user()
    #content inner content
    innerContent = []
    def __init__(self):
        pass

class post:
    title = ""
    href = ""
    author = user()
    #list of postContent
    posContentList = []
    def __init__(self):
        pass
    def __init__(self,hrefValue,titleValue):
        self.title = titleValue
        self.href = hrefValue
        pass
def buildConnection(url):

    # httpPoll = urllib3.HTTPConnectionPool(url, maxsize=1)
    httpPoll = urllib3.PoolManager()
    return httpPoll

def sendRequest(connection,url,fields):
    page = connection.request(method="GET",url=url,fields=fields)
    return page

def main():
    baseUrl = "http://tieba.baidu.com"
    httpPoll = buildConnection("tieba.baidu.com")
    fields={"kw":"花泽香菜"}
    page = sendRequest(httpPoll,baseUrl+"/f",fields=fields)
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
        curPost = post(href[0],title[0])
        postList.append(curPost)

    contentPostedList = []
    contentPostedPattern = re.compile(r"(?<=class=\"d_post_content j_d_post_content \">).*?(?=</div>)")
    authorPostedPattern = re.compile(r"(?<=class=\"d_name\" data-field='{&quot;user_id&quot;:)\d+?(?=\")")
    for i in postList:
        pageInnerPost = sendRequest(httpPoll,baseUrl + i.href,fields={})
        content = pageInnerPost.data.decode("utf-8")
        #extract post content
        curPostsContentList = contentPostedPattern.findall(content)
        curPostAuthorIdList = authorPostedPattern.findall(content)
        postContentList = []
        for i,j in curPostsContentList,curPostAuthorIdList:
            curPostContent = postContent()
            curPostContent.content = i
            curPostContent.author = j
            postContentList.append(curPostContent)

        i.posContentList = postContentList
        print()

    print(page)

if __name__=="__main__":
    main()
