"""Module for running luxdetails.py"""
import argparse
import sys
import sqlite3

from table import Table
from query import LuxDetailsQuery, NoSearchResultsError

DB_NAME = "./lux.sqlite"

class LuxDetailsCLI():
    """"Class to represent the command line interface for the program.
    Stores the a query class, and the inputted id of the object.
    """
    def __init__(self, db_name):
        """Initalizes the CLI with the id given be the user
        and create a query with the given database file.
        Query the database with based on the given id and output the results into Console.

        Args:
            db_name (str): database file
        """

        self._query = LuxDetailsQuery(db_name)
        self._id = None

        self.parse_args()

        try:
            response = self._query.search(self._id)
        except sqlite3.Error as err:
            print(err, file=sys.stderr)
            sys.exit()
        except NoSearchResultsError:
            print("Invalid id.")
            sys.exit()

        self.output_results(response)

    def output_results(self, response):
        """Takes in the results from a database query
        and output and displays in the console a the label
        information about agent (part, name, nationalities, timespan)
        classification, and information.

        Args:
            response (list): [columns_produced_by, columns_information, agent_rows_list, obj_dict]
            returned from db query
        """

        columns_produced_by = response[0]
        columns_information = response[1]
        format_str_informaton = response[2]
        format_str_produced = response[3]
        agent_rows_list = response[4]
        obj_dict = response[5]
        information_list = self.parse_type_content(obj_dict['ref_type'], obj_dict['ref_content'])

        divider = "----------------\n"
        space = "\n"
        res = "\n"

        #build the output
        res += divider
        res += "Label\n"
        res += divider
        res += obj_dict['label'] + space
        res += space

        res += divider
        res += "Produced By\n"
        res += divider
        res += str(Table(columns_produced_by, agent_rows_list,
                        format_str=format_str_produced)) + space
        res += space

        res += divider
        res += "Classification\n"
        res += divider
        res += ", ".join(obj_dict['classifier']).lower() + space
        res += space

        res += divider
        res += "Information\n"
        res += divider

        res += str(Table(columns_information, information_list,
                         format_str=format_str_informaton)) + space
        res += space

        print(res, end="")

    def parse_type_content(self, list_type, list_content):
        """Parse type and content to fit Table requirements."""
        new_list = []
        for index, type_elem in enumerate(list_type):
            new_list.append([type_elem, list_content[index]])
        return new_list

    def parse_args(self):
        """Uses ArgParse to parse the arguments inputted by the user and store it
        as instance variables.

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
