def trim(s):
    length = len(s)
    if(length == 0):
        return ''
    start = 0
    end = 0
    n = 0
    while n < length  :
        if(s[n] != ' ') :
            start = n
            break
        n=n+1
    n = length -1
    while n > -1 :
        if(s[n] != ' ') :
            end = n+1
            break
        n=n-1
    return s[start:end]


# 测试:
if trim('hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello') != 'hello':
    print('测试失败!')
elif trim('  hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败!')
elif trim('') != '':
    print('测试失败!')
elif trim('    ') != '':
    print('测试失败!')
else:
    print('测试成功!')