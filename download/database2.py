import shelve, os

class Database():
    
    fmt = "{} : {}\n"

    def newfile(self):
        if not os.path.exists(self.name):
            f = open(self.name, "w")
            f.close()

    def __init__(self, databaseName='tmp'):
        self.name = databaseName
        self.newfile()
        self.db = open(databaseName, 'r+') 
        self.dictionary = {}
        self.keys = set()
        self._parse()

    def _parse(self):
        self.db.seek(0)
        lines = self.db.readlines()
        for line in lines:
            item = line.split(":")
            key = item[0].strip()
            value = item[1][:-1].strip()
            self.keys.add(key)
            self.dictionary.setdefault(key, value)

    def put(self, key, value): 
        self._update(key, value)
        self._write()

    def _update(self, key, value):
        if key not in self.keys:
            self.dictionary.setdefault(key, value)
        else:
            self.dictionary[key] = value

    def _write(self):
        self.db.seek(0)
        for key, value in self.dictionary.items():
            item = Database.fmt.format(key, value)    
            self.db.write(item)  
 
    def get(self, key):
        self.dictionary.get(key)


    def close(self): 
        self.db.close()

    
    def destroy(self): 
        self.close()  
        os.remove(self.name)



def test(db, key):
    count = 0
    while True:
        count += 1
        db.put(key, count)



if __name__ == "__main__":

    import threading
 
    db = Database() 
    db.put('key', 0)
    db.put('position', 0)

    db.put('key', 'heelo')

   
    th = threading.Thread(target=test, args=(db,'key'))
    th.start()
    
    th2 = threading.Thread(target=test, args=(db,'position'))
    th2.start()
  
 

    #db.destroy()