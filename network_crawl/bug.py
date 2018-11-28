#coding:utf-8
from urllib import request 
import re

#url =  'http://localhost:10017/1/index.html' 
url = r'https://tieba.baidu.com/index.html'
#url = r'http://tieba.baidu.com/p/1753935195'
file = 'g:/test.html'
 
def getPage(url, file) :
    with request.urlopen(url) as html : 
        res = html.read()
        with open(file, 'w') as f :  
                f.write(res.decode('utf-8'))

def get_html(url) :
    page = ''
    with request.urlopen(url) as html : 
        res = html.read()
        page = res.decode('utf-8') 
    return page
 
def fet_img() :
    reg = r'src=[\'\"]?([^\'\"]*)[\'\"]?'#正则表达式
    imgReg = r'<img.*?(?:>|\/>)'
    srcReg = r'src=[\'\"]?(http:\/\/|https:\/\/)([^\'\"]*)[\'\"]?'
    reg_img = re.compile(imgReg)#编译一下，运行更快
    src_img = re.compile(srcReg)

    imglist = reg_img.findall(get_html(url))#进行匹配
    x = 0
    for img in imglist: 
        m = re.search(src_img, img)
        if m : 
            url2 = m.group(0)
            url2 = url2[5 : -1]
            print(url2)
            pfx = url2[-3:]
            print(pfx)
            request.urlretrieve(url2, '%s.%s' % (x,pfx))
            x += 1
 
def fetch_image() :
    allReg = r'<img.*? src=[\'\"]?(http:\/\/|https:\/\/)([^\'\"]*)[\'\"]?'
    all_img = re.compile(allReg)
    pageStr = get_html(url)
    imgList = all_img.findall(pageStr)
    count = 0
    for imgUrl in imgList  : 
        #print(imgUrl[1])
        iUrl = imgUrl[0] + imgUrl[1]
        index = iUrl.rindex('.')
        pfx = iUrl[index + 1 :]
        count += 1
        print( '%d url: %s, fileName: %s' % (count, iUrl, pfx))
        request.urlretrieve(iUrl, '%s.%s' % (count, pfx))


fetch_image()