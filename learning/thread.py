
import threading
import time 

def test():
    try:
        print('current thread:', threading.currentThread().getName())
        count = 0
        while True:
            count += 1
    except Exception as e :
        print('error') 
    finally:
        print('finally block')

if __name__ == "__main__":
    my = threading.Thread(target=test)
    my.start()
    


