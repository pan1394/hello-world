from os.path import getsize, exists
import sys, getopt, threading, time, urllib
sys.path.append('../')
from download.progressBar import ProgressBar
from download.database import DatabaseX

def copy(sourceFile, targetFile=None, bufferSize = 1024, realTimeFunc=None):
    if targetFile == None:
        targetFile = replaceFileName(sourceFile)
    try:
        with open(sourceFile, "rb") as s:
            with open(targetFile, "wb") as d: 
                while True:
                    chunk = None 
                    chunk = s.read(bufferSize)
                    if not chunk : break
                    d.write(chunk)
                    if realTimeFunc:
                        realTimeFunc()
    except Exception:
        print('error during copy...')  
    else:
        print("[{}] has copied to [{}].".format(sourceFile,targetFile))
       
def copyx(s, targetFile=None, bufferSize = 1024, realTimeFunc=None, copied=0, total=1):
    sourceFile = 'test'
    try:
        finished = False   
        if copied: 
            s.seek(copied)
        with open(targetFile, "ab") as d: 
            if copied : d.seek(copied)
            while True:
                chunk = None 
                chunk = s.read(bufferSize)
                copied += len(chunk)
                if not chunk : break
                d.write(chunk)
                if realTimeFunc:
                    for k, func in realTimeFunc.items():
                        if k == 'f1': func('size', copied)
                        if k == 'f2': func() 
            finished = True
        return finished
    except:
        print('error during copy...')  
    finally:
        if not finished: 
            print("[{}] being copied to [{}], copyed {}, complete rate: {:.1f}%.".format(sourceFile,targetFile, copied, float((copied/total) * 100)))
        else:
            print("[{}] has copied to [{}].".format(sourceFile,targetFile))
        return finished
  
def copyX2(s, targetFile, storeKey, bufferSize = 1024, realTimeFunc=None, copied=0, start=0, end=100):
    sourceFile = 'test'
    thName = threading.currentThread().getName()
    total = end - start
    position = start + copied
    try:
        finished = False   
        if position : s.seek(position)
        with open(targetFile, "rb+") as d: 
            if position : d.seek(position)
            while True:
                chunk = None 
                chunk = s.read(bufferSize)
                copied += len(chunk)
                if not chunk : break
                real = chunk
                if position + len(chunk) > end: 
                    real = chunk[:end - position]
                d.write(real)
                if realTimeFunc:
                    for k, func in realTimeFunc.items(): 
                        #if k == 'f1': func(storeKey, copied)
                        if k == 'f2': func() 
            finished = True
        return finished
    except:
        print('error during copy...')  
    finally:
        if not finished:   
            print("[{}] being copied to [{}], copyed {}, complete rate: {:.1f}%.".format(sourceFile,targetFile, copied, float((copied/total) * 100)))
        else: 
            print("[{}-{}] has copied to [{}].".format(thName,sourceFile,targetFile))
        return finished

def retrieveFileName(fileName):
    try:
        import re
        pattern = r'([^/]+)(\.\w{3,})'
        m = re.search(pattern, fileName)
        if m :
            return m.group(1)
    except Exception as e:
        print(e)

def replaceFileName(fileName):
    try:
        import re
        pattern = r'([^/]+)(\.\w{3,})'
        return re.sub(pattern, lambda m:addTimeStamp(m.group(1))+m.group(2), fileName) 
    except Exception as e:
        print(e)

def addTimeStamp(a):
     import time
     fmt = "%Y%m%d%H%M%S"
     fs = time.localtime(time.time())
     return a + '_' + time.strftime(fmt, fs)

def exec(source, destination, chunk, thread_num=0): 
    '''
    source -> source file abs path
    destination -> destination file abs path, if not entered, a default name provided
    chunk ->  a chunk to store buffer
    ''' 
    bar_total = getsize(source) / 1024                     #文件内容大小, 单位KB
    source = source.strip()
    bar_chunk = chunk
    copy_total = getsize(source)
    copy_chunk = 1024 * bar_chunk 
    progress = ProgressBar(source, total=bar_total, unit="KB", chunk_size=bar_chunk, run_status="正在拷贝", fin_status="拷贝完成")
    if not destination:
        copy(source, destination, copy_chunk, progress.refresh)
    elif thread_num: 
        tnum = thread_num
        destination = destination.strip() 
        make_empyt_file(destination, copy_total)
        parts = file_split(copy_total,tnum)
        db = DatabaseX() 
  
        func = {'f1':db.update, 'f2':progress.calulate}
        key_fmt = "thread{}.copied"
        threadName_fmt = "thread-{}"
        bar_total_copied = 0
        for i in range(tnum):
            name = key_fmt.format(i)
            tName = threadName_fmt.format(i)
            copied = db.get(name)
            if not copied: 
                copied = 0
                db.put(name, copied)  
            else:
                bar_total_copied += copied
                progress.completed_size = bar_total_copied / 1024        #已拷贝KB
            start, end = parts[i]  
            myargs = (source, destination, name, copy_chunk, func, copied, start, end)
            th = threading.Thread(target=copyX2, args=myargs)
            th.start() 
        
        monitor = threading.Thread(target=listener, args=(progress,db))
        monitor.start() 
          
        
    else: 
        destination = destination.strip()
        db = DatabaseX() 
        copied = db.get('size')
        if not copied: 
            copied = 0
            db.put('size', copied)  
        else:
            progress.completed_size = copied / 1024             #已拷贝KB

        func = {'f1':db.update, 'f2':progress.refresh}
        finished = copyx(source, destination, copy_chunk, func, copied, copy_total)

        if finished:
            db.destroy()
        else:
            db.close()



def download(url, destination, chunk, thread_num=0): 
    '''
    source -> source file abs path
    destination -> destination file abs path, if not entered, a default name provided
    chunk ->  a chunk to store buffer
    ''' 
    res = urllib.request.urlopen(url) 
    try:
        xtotal = int( res.headers['Content-Length'])
    except:
        xtotal = 217370560
    
    bar_total = xtotal / 1024                     #文件内容大小, 单位KB
    source = retrieveFileName(url) 
    bar_chunk = chunk
    copy_total = xtotal
    copy_chunk = 1024 * bar_chunk 
    progress = ProgressBar(source, total=bar_total, unit="KB", chunk_size=bar_chunk, run_status="正在拷贝", fin_status="拷贝完成")
    if not destination:
        copy(source, destination, copy_chunk, progress.refresh)
    elif thread_num: 
        tnum = thread_num
        destination = destination.strip() 
        make_empyt_file(destination, copy_total)
        parts = file_split(copy_total,tnum)
        db = DatabaseX() 
  
        func = {'f1':db.update, 'f2':progress.calulate}
        key_fmt = "thread{}.copied"
        threadName_fmt = "thread-{}"
        bar_total_copied = 0
        for i in range(tnum):
            name = key_fmt.format(i)
            tName = threadName_fmt.format(i)
            copied = db.get(name)
            if not copied: 
                copied = 0
                db.put(name, copied)  
            else:
                bar_total_copied += copied
                progress.completed_size = bar_total_copied / 1024        #已拷贝KB
            start, end = parts[i]  
            myargs = (res, destination, name, copy_chunk, func, copied, start, end)
            th = threading.Thread(target=copyX2, args=myargs)
            th.start() 
        
        monitor = threading.Thread(target=listener, args=(progress,db))
        monitor.start()  
    else: 
        destination = destination.strip()
        db = DatabaseX() 
        copied = db.get('size')
        if not copied: 
            copied = 0
            db.put('size', copied)  
        else:
            progress.completed_size = copied / 1024             #已拷贝KB

        func = {'f1':db.update, 'f2':progress.refresh}
        finished = copyx(res, destination, copy_chunk, func, copied, copy_total)

        if finished:
            db.destroy()
        else:
            db.close()

def listener(bar, database):
    while True:
        time.sleep(3)
        end = bar.print()
        if end: break
    database.destroy()


def make_empyt_file(file, size):
    '''创建一个大小为size的临时文件
    '''
    if exists(file):
        return 
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
     
 
    

def main(argv):
    ''' 参数说明:
    -i: 源文件
    -o: 目标文件
    -s: 复制最小内存单位, 默认 1KB
    -t: 复制线程数, 默认为 1
    '''
    source = None
    dest = None
    chunk = 1
    thread = 0
    try:
        opts, args = getopt.getopt(argv,"hi:o:s:t:",["ifile=","ofile=","chunkSize=","threadNum="])
    except getopt.GetoptError:
        print ('copy.py -i <inputfile> -o <outputfile> -s <chunksize> -t <threadNum>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('copy.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            source = arg
        elif opt in ("-o", "--ofile"):
            dest = arg 
        elif opt in ("-s", "--chunkSize"):
            chunk = int(arg)
        elif opt in ("-t", "--threadNum"):
            thread = int(arg)
    if source == None:
        raise Exception("source is required.")

    exec(source, dest, chunk, thread)


if __name__ == "__main__":
   #t1 = time.time()
   #main(sys.argv[1:])
   #s = r'f:\downloads\VSCodeSetup-x64-1.29.0.exe'
   #s = r'f:\downloads\a.txt'
   #d = r'f:\downloads\VSCodeSetup_9.exe'
   url =  r'http://172.17.0.15:10017/1/jdk1.8.html'
   d = r'g:\downloads\jdk1_8_test3.exe'
   download(url, d, 100,1)
   #t2 = time.time()
   #print("time consumed %.3f seconds" % (t2 - t1))


