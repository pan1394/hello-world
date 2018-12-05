import random

data = [i for i in range(1,101)]
random.shuffle(data)

def draw():
    if len(data) > 0:
        a = random.choice(data)
        index = data.index(a)
        return data.pop(index)
    return 0

isProcess = True
while isProcess:
    x = draw(); 
    if 0 == x:
        isProcess = False
    else:
        print("抽到编号为{}的幸运者".format(x))
        
        