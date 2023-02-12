from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
from table import Table
from query import Query
import argparse

DB_NAME = "./lux.sqlite"

class LuxCLI():
    
    def __init__(self) -> None:
        self.query = Query(DB_NAME)
        self.department = None
        self.agent = None
        self.classifier = None
        self.label = None

        self.parse_args()
        self.query.search(dep=self.department, agt=self.agent, classifier=self.classifier, label=self.label)

    def parse_args(self):
        parser = argparse.ArgumentParser(
                    prog = 'lux.py', allow_abbrev=False)

        parser.add_argument("-d", help="show only those objects whose department label contains department", metavar='dep')
        parser.add_argument("-a", help="show only those objects produced by an agent with name containing agentname", metavar='agt')
        parser.add_argument("-c", help="show only those objects classifier with a classifier having a name containing cls", metavar='cls')
        parser.add_argument("-l", help="show only those objects whose label contains label", metavar='label')

        args = parser.parse_args()

        self.department = args.d
        self.agent = args.a
        self.classifier = args.c
        self.label = args.l

        



if __name__ == '__main__':
    LuxCLI()