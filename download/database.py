import shelve, os

class DatabaseX():
    
    def __init__(self, databaseName='tmp'):
        self.name = databaseName
        self.db = shelve.open(databaseName)
    
    def put(self, key, value):
        self.db.setdefault(key, value)
    
    def update(self, key, value):
        self.db.update({key:value})

    def get(self, key):
        return self.db.get(key)

    def close(self):
        self.db.close()
    
    def destroy(self):
        self.close() 
        lst = ['.dat','.dir','.bak']
        for x in lst:
            os.remove(self.name + x)


if __name__ == "__main__":
    db = DatabaseX() 
    print(db.get('size'))
    print(db.get('position')) 