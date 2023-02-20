from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
from table import Table
from query import Query
import argparse


DB_NAME = "./lux.sqlite"

class LuxDetailsCLI():
    def __init__(self, db_name):
        """Initalizes the CLI with the id given be the user and create a query with the given database file.
        Query the database with based on the given id and output the results into Console.

        Args:
            db_name (str): database file
        """

        self._query = Query(db_name)
        self._id = None

        self.parse_args()

        response = self._query.query_id(id=self._id)
        self.output_results(response)


    def output_results(self, response):
        """Takes in the results from a database query and output and
        displays in the console a table of objects filtered by department, agent, classification, and title.

        Args:
            response (list): [search_count, columns, obj_list] returned from db query
        """

        search_count = response[0]
        columns = response[1]
        obj_list = response[2]

        print(f"Search produced {search_count} objects.")
        print(Table(columns, obj_list, preformat_sep=""))

    def parse_args(self):
        """Uses ArgParse to parse the arguments inputted by the user and store it as instance variables.
        Takes in:
            -id: id
        """
        
        parser = argparse.ArgumentParser(
                    prog = 'luxdetails.py', allow_abbrev=False)
        

        parser.add_argument("-id", help="the id of the object whose details should be shown", metavar='id')
        

        args = parser.parse_args()

        self._id = args.id

if __name__ == '__main__':
    LuxDetailsCLI(DB_NAME)
