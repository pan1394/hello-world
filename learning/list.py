L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [ a.lower() for a in L1 if isinstance(a, str)]

print(L2)
if L2 == ['hello', 'world', 'apple']:
    print('测试通过!')
else:
    print('测试失败!')