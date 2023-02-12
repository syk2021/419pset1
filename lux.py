from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
from table import Table

with connect('./lux.sqlite', isolation_level=None, uri=True) as connection:
    with closing(connection.cursor()) as cursor:
        smt_str = "SELECT * FROM objects LIMIT 5"
        cursor.execute(smt_str)
        data = cursor.fetchall()
        print(len(data))

        rows_list = []
        
        for row in data:
            rows_list.append(list(row))

        print(Table(["ID", "label", "name"], [["hi", "hi", "hi"]]))

        
        