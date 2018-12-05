from os.path import getsize
import sys, getopt
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
    except Exception as e:
        print('error during copy...')  
    else:
        print("[{}] has copied to [{}].".format(sourceFile,targetFile))
       
def copyx(sourceFile, targetFile=None, bufferSize = 1024, realTimeFunc=None):
    if targetFile == None:
        targetFile = replaceFileName(sourceFile)
    try:
        finished = False
        db = DatabaseX(targetFile)
        total = getsize(sourceFile.strip())
        size = db.get('size')
        if not size: 
            size = 0
            db.put('size', size) 

        with open(sourceFile, "rb") as s:
            if size : s.seek(size)
            with open(targetFile, "ab") as d: 
                while True:
                    chunk = None 
                    chunk = s.read(bufferSize)
                    size += len(chunk)
                    if not chunk : break
                    d.write(chunk)
                    if realTimeFunc:
                        db.update('size', size)
                        realTimeFunc()
                finished = True
    except Exception as e:
        print('error during copy...')  
    finally:
        if not finished:
            db.close()
            print("[{}] being copied to [{}], copyed {}, complete rate: {:.1f}%.".format(sourceFile,targetFile, size, float((size/total) * 100)))
        else:
            print("[{}] has copied to [{}].".format(sourceFile,targetFile))
            db.destroy()
  
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
    content_size = getsize(source.strip())/1024                     #文件内容大小, 单位KB
    chunk_size= chunk                                               #进度条chunk,  单位KB
    bufferSize = 1024 * chunk_size                                  #copy方法的chunk, 单位Byte
    progress = ProgressBar(source, total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在拷贝", fin_status="拷贝完成")
    copyx(source, destination, bufferSize, progress.refresh)
 

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
   s = r'F:\Downloads\VSCodeSetup-x64-1.29.0.exe'
   d = r'F:\Downloads\test4.exe'
   exec(s, d, 1)

