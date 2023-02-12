from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
from table import Table

class Query():  
    def __init__(self, db_file) -> None:
        self.db_file = db_file

    def search(self, dep=None, agt=None, classifier=None, label=None):
        with connect(self.db_file, isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                # objects.id, objects.label, agents.name, objects.date, departments.name, classifiers.name
                smt_str = "SELECT DISTINCT objects.id, objects.label, agents.name, objects.date FROM objects INNER JOIN productions ON productions.obj_id =  objects.id INNER JOIN agents ON productions.agt_id = agents.id"
                # joining objects and departments, using objects_departments
                smt_str += " INNER JOIN objects_departments ON objects_departments.obj_id = objects.id INNER JOIN departments ON departments.id = objects_departments.dep_id"
                # # joining objects and classifiers, using objects_classifiers
                smt_str += " INNER JOIN objects_classifiers ON objects_classifiers.obj_id = objects.id INNER JOIN classifiers ON classifiers.id = objects_classifiers.cls_id"

                # counting how many variables were not None 
                count = sum(x is not None for x in [dep, agt, classifier, label])

                if dep or agt or classifier or label:
                    smt_str += " WHERE"
                if dep:
                    smt_str += f" departments.name LIKE '%{dep}%'"
                if agt:
                    if count > 1:
                        smt_str += " AND"
                    smt_str += f" agents.name LIKE '%{agt}%'"
                if classifier:
                    if count > 1:
                        smt_str += " AND"
                    smt_str += f" classifiers.name LIKE '%{classifier}%'"
                if label:
                    if count > 1:
                        smt_str += " AND"
                    smt_str += f" objects.label LIKE '%{label}%'"
                # print(smt_str)
                cursor.execute(smt_str)
                
                # SELECT agents.name FROM objects NATURAL JOIN agents;
                # SELECT objects.label, agents.name FROM (objects INNER JOIN productions ON productions.obj_id = objects.id) INNER JOIN agents ON productions.agt_id = agents.id;
                data = cursor.fetchall()
                print(len(data))
                
                for row in data:
                    print(row)

    



