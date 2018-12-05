import re


def is_valid_email(addr):
    reg = re.compile(r'[a-zA-Z.]+@[a-zA-Z.]+')
    return re.match(reg, addr) 


# 测试:
assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')


def name_of_email(addr):
    reg = re.compile(r'(<\w+ \w+> )?([a-zA-Z\.]+)@[a-zA-Z\.]+')
    name = ''
    if re.match(reg, addr) : 
        x,y = re.match(reg, addr).group(1,2) 
        name =  (x and x[1:-2]) or y 
    return name

#name_of_email('<Tom Paris> tom@voyager.org')
#name_of_email('tom@voyager.org')
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')