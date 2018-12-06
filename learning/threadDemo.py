import threading
import time 
 

exitFlag = False
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

def write(file, content, start=0, end=100,):
    with open(file,"rb+") as f:
        f.seek(start)
        content_size = len(content)
        real = content
        if (start + content_size) > end:
            real = content[:end - start]
        f.write(real)

 
def make_file(file, size):
    '''创建一个大小为size的临时文件
    '''
    with open(file,"bw") as f:
        content = b'\x01' * size
        f.write(content)

def file_split(size, t_num):
    '''根据线程数分割文件块'''
    a = size // t_num
    b = a + size % t_num
    part = [a] * t_num
    part[-1] = b
    res = [(i*a, (i+1)*a) for i in range(t_num)] 
    x , y = res[-1]
    y = x + b
    res[-1] = (x, y)
    return res
     

if __name__ == "__main__":
    f = 'a.txt'
    tNum = 4
    fSize = 21
    make_file(f, fSize)
    parts = file_split(fSize,tNum)
    contents=[b'abcdefg', b'123456','你'.encode('utf8'), b'hello jack']
    for i in range(tNum):
        start, end = parts[i]
        th = threading.Thread(target=write, args=(f,contents[i], start, end))
        th.start()
 

""" make_file('a.txt')
thread1 = threading.Thread(target=print_time, args=("Thread-1",1,4))
thread2 = threading.Thread(target=print_time, args=("Thread-2",2,4))
kw1 = {'file':'a.txt', 'start': 0, 'content':b'abc\n'}
kw2 = {'file':'a.txt', 'start': 10, 'content':b'123\n'}
kw3 = {'file':'a.txt', 'start': 20, 'content':b'xxx\n'}
thread3 = threading.Thread(target=write, kwargs=kw1)
thread4 = threading.Thread(target=write, kwargs=kw2)
thread5 = threading.Thread(target=write, kwargs=kw3) 
# 开启新线程
thread3.start()
thread4.start()
thread5.start()
#thread1.join()
#thread2.join()
print ("退出主线程") """