import urllib.request
import time
from bs4 import BeautifulSoup 


Help=   """
        友情提示：
        请输入城市拼音获取天气结果，如果无法识别，自动返回首都记录
        """ 
fmt = r"http://www.pm25.com/%s.html"

def getPM25(cityname):
    site = fmt % cityname
    page = urllib.request.urlopen(site)
    html = page.read()
    soup = BeautifulSoup(html.decode("utf-8"),"html.parser")
    city = soup.find(class_='bi_loaction_city')                 # 城市名称
    aqi = soup.find("a", {"class", "bi_aqiarea_num"})           # AQI指数
    quality = soup.select(".bi_aqiarea_right span")             # 空气质量等级
    result = soup.find("div", class_='bi_aqiarea_bottom')       # 空气质量描述
    output=city.text + u'AQI指数：' + aqi.text + u'\n空气质量：' + quality[0].text + result.text
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(output)
    print('*' * 20 + currentTime + '*' * 20)
    return output
 
if __name__ == '__main__':
    getPM25('suzhou')