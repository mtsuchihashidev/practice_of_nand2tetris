class TableA(object): pass
class TableB(object): pass
class TableC(object): pass
class Table:
    def __init__(self,i):
        self.__i = i
    def __eq__(self, other):
        return self.__i == other.__i
    def __hash__(self):
        return hash(self.__i)

class Poller(object):
    TABLES = {Table(1): '1',
              Table(2): '2',
              Table(3): '3'}
    
    def poll(self):
        for table, value in self.TABLES.items():
            # look for an entry
            print(table)
            print(table.__hash__())
        print(self.TABLES[Table(1)])
        return

p = Poller()
p.poll()
