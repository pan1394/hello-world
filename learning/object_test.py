class Worker(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def get_gender(self):
        return self.gender
    
    def set_gender(self, gender):
        self.gender = gender

    def calulateSalary(self, salary) :
        if( not isinstance(salary, (int, float))) :
            raise TypeError('%s is not a salary num' % salary) 
        return salary * 12


# 测试:
bart = Worker('Bart', 'male')
print(bart.calulateSalary(100))
if bart.get_gender() != 'male':
    print('测试失败!')
else:
    bart.set_gender('female')
    if bart.get_gender() != 'female':
        print('测试失败!')
    else:
        print('测试成功!')


class Student(object):
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count = Student.count + 1
 
# 测试:
if Student.count != 0:
    print('测试失败!')
else:
    bart = Student('Bart')
    if Student.count != 1:
        print('测试失败!')
    else:
        lisa = Student('Bart')
        if Student.count != 2:
            print('测试失败!')
        else:
            print('Students:', Student.count)
            print('测试通过!')
