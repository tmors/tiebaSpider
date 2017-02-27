import re
import threading

import time

baseUrl = "http://tieba.baidu.com"
dict = {}
httpPool = ""
filterDict = {}
keywords = ""
tb_name = ""
import urllib3

postAndContentDict =  {}




class User:
    userId = 0
    userName = ""
    # tieba age
    userAge = 0
    # post number
    postNumb = 0
    # sex
    sex = ""
    def __init__(self):
        pass
    def toString(self):
        return self.userName + " " + self.sex + " "  + str(self.userAge) + " "  + str(self.postNumb)

class Post:
    author = User()
    title = ""
    href = ""
    postContentList = []

class PostContent:
    # content user replied
    content = ""
    # user who post the content
    author = User()
    # content inner content
    innerContent = []

    def __init__(self):
        pass

def userFilter(userInfo):
    global filterDict
    sexRequired = filterDict.get("sex")
    tb_age_min = filterDict.get("tg_age_min")
    isVIP = filterDict.get("isVIP")
    if(tb_age_min!=None and userInfo.userAge < tb_age_min):
        return False
    if(sexRequired!=None and userInfo.sex != sexRequired):
        return False
    if(isVIP!=None and userInfo.isVIP != isVIP):
        return False
    return True

def getUserInfo(curName):
    global httpPool
    userUrl = "/home/get/panel"
    dict = {"un": curName, "ie": "utf-8"}
    curUser = User()

    userInfo = httpPool.request(method="GET", url=baseUrl + userUrl, fields=dict)
    userInfoData = userInfo.data.decode("utf-8")
    # pattern to extract user info
    userAgePattern = re.compile(r"(?<=tb_age\":).*?(?=,)")
    userPostNumbPattern = re.compile(r"(?<=post_num\":).*?(?=,)")
    userSexPattern = re.compile(r"(?<=sex\":\").*?(?=\")")
    curUser.userAge = float(userAgePattern.findall(userInfoData)[0].replace("\"", ""))
    postNumbStr = userPostNumbPattern.findall(userInfoData)[0].replace("\"", "")
    postNum = 0
    # because \\u4e07 represent ten thousands
    if "\\u4e07" in postNumbStr:
        postNum = float(postNumbStr.replace("\\u4e07", "")) * 10000
    else:
        postNum = float(postNumbStr)
    curUser.postNumb = postNum
    curUser.sex = userSexPattern.findall(userInfoData)[0]
    curUser.userName = curName
    # print("userAge", curUser.userAge, "userName", curUser.userName, "postNum", curUser.postNumb)
    return curUser




class postContentScanner(threading.Thread):  # The timer class is derived from the class threading.Thread
    def __init__(self,curPostUrl):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.curPostUrl = curPostUrl

    def run(self):  # Overwrite run() method, put what you want the thread do here
        if(self.thread_stop == False):
            firstPage = httpPool.request(method="GET", url=self.curPostUrl, fields={"pn": 1})
            # 帖子内容正则表达式
            pageCountPattern = re.compile(r"(?<=<span class=\"red\">).*?(?=</span>)")
            contentPostedPattern = re.compile(r"(?<=class=\"d_post_content j_d_post_content \">).*?(?=</div>)")
            authorNamePostedPattern = re.compile(r"(?<=<a data-field='\{&quot;un&quot;:&quot;).*?(?=&)")

            # 帖子总页数
            pageCount = int(pageCountPattern.findall(str(firstPage.data))[0])
            curPageCount = pageCount
            pageCountLimit = 5

            # 贴吧回复列表
            postContentList = []
            while curPageCount >= 1 and (pageCount - curPageCount) <= pageCountLimit:
                curPageContent = httpPool.request(method="GET", url=self.curPostUrl,
                                                  fields={"pn": curPageCount})
                try:
                    content = curPageContent.data.decode("utf-8")
                except:
                    print("droped url:", self.curPostUrl)
                    curPageCount -= 1
                    continue
                curPageCount -= 1

                # 提取帖子回复内容
                curPostsContentList = contentPostedPattern.findall(content)

                # 提取帖子回复作者
                curPostAuthorNameList = [i.encode("utf-8").decode("unicode_escape") for i in
                                         authorNamePostedPattern.findall(content)]

                for curContent, curName in zip(curPostsContentList, curPostAuthorNameList):
                    if keywords == "" or keywords in curContent:
                        if (dict.get(curName) == None):
                            curUser = getUserInfo(curName=curName)
                            if (userFilter(curUser)):
                                dict[curName] = curUser
                                curPostContent = PostContent()
                                curPostContent.content = curContent
                                postContentList.append(curPostContent)

                                # print(curName, curUser)
                    else:
                        continue

            print(self.getName(),"stopped")
            self.thread_stop = True


    def stop(self):
        self.thread_stop = True



class mySpider:
    def __init__(self,tb_name_var,keywords_var,filterDict_var,):
        global filterDict,keywords,tb_name,dict
        dict = {}
        filterDict = filterDict_var
        keywords = keywords_var
        tb_name = tb_name_var
        return
    def search(self):
        global dict

        postCountLimit = 30
        global httpPool,filterDict,keywords,tb_name
        httpPool = urllib3.PoolManager()

        page = httpPool.request(method="GET", url = baseUrl + "/f", fields={"kw": tb_name})
        print("open the main page")
        content = page.data.decode("utf-8")
        pattern = re.compile(r"<a.*class=\"j_th_tit \".*>")
        posts = pattern.findall(content)
        hrefPattern = re.compile(r"(?<=href=\").*?(?=\")")
        threads = []
        curPostNum = 1
        for i in posts:
            if(curPostNum > postCountLimit):
                break
            hrefList = hrefPattern.findall(i)
            print("open post url ", i)
            postContentTask = postContentScanner(baseUrl + hrefList[0])
            threads.append(postContentTask)
            postContentTask.start()
            curPostNum += 1

        time.sleep(5)
        stopedThreads = threads
        startTime = time.time()
        while time.time() - startTime < 10 and stopedThreads.__len__()!= 0:
            stopedThreads = threads
            stopedThreads = [i for i in stopedThreads if i.isAlive() == True]
            time.sleep(1)
            print("alived thread:",stopedThreads.__len__())

        print(dict)
        postList = []
        return postList,dict
def test():
    myS = mySpider("炉石传说","内容",{"sex":"male"})
    myS.search()


    return


if __name__ == '__main__':
    test()