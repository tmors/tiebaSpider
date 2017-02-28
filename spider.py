import re
import threading

import time
from enum import Enum

baseUrl = "http://tieba.baidu.com"
dict = {}
httpPool = ""
filterDict = {}
keywords = ""
tb_name = ""
import urllib3
sexDict = {"male":1,"female":2}
postAndContentDict =  {}
totalThread = []
dictLock=threading.Lock()
#帖子回复内容也被提取出来了，但是由于目前改为多线程版本，数据在线程里面没有传回来

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
    if(sexRequired!=None and sexRequired != 0 and sexDict.get(userInfo.sex) != sexRequired):
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
                    print("droped url:", self.curPostUrl ,"pn is", curPageCount)
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
                                dictLock.acquire()
                                dict[curName] = curUser
                                dictLock.release()

                                curPostContent = PostContent()
                                curPostContent.content = curContent
                                postContentList.append(curPostContent)
                                print("add user:", curName)

                                # print(curName, curUser)
                    else:
                        continue

            # print(self.getName(),"stopped")
            self.stop()


    def stop(self):
        self.thread_stop = True



class PostPageScanner(threading.Thread):
    def __init__(self,cur_tb_name,curPn):
        threading.Thread.__init__(self)
        self.curPn = curPn
        self.cur_tb_name = tb_name
        self.threadStop = False
        return
    def run(self):
        if(self.threadStop != True):
            global dict
            postCountLimit = 50
            global httpPool, filterDict, keywords
            httpPool = urllib3.PoolManager()

            page = httpPool.request(method="GET", url=baseUrl + "/f", fields={"kw": self.cur_tb_name, "pn": self.curPn})
            print("open the main page")
            content = page.data.decode("utf-8")
            pattern = re.compile(r"<a.*class=\"j_th_tit \".*>")
            posts = pattern.findall(content)
            hrefPattern = re.compile(r"(?<=href=\").*?(?=\")")
            threads = []
            curPostNum = 1
            for i in posts:
                if (curPostNum > postCountLimit):
                    break
                hrefList = hrefPattern.findall(i)
                print("open post url ", i)
                postContentTask = postContentScanner(baseUrl + hrefList[0])
                postContentTask.setDaemon(True)
                threads.append(postContentTask)
                totalThread.append(postContentTask)
                postContentTask.start()
                time.sleep(2)
                curPostNum += 1


            alivedThreads = threads
            startTime = time.time()
            while time.time() - startTime < 10 and alivedThreads.__len__() != 0:
                alivedThreads = threads
                alivedThreads = [i for i in alivedThreads if i.isAlive() == True]
                time.sleep(1)

            print("curPn", self.curPn, "finished","dict len is ",dict.__len__())
            self.stop()
    def stop(self):
        self.threadStop = True

def test():
    myS = PostPageScanner("炉石传说","",{"sex":"male"})
    myS.search()


    return


class Main(threading.Thread):
    def __init__(self,tb_name_var,keywords_var,filterDict_var):
        threading.Thread.__init__(self)
        global filterDict,keywords,tb_name,dict
        dict = {}
        filterDict = filterDict_var
        keywords = keywords_var
        tb_name = tb_name_var
        self.threadStop = False
        return
    def run(self):
        if(self.threadStop == False):
            global tb_name
            postPageLimit = 1
            threads = []
            for i in range(0, postPageLimit):
                postPageThread = PostPageScanner(tb_name, i * 50)
                totalThread.append(postPageThread)
                postPageThread.start()
                time.sleep(5)
                threads.append(postPageThread)
            time.sleep(5)
            alivedThreads = threads
            startTime = time.time()
            while alivedThreads.__len__() != 0:
                alivedThreads = threads
                alivedThreads = [i for i in alivedThreads if i.isAlive() == True]
                time.sleep(1)
                print("post page alived thread:", alivedThreads.__len__())
            print(dict.__len__())
            self.threadStop()
    def threadStop(self):
        self.threadStop = True

if __name__ == '__main__':

    mainThread = Main("炉石传说", "", {"sex": 0})
    mainThread.setDaemon(True)
    mainThread.start()
    isAllThreadsStopped = False
    while (isAllThreadsStopped != True):
        isAllThreadsStopped = True
        for curThread in totalThread:
            if (curThread.isAlive() == True):
                isAllThreadsStopped = False
                break
        time.sleep(5)