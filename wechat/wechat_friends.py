#-*- coding:utf-8 -*- 
from pyecharts import Map
import itchat
import re
import sys
import os
import numpy as np
import PIL.Image as Image
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, ImageColorGenerator



def friendsLoaction(friends):
    obj = {}
    for friend in friends:
        p = friend['Province']
        if p == '':
            p = 'unknown'
        if p in obj :
            obj[p] += 1
        else:
            obj.update({p:1})

    provinces = list(obj.keys())
    count = [ obj[key] for key in provinces]
    
    map=Map("各省微信好友分布", width=1200, height=600) 
    map.add("", provinces, count, maptype='china', is_visualmap=True, visual_text_color='#000') 
    map.show_config() 
    map.render()


def analyseSignature(friends):
    signatures = ''
    emotions = []

    tList = []
    for friend in friends:
        # 获取好友的签名
        signature = friend['Signature']
        if (signature != None):
            # 过滤掉标签和表情
            signature = signature.strip().replace('span', '').replace('class', '').replace('emoji', '')
            signature = re.sub(r'1f(\d.+)', '', signature)
            tList.append(signature)

            if (len(signature) > 0):
                pass
                # 分析标签
                #nlp = SnowNLP(signature)
                # 获取情绪值
                #emotions.append(nlp.sentiments)
                # 结巴分析
                #signatures += ' '.join(jieba.analyse.extract_tags(signature, 5))  
    # 拼接字符串
    text = "".join(tList) 
    # jieba分词 
    wordlist_jieba = jieba.cut(text, cut_all=True)
    signatures = " ".join(wordlist_jieba)
 
    #back_coloring = np.array(Image.open('baseketball.jpg'))
    d = os.path.dirname(__file__)
    alice_coloring = np.array(Image.open(os.path.join(d, "wechat.jpg")))
    wordcloud = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
                         max_font_size=40, random_state=42,
                         font_path='C:/Windows/Fonts/FZSTK.TTF')

    # 生成云词
    wordcloud.generate(signatures)
    image_colors = ImageColorGenerator(alice_coloring)
    plt.imshow(wordcloud.recolor(color_func=image_colors)) 
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file('signatures.jpg')

 
if __name__ == '__main__' :
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)
    analyseSignature(friends)
    friendsLoaction(friends)