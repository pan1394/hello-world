from os.path import getsize
import sys, getopt
sys.path.append('../')
from download.progressBar import ProgressBar


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
        print(e)
    else:
        print("[{}] has copied to [{}].".format(sourceFile,targetFile))
 
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
    content_size = getsize(source.strip())/1024                 #文件内容大小, 单位KB
    chunk_size= chunk                                   #进度条chunk,  单位KB
    bufferSize = 1024 * chunk_size                      #copy方法的chunk, 单位Byte
    progress = ProgressBar(source, total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在拷贝", fin_status="拷贝完成")
    copy(source, destination, bufferSize, progress.refresh)
 

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
   main(sys.argv[1:])
