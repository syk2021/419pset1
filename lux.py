from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
from table import Table
from query import Query
import argparse

DB_NAME = "./lux.sqlite"

class LuxCLI():
    """"Class to represent the command line interface for the program.
    Stores the a query class, and the inputted department, agent, classifers, and label.
    """

    def __init__(self, db_name) -> None:
        """Initalizes the CLI with the passed in arguments from the terminal and create a query with the given database file.
        Query the database with the args and output the results into Console.

        Args:
            db_name (str): database file
        """

        self._query = Query(db_name)
        self._department = None
        self._agent = None
        self._classifier = None
        self._label = None

        self.parse_args()

        response = self._query.query_filter(dep=self._department, agt=self._agent, classifier=self._classifier, label=self._label)
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
            -d: department
            -a: agent
            -c: classifer
            -l: label
        """
        
        parser = argparse.ArgumentParser(
                    prog = 'lux.py', allow_abbrev=False)

        parser.add_argument("-d", help="show only those objects whose department label contains department", metavar='dep')
        parser.add_argument("-a", help="show only those objects produced by an agent with name containing agentname", metavar='agt')
        parser.add_argument("-c", help="show only those objects classifier with a classifier having a name containing cls", metavar='cls')
        parser.add_argument("-l", help="show only those objects whose label contains label", metavar='label')

        args = parser.parse_args()

        #set the instance variables to the args passed in by the user
        #None if nothing is passed in
        self._department = args.d
        self._agent = args.a
        self._classifier = args.c
        self._label = args.l

        
if __name__ == '__main__':
    LuxCLI(DB_NAME)