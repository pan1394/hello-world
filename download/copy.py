from os.path import getsize
import sys, getopt, threading
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
       
def copyx(sourceFile, targetFile=None, bufferSize = 1024, realTimeFunc=None, copied=0, total=1):
    if targetFile == None:
        targetFile = replaceFileName(sourceFile)
    try:
        finished = False  
        with open(sourceFile, "rb") as s:
            if copied : s.seek(copied)
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
    except KeyboardInterrupt:
        print('error during copy...')  
    finally:
        if not finished: 
            print("[{}] being copied to [{}], copyed {}, complete rate: {:.1f}%.".format(sourceFile,targetFile, copied, float((copied/total) * 100)))
        else:
            print("[{}] has copied to [{}].".format(sourceFile,targetFile))
        return finished
  
def copy2(sourceFile, targetFile, bufferSize = 1024, realTimeFunc=None, copied=0, start=0, end=100):
    if targetFile == None:
        targetFile = replaceFileName(sourceFile)

    total = end - start
    position = start + copied
    try:
        finished = False  
        with open(sourceFile, "rb") as s:
            if position : s.seek(position)
            with open(targetFile, "ab") as d: 
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
                            if k == 'f1': func('size', copied)
                            if k == 'f2': func() 
                finished = True
        return finished
    except KeyboardInterrupt:
        print('error during copy...')  
    finally:
        if not finished: 
            print("[{}] being copied to [{}], copyed {}, complete rate: {:.1f}%.".format(sourceFile,targetFile, copied, float((copied/total) * 100)))
        else:
            print("[{}] has copied to [{}].".format(sourceFile,targetFile))
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

def exec(source, destination, chunk): 
    '''
    source -> source file abs path
    destination -> destination file abs path, if not entered, a default name provided
    chunk ->  a chunk to store buffer
    '''
    thead_enabled = True
    source = source.strip()
    bar_total = getsize(source) / 1024                     #文件内容大小, 单位KB
    bar_chunk = chunk
    copy_total = getsize(source)
    copy_chunk = 1024 * bar_chunk 
    progress = ProgressBar(source, total=bar_total, unit="KB", chunk_size=bar_chunk, run_status="正在拷贝", fin_status="拷贝完成")
    if not destination:
        copy(source, destination, copy_chunk, progress.refresh)
    elif thead_enabled:
        
        destination = destination.strip()
        thead_num = 3  
        make_empyt_file(destination, copy_total)
        parts = file_split(copy_total,thead_num)
        db = DatabaseX() 

        # contents=[b'abcdefg', b'123456','你'.encode('utf8'), b'hello jack']
        keys = ["thread{}.start", "thread{}.end", "thread{}.copied"]
        """ for i in range(thead_num):
            name = keys[i].format(thead_num)
            copied = db.get('size')
            if not copied: 
                copied = 0
                db.put('size', copied)  
            else:
                progress.completed_size = copied / 1024
            start, end = parts[i]
            th = threading.Thread(target=copy2, args=(f,contents[i], start, end))
            th.start()   """
        
    else: 
        destination = destination.strip()
        db = DatabaseX() 
        copied = db.get('size')
        if not copied: 
            copied = 0
            db.put('size', copied)  
        else:
            progress.completed_size = copied / 1024

        func = {'f1':db.update, 'f2':progress.refresh}
        finished = copyx(source, destination, copy_chunk, func, copied, copy_total)

        if finished:
            db.destroy()
        else:
            db.close()


def make_empyt_file(file, size):
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
     
 
    

def main(argv):
    source = None
    dest = None
    chunk = 1
    try:
        opts, args = getopt.getopt(argv,"hi:o:s:",["ifile=","ofile=","chunkSize="])
    except getopt.GetoptError:
        print ('copy.py -i <inputfile> -o <outputfile> -s <chunksize>')
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
    if source == None:
        raise Exception("source is required.")

    exec(source, dest, chunk)


if __name__ == "__main__":
   #main(sys.argv[1:])
   s = r'G:\downloads\WeChatSetup.exe'
   d = r'g:\Downloads\test12.exe'
   exec(s, d, 100)

