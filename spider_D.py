import threading

import time
import urllib3
import re
import codecs
import testMultiThread


baseUrl = "http://tieba.baidu.com"
dict = {}
httpPoll = ""
filterDict = {}
keywords = ""
tb_name = ""

class user:
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


class postContent:
    # content user replied
    content = ""
    # user who post the content
    author = user()
    # content inner content
    innerContent = []

    def __init__(self):
        pass


class post:
    title = ""
    href = ""
    author = user()
    # list of postContent
    posContentList = []

    def __init__(self):
        pass

    def __init__(self, hrefValue, titleValue):
        self.title = titleValue
        self.href = hrefValue
        pass

class timer(threading.Thread):  # The timer class is derived from the class threading.Thread

    def __init__(self, num, interval, httpPoll):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False
        self.httpPoll = httpPoll

    def run(self):  # Overwrite run() method, put what you want the thread do here
        while not self.thread_stop:
            print('Thread Object')



    def stop(self):
        self.thread_stop = True

class postContentScanningTask(threading.Thread):
    global tb_name,keywords,filterDict

    def __init__(self, num, interval, httpPoll):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False
        self.httpPoll = httpPoll

    def run(self):
        pageInnerPost = self.httpPoll.request(method="GET", url=self.curPostUrl, fields={"pn": 1})
        pageCountPattern = re.compile(r"(?<=<span class=\"red\">).*?(?=</span>)")
        contentPostedPattern = re.compile(r"(?<=class=\"d_post_content j_d_post_content \">).*?(?=</div>)")
        authorNamePostedPattern = re.compile(r"(?<=<a data-field='\{&quot;un&quot;:&quot;).*?(?=&)")
        pageCount = int(pageCountPattern.findall(str(pageInnerPost.data))[0])

        curPostPage = pageCount
        # each page of postContent in cur url
        postContentList = []
        # 帖子内容页面限制
        pageCountLimit = 50
        # 从后往前遍历帖子内容
        while curPostPage >= 1 and (pageCount - curPostPage) <= pageCountLimit:
            pageInnerPost = self.sendRequest(httpPoll, self.curPostUrl, fields={"pn": curPostPage})
            # content = pageInnerPost.data.decode("utf-8")
            # content = bytes.decode(pageInnerPost.data)
            # there are some post may throw exception when decode, so i discards these page based on the page is far less than the total posts
            try:
                content = pageInnerPost.data.decode("utf-8")
            except:
                print("droped url:", self.curPostUrl)
                curPostPage += 1
                continue

            curPostPage -= 1
            # extract post content
            curPostsContentList = contentPostedPattern.findall(content)
            # curPostAuthorIdList = authorIdPostedPattern.findall(content)
            curPostAuthorNameList = [i.encode("utf-8").decode("unicode_escape") for i in
                                     authorNamePostedPattern.findall(content)]
            # if(curPostsContentList.__len__()!=curPostAuthorIdList.__len__()):
            #     print("content list size unequals to author list size")
            #     continue

            for curContent, curName in zip(curPostsContentList, curPostAuthorNameList):

                # curUser.userId = curUserId
                # print(codecs.escape_decode(str(curContent.encode("utf-8")))[0].decode("utf-8"))
                # try to use the code last line
                # remember the method of decode
                # get user info
                if self.keywords == "" or self.keywords in curContent:
                    if (dict.get(curName) == None):
                        curUser = self.getUserInfo(httpConnection=httpPoll, curName=curName)
                        if (self.userFilter(curUser, self.filterDict)):
                            dict[curName] = curUser
                            curPostContent = postContent()
                            curPostContent.content = curContent
                            postContentList.append(curPostContent)
                            print(curName, curUser)
                else:
                    continue
        self._stop()
    def _stop(self):
        self.thread_stop = True


class mySpider():
    def __init__(self):
        pass
    def __init__(self,tb_name_var,keywords_var,filterDict_var):
        global tb_name,keywords,filterDict
        tb_name = tb_name_var
        keywords = keywords_var
        filterDict = filterDict_var
        pass

    def buildConnection(self,url):
        # httpPoll = urllib3.HTTPConnectionPool(url, maxsize=1)
        httpPoll = urllib3.PoolManager()
        return httpPoll


    def sendRequest(self,connection, url, fields):
        page = connection.request(method="GET", url=url, fields=fields)
        return page


    def getUserInfo(self,httpConnection, curName):
        userUrl = "/home/get/panel"
        dict = {"un": curName, "ie": "utf-8"}
        curUser = user()
        userInfo = self.sendRequest(httpConnection, baseUrl + userUrl, fields=dict)
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

    def userFilter(self,userInfo,filterDict):
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

    def search(self):
        global httpPoll,tb_name,filterDict,keywords
        tb_name="炉石传说"
        keywords="内容"
        httpPoll = self.buildConnection("tieba.baidu.com")
        fields = {"kw": tb_name}
        # we get the index of someone tieba, it contains all the post index
        page = self.sendRequest(httpPoll, baseUrl + "/f", fields=fields)
        content = page.data.decode("utf-8")
        #帖子数量
        postNumLimit = 10
        pattern = re.compile(r"<a.*class=\"j_th_tit \".*>")
        posts = pattern.findall(content)
        # href contains /p/  exist title
        postList = []
        hrefPattern = re.compile(r"(?<=href=\").*?(?=\")")
        titlePattern = re.compile(r"(?<=title=\").*?(?=\")")
        # user url http://tieba.baidu.com/home/get/panel?ie=utf-8&un=athmey
        curPost = ""
        curPostPage = 1
        for i in posts:
            href = hrefPattern.findall(i)
            title = titlePattern.findall(i)
            curPost = post(href[0], title[0])
            # postContentScanningThread = postContentScanningTask(baseUrl + href[0])
            # postContentList = postContentScanningThread.start()

            thread1 = timer(httpPoll,1,1,baseUrl + href[0])
            thread1.start()
            postContentList = ""
            curPost.posContentList = postContentList
            postList.append(curPost)
            curPostPage += 1
            print(curPostPage,"/",posts.__len__(),"finished")

        contentPostedList = []

        # authorIdPostedPattern = re.compile(r"(?<=class=\"d_name\" data-field='{&quot;user_id&quot;:)\d+?(?=})")
        # authorNamePostedPattern = re.compile(r"((?<=a data-field=\\'\{&quot;un&quot;:&quot;).*?(?=&quot))")

        # inner content extract
        # innerContentPattern = re.compile(r"<?<=<ul class=\"j_lzl_m_w\" style=\"display:\">>.*<?=/ul>")

        # the first layer is each post


        return postList,dict



