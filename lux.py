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

        parser.add_argument("-d", help="dep show only those objects whose department label contains department", metavar='\b')
        parser.add_argument("-a", help="agt show only those objects produced by an agent with name containing agentname", metavar='\b')
        parser.add_argument("-c", help="acls show only those objects classified with a classifier having a name containing cls", metavar='\b')
        parser.add_argument("-l", help="label show only those objects whose label contains label", metavar='\b')

        args = parser.parse_args()

        self.department = args.d
        self.agent = args.a
        self.classifier = args.c
        self.label = args.l



if __name__ == '__main__':
    LuxCLI()