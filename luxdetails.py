from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
from table import Table
from query import LuxDetailsQuery
import argparse


DB_NAME = "./lux.sqlite"

class LuxDetailsCLI():
    def __init__(self, db_name):
        """Initalizes the CLI with the id given be the user and create a query with the given database file.
        Query the database with based on the given id and output the results into Console.

        Args:
            db_name (str): database file
        """

        self._query = LuxDetailsQuery(db_name)
        self._id = None

        self.parse_args()

        response = self._query.search(self._id)
        # response = self._query.query_id(id=self._id)
        self.output_results(response)


    def output_results(self, response):
        """Takes in the results from a database query and output and
        displays in the console a the label, information about agent (part, name, nationalities, timespan), classification, and information.

        Args:
            response (list): [columns_produced_by, columns_information, agent_rows_list, obj_dict] returned from db query
        """

        columns_produced_by = response[0]
        columns_information = response[1]
        agent_rows_list = response[2]
        obj_dict = response[3]

        divider = "----------------\n"
        space = "\n"
        res = "\n"

        res += divider
        res += "Label\n"
        res += divider
        res += obj_dict['label'] + space
        res += space

        res += divider
        res += "Produced\n"
        res += divider
        res += str(Table(columns_produced_by, agent_rows_list)) + space
        res += space
        res += divider

        res += divider
        res += "Classification\n" 
        res += divider
        res += ", ".join(obj_dict['classifier']) + space
        res += space

        res += divider
        res += "Information\n"
        res += divider
        res += str(Table(columns_information, [[obj_dict['ref_type'], obj_dict['ref_content']]])) + space
        res += space
        print(res, end="")

    def parse_args(self):
        """Uses ArgParse to parse the arguments inputted by the user and store it as instance variables.
        Takes in:
            -id: id
        """
        
        parser = argparse.ArgumentParser(
                    prog = 'luxdetails.py', allow_abbrev=False)
        

        parser.add_argument("id", help="the id of the object whose details should be shown")
        

        args = parser.parse_args()

        self._id = args.id

if __name__ == '__main__':
    LuxDetailsCLI(DB_NAME)

