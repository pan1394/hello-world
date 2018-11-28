import math

def findMinAndMax(L):
    if len(L) == 0 : 
        return (None, None)
    elif len(L) == 1 :
        return (L[0], L[0])
    else :
        min = 99999
        max = -99999
        for n in L :
            if n > max :
                max = n
            if n < min :
                min = n
        return (min, max)


 

# 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')