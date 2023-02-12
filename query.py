from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
from table import Table



class Query():  
    def __init__(self, db_file) -> None:
        self.db_file = db_file

    def search(self, dep=None, agt=None, cls=None, label=None):
        with connect(self.db_file, isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:

                smt_str = "SELECT * FROM objects LIMIT 5"
                
                
                cursor.execute(smt_str)
                
                
                
                
                
                data = cursor.fetchall()
                print(len(data))

                rows_list = []
                
                for row in data:
                    rows_list.append(list(row))


    



