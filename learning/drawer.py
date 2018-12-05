import tkinter
import random
import threading
import time
import csv    
#加载csv包便于读取csv文件
# 初始化窗口
root = tkinter.Tk()
root.title("上海克比年会抽奖名单")
root.geometry('500x500+400+200')
root.resizable(False, False)
root.flag = True

# 三个Lable标签
#csv_file=open('c:/12.csv')    
#打开csv文件
#csv_reader_lines = csv.reader(csv_file)   
#逐行读取csv文件
students = [ range(100)]    
#创建列表准备接收csv各行数据
#for one_line in csv_reader_lines:    
    #students.append(one_line)  
    # 将读取的csv分行数据按行存入列表‘date’中
    #students.append(one_line)
    
def switch():    
    root.flag = True    
    while root.flag:        
        i = random.randint(0, len(students) - 1) 
        first, second, third = {},{},{}       
        first['text'] = students       
        second['text'] = students        
        third['text'] = students        
        time.sleep(0.001)
        first = tkinter.Label(root, text='', font=("宋体", 20, "normal"))
        first.place(x=100, y=100, width=300, height=100)
        second = tkinter.Label(root, text='', font=("宋体", 20, "normal"))
        second['fg'] = 'red'
        second.place(x=100, y=200, width=300, height=100)
        third = tkinter.Label(root, text='', font=("宋体", 20, "normal"))
        third.place(x=100, y=300, width=300, height=100)

# 开始按钮
def butStartClick():    
    t = threading.Thread(target=switch)    
    t.start()
    #设置几个奖项


# 结束按钮
def btnStopClick():    
    root.flag = False


btnStart = tkinter.Button(root, text='开始', command=butStartClick)
btnStart.place(x=20, y=30, width=80, height=20)
one = tkinter.Button(root, text='一等奖', command=butStartClick)
one.place(x=110, y=30, width=80, height=20)
two = tkinter.Button(root, text='二等奖', command=butStartClick)
two.place(x=210, y=30, width=80, height=20)
three= tkinter.Button(root, text='三等奖', command=butStartClick)
three.place(x=310, y=30, width=80, height=20)
butStop = tkinter.Button(root, text='停止', command=btnStopClick)
butStop.place(x=410, y=30, width=80, height=20)
# 启动主程序
root.mainloop()