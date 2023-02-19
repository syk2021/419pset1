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

    def __init__(self) -> None:
        """Initalizes the CLI with the passed in arguments from the terminal and query the database with the args."""

        self._query = Query(DB_NAME)
        self._department = None
        self._agent = None
        self._classifier = None
        self._label = None

        self.parse_args()

        self._query.search(dep=self._department, agt=self._agent, classifier=self._classifier, label=self._label)

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
    LuxCLI()