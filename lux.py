from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
from table import Table
from query import Query
DB_NAME = "./lux.sqlite"

class LuxCLI():
    
    def __init__(self) -> None:
        self.query = Query(DB_NAME)

        department = None
        agent = None
        classifier = None
        label = None

        if '-d' in argv:
            d_index = argv.index('-d')
            department = argv[d_index+1]

        if '-a' in argv:
            a_index = argv.index('-a')
            agent = argv[a_index+1]
        
        if '-c' in argv:
            c_index = argv.index('-c')
            classifier = argv[c_index+1]
        
        if '-l' in argv:
            l_index = argv.index('-l')
            label = argv[l_index+1]
        
        self.query.search(dep=department, agt=agent, cls=classifier, label=label)

        pass

if __name__ == '__main__':
    LuxCLI()