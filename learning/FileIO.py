fpath = r'C:\Windows\system.ini'
wpath = r'g:\test.txt'
with open(fpath, 'r') as f:
    with open(wpath, 'w') as book: 
        print('Start')
        for line in f.readlines() : 
            print(line.strip()) 
            book.write(line)
        print('END')
