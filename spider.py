import urllib3
import re
import codecs

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


def getUserInfo(httpConnection,baseUrl,curName):
    userUrl = "/home/get/panel"
    dict = {"un": curName, "ie": "utf-8"}
    curUser = user()
    userInfo = sendRequest(httpConnection, baseUrl + userUrl, fields=dict)
    userInfoData = userInfo.data.decode("utf-8")
    # pattern to extract user info
    userAgePattern = re.compile(r"(?<=tb_age\":).*?(?=,)")
    userPostNumbPattern = re.compile(r"(?<=post_num\":).*?(?=,)")
    userSexPattern = re.compile(r"(?<=sex\":\").*?(?=\")")
    curUser.userAge = userAgePattern.findall(userInfoData)[0]
    curUser.postNumb = userPostNumbPattern.findall(userInfoData)[0]
    curUser.sex = userSexPattern.findall(userInfoData)[0]
    curUser.userName = curName
    print("userAge",curUser.userAge,"userName",curUser.userName,"postNum",curUser.postNumb)
    return curUser
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
            # curUser.userId = curUserId
            #print(codecs.escape_decode(str(curContent.encode("utf-8")))[0].decode("utf-8"))
            #try to use the code last line
            #remember the method of decode
            curName = curName.encode("utf-8").decode("unicode_escape")
            #get user info
            curUser = getUserInfo(httpConnection=httpPoll,baseUrl=baseUrl,curName=curName)
            postContent.author = curUser
            postContentList.append(curPostContent)

        i.posContentList = postContentList
        print(baseUrl+i.href,"finished")

    print(page)

if __name__=="__main__":
    main()
