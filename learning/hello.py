 
import math

def quadratic(a, b, c):
    if not isinstance(a, (int, float)):
        raise TypeError ('{0} is not a number'.format(a))
    if not isinstance(b, (int, float)):
        raise TypeError ('{0} is not a number'.format(b))
    if not isinstance(c, (int, float)):
        raise TypeError ('{0} is not a number'.format(c))
    
    temp = math.sqrt(math.pow(b, 2) - 4*a*c)
    x1 = (-b + temp) / (2 * a)
    x2 = (-b - temp) / (2 * a)
    return x1, x2

print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')