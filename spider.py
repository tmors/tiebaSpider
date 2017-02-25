import urllib3
from urllib3 import *
import xml.etree.ElementTree as ET
from lxml import etree
from xml.parsers import expat
import re
import codecs

class user:
    userId = 0
    userName = ""
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
    bodyPattern = re.compile(r"<body>.*</body>")
    body = bodyPattern.findall(str(page.data))
    content = page.data.decode("utf-8")


    pattern = re.compile(r"<a.*class=\"j_th_tit \".*>")
    posts = pattern.findall(content)
    #href contains /p/  exist title
    postList = []
    hrefPattern = re.compile(r"(?<=href=\").*?(?=\")")
    titlePattern = re.compile(r"(?<=title=\").*?(?=\")")
    #user url http://tieba.baidu.com/home/get/panel?ie=utf-8&un=athmey

    for i in posts:
        href = hrefPattern.findall(i)
        title = titlePattern.findall(i)
        curPost = post(href[0],title[0])
        postList.append(curPost)

    contentPostedList = []
    contentPostedPattern = re.compile(r"(?<=class=\"d_post_content j_d_post_content \">).*?(?=</div>)")
    # authorIdPostedPattern = re.compile(r"(?<=class=\"d_name\" data-field='{&quot;user_id&quot;:)\d+?(?=})")
    # authorNamePostedPattern = re.compile(r"((?<=a data-field=\\'\{&quot;un&quot;:&quot;).*?(?=&quot))")
    authorNamePostedPattern = re.compile(r"(?<=<a data-field='\{&quot;un&quot;:&quot;).*?(?=&)")
    #inner content extract
    innerContentPattern = re.compile(r"<?<=<ul class=\"j_lzl_m_w\" style=\"display:\">>.*<?=/ul>")
    for i in postList:
        pageInnerPost = sendRequest(httpPoll,baseUrl + i.href,fields={})
        # content = pageInnerPost.data.decode("utf-8")
        # content = bytes.decode(pageInnerPost.data)
        try:
            content = pageInnerPost.data.decode("utf-8")
        except:
            print("droped url:",baseUrl+i.href)
            continue

        #extract post content
        curPostsContentList = contentPostedPattern.findall(content)
        # curPostAuthorIdList = authorIdPostedPattern.findall(content)
        curPostAuthorNameList = authorNamePostedPattern.findall(content)
        # if(curPostsContentList.__len__()!=curPostAuthorIdList.__len__()):
        #     print("content list size unequals to author list size")
        #     continue
        postContentList = []
        for curContent,curName in zip(curPostsContentList,curPostAuthorNameList):
            curPostContent = postContent()
            # escapedContent = codecs.escape_decode(curContent)[0]
            curPostContent.content = curContent
            curUser = user()
            # curUser.userId = curUserId
            #remember the method of decode
            curName = curName.encode("utf-8").decode("unicode_escape")
            curUser.userName = curName
            postContent.author = curUser
            userUrl = "/home/get/panel"
            dict = {"un":curName,"ie":"utf-8"}
            userInfo = sendRequest(httpPoll,baseUrl + userUrl,fields=dict)
            postContentList.append(curPostContent)

        i.posContentList = postContentList
        print(baseUrl+i.href,"finished")

    print(page)

if __name__=="__main__":
    main()
