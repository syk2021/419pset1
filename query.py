from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
from table import Table

class Query():  
    def __init__(self, db_file) -> None:
        self.db_file = db_file
        self.columns = ["ID", "Label", "Produced By", "Date", "Member Of", "Classified As"]

    def search(self, dep=None, agt=None, classifier=None, label=None):
        with connect(self.db_file, isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                # objects.id, objects.label, agents.name, objects.date, departments.name, classifiers.name
                smt_str = "SELECT DISTINCT objects.id, objects.label, agents.name, productions.part, objects.date, departments.name, classifiers.name FROM objects INNER JOIN productions ON productions.obj_id =  objects.id INNER JOIN agents ON productions.agt_id = agents.id"
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


                cursor.execute(smt_str)
                data = cursor.fetchall()
                obj_dict = self.clean_data(data)
                rows_list = []

                for key in obj_dict:
                    rows_list.append(list(obj_dict[key].values()))

                print(Table(self.columns, rows_list))


    def clean_data(self, data):
        obj_dict = {}
        for row in data:
            id = str(row[0])
            label = row[1]
            produced_by = row[2]
            part_produced = row[3]
            date = row[4]
            department = row[5]
            classifier = row[6]
            agent_and_part = f"{produced_by} ({part_produced})"

            if label not in obj_dict:
                obj_dict[label] = {
                    "id" : id,
                    "label" : label,
                    "produced_by" : [agent_and_part],
                    "date" : date,
                    "department": [department],
                    "classifier": [classifier] 
                }
            else:
                if agent_and_part not in obj_dict[label]['produced_by']:
                    obj_dict[label]['produced_by'].append(agent_and_part)
                    obj_dict[label]['produced_by'].sort()
                if department not in obj_dict[label]['department']:
                    obj_dict[label]['department'].append(department)
                    obj_dict[label]['department'].sort()
                if classifier not in obj_dict[label]['classifier']:
                    obj_dict[label]['classifier'].append(classifier)
                    obj_dict[label]['classifier'].sort()
                    
        return obj_dict




