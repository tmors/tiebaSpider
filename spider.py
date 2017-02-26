import urllib3
import re
import codecs

baseUrl = "http://tieba.baidu.com"
dict = {}
class user:
    userId = 0
    userName = ""
    #tieba age
    userAge = 0
    #post number
    postNumb = 0
    #sex
    sex = ""
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


def getUserInfo(httpConnection,curName):
    userUrl = "/home/get/panel"
    dict = {"un": curName, "ie": "utf-8"}
    curUser = user()
    userInfo = sendRequest(httpConnection, baseUrl + userUrl, fields=dict)
    userInfoData = userInfo.data.decode("utf-8")
    # pattern to extract user info
    userAgePattern = re.compile(r"(?<=tb_age\":).*?(?=,)")
    userPostNumbPattern = re.compile(r"(?<=post_num\":).*?(?=,)")
    userSexPattern = re.compile(r"(?<=sex\":\").*?(?=\")")
    curUser.userAge = float(userAgePattern.findall(userInfoData)[0].replace("\"",""))
    postNumbStr = userPostNumbPattern.findall(userInfoData)[0].replace("\"","")
    postNum = 0
    #because \\u4e07 represent ten thousands
    if "\\u4e07" in postNumbStr:
        postNum = float(postNumbStr.replace("\\u4e07",""))*10000
    else:
        postNum = float(postNumbStr)
    curUser.postNumb = postNum
    curUser.sex = userSexPattern.findall(userInfoData)[0]
    curUser.userName = curName
    print("userAge",curUser.userAge,"userName",curUser.userName,"postNum",curUser.postNumb)
    return curUser

def main():
    httpPoll = buildConnection("tieba.baidu.com")
    fields={"kw":"炉石传说"}
    #we get the index of someone tieba, it contains all the post index
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
    pageCountPattern = re.compile(r"(?<=<span class=\"red\">).*?(?=</span>)")
    # the first layer is each post
    for curPostInfo in postList:
        curPostPage = 1
        pageCount = 1
        #search each page in cur url
        postContentList = []
        #the second layer is each page in the post
        while curPostPage <= pageCount:
            pageInnerPost = sendRequest(httpPoll,baseUrl + curPostInfo.href,fields={"pn":curPostPage})
            # content = pageInnerPost.data.decode("utf-8")
            # content = bytes.decode(pageInnerPost.data)
            #there are some post may throw exception when decode, so i discards these page based on the page is far less than the total posts
            try:
                content = pageInnerPost.data.decode("utf-8")
            except:
                print("droped url:",baseUrl+curPostInfo.href)
                continue
            pageCount = int(pageCountPattern.findall(content)[0])
            curPostPage += 1
            #extract post content
            curPostsContentList = contentPostedPattern.findall(content)
            # curPostAuthorIdList = authorIdPostedPattern.findall(content)
            curPostAuthorNameList = [i.encode("utf-8").decode("unicode_escape") for i in authorNamePostedPattern.findall(content)]
            # if(curPostsContentList.__len__()!=curPostAuthorIdList.__len__()):
            #     print("content list size unequals to author list size")
            #     continue

            for curContent,curName in zip(curPostsContentList,curPostAuthorNameList):
                curPostContent = postContent()
                # escapedContent = codecs.escape_decode(curContent)[0]
                curPostContent.content = curContent
                # curUser.userId = curUserId
                #print(codecs.escape_decode(str(curContent.encode("utf-8")))[0].decode("utf-8"))
                #try to use the code last line
                #remember the method of decode
                #get user info
                curUser = getUserInfo(httpConnection=httpPoll,curName=curName)
                postContent.author = curUser
                postContentList.append(curPostContent)
            print(baseUrl+curPostInfo.href,"page:",curPostPage,"finished")

        curPostInfo.posContentList = postContentList
        print(baseUrl + curPostInfo.href,"finished")

    print(page)

if __name__=="__main__":
    main()
