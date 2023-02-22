from contextlib import closing
from sqlite3 import connect
from datetime import datetime

class NoSearchResultsError(Exception):
    pass

class Query():
    """Abstract Query Class for querying databases. 
    Query should be instantiated as LuxQuery or LuxDetailsQuery.
    """
    def __init__(self):
        raise NotImplementedError

    def search():
        raise NotImplementedError

    def clean_data():
        raise NotImplementedError

    def format_data():
        raise NotImplementedError

class LuxQuery(Query):
    """"Class to represent querying the database. 
    Stores the database file for opening connection to later on. 
    Stores the columns for the output table.
    """

    def __init__(self, db_file):
        """Initalizes the class with the database file and 
        the columns and format_str for the output table.

        Args:
            db_file (str): database file
        """

        self._db_file = db_file
        self._columns = ["ID", "Label", "Produced By", "Date", "Member Of", "Classified As"]
        self._format_str=["w", "w", "w", "w", "w", "p"]

    def search(self, dep=None, agt=None, classifier=None, label=None):
        """Opens a connection to the database and uses the given argument to create a 
        SQL statement that query the database satisfying the search criteria. 

        Args:
            dep (str): selected department
            agt (str): selected agent
            classifer: selected slassifer
            label: selected label

        Return:
            list: numbers of items returned from query (search count), 
            columns for Table, a list of objects

        Arguments are by default None if not passed in.
        If no arguments are passed in output includes first 1000 objects in the database.

        Sort Order:
            Sorted first by object label/date, then by agent name/part, 
            then by classifier, then by department name.
        """
        with connect(self._db_file, isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                # objects.id, objects.label, agents.name, objects.date,
                # departments.name, classifiers.name
                smt_str = "SELECT DISTINCT objects.id, objects.label, agents.name,"
                smt_str += " productions.part, objects.date, departments.name, classifiers.name"
                smt_str += " FROM objects INNER JOIN productions ON productions.obj_id = objects.id"
                smt_str += " INNER JOIN agents ON productions.agt_id = agents.id"
                # joining objects and departments, using objects_departments
                smt_str += " INNER JOIN objects_departments ON"
                smt_str += " objects_departments.obj_id = objects.id"
                smt_str += " INNER JOIN departments ON departments.id = objects_departments.dep_id"
                # joining objects and classifiers, using objects_classifiers
                smt_str += " INNER JOIN objects_classifiers"
                smt_str += " ON objects_classifiers.obj_id = objects.id"
                smt_str += " INNER JOIN classifiers ON classifiers.id = objects_classifiers.cls_id"

                # counting how many variables were not None
                smt_count = 0
                smt_params = []

                if dep or agt or classifier or label:
                    smt_str += " WHERE"

                #append to the stm_str, using prepared statements to filter objects out
                # based on the given arguments if they exists
                if dep:
                    smt_str += f" departments.name LIKE ?"
                    smt_params.append(f"%{dep}%")
                    smt_count += 1
                if agt:
                    if smt_count >= 1:
                        smt_str += " AND"
                    smt_str += f" agents.name LIKE ?"
                    smt_count += 1
                    smt_params.append(f"%{agt}%")
                if classifier:
                    if smt_count >= 1:
                        smt_str += " AND"
                    smt_str += f" classifiers.name LIKE ?"
                    smt_count += 1
                    smt_params.append(f"%{classifier}%")
                if label:
                    if smt_count >= 1:
                        smt_str += " AND"
                    smt_str += f" objects.label LIKE ?"
                    smt_count += 1
                    smt_params.append(f"%{label}%")
                smt_str += " ORDER BY objects.label, objects.date, agents.name,"
                smt_str += " productions.part, classifiers.name, departments.name"

                #execute the statement and fetch the results
                cursor.execute(smt_str, smt_params)
                data = cursor.fetchall()

        #data formatting
        obj_dict = self.clean_data(data)
        obj_list = self.format_data(obj_dict)

        search_count = len(obj_list)
        return [search_count, self._columns, self._format_str, obj_list]

    def format_data(self, obj_dict):
        """Transform each object's dictionary into a list to fit the Table class requirements.

        Args:
            obj_dict (dict): dictionary of all the objects

        Returns:
            rows_list (list): a list with each object as a list which is a "row" in the Table
        """

        rows_list = []

        #loop through each obj in dictionary and convert the obj's dictionary to a list
        for key in obj_dict:

            #no more than 1000 objects in output
            if len(rows_list) == 1000:
                break

            #sort approriate key in ascending order
            obj_dict[key]['produced_by'].sort()
            obj_dict[key]['department'].sort()
            obj_dict[key]['classifier'].sort()

            #join appropriate strings together
            obj_dict[key]["produced_by"] = ", ".join(obj_dict[key]["produced_by"])
            obj_dict[key]["department"] = ", ".join(obj_dict[key]["department"])
            obj_dict[key]["classifier"] = "|".join(obj_dict[key]["classifier"])

            rows_list.append(list(obj_dict[key].values()))
        return rows_list

    def clean_data(self, data):
        """Creates a dictionary for each object with their relevant information 
        (id, label, produced_by, date, department, classifers).
        Stores them in a master dictionary (obj_dict) with their id as the key.

        Args:
            data (list): data returned from cursor.fetchall()

        Returns:
            obj_dict (dict): 
                key: object's id
                value: dictionary with all information relevant to the obhect
        """

        #master dictionary
        obj_dict = {}

        #loop through each row in the data, get the relevant data,
        # and store them in the dictionary for the relevant object
        for row in data:
            obj_id = str(row[0])
            label = row[1]
            produced_by = row[2]
            part_produced = row[3]
            date = row[4]
            department = row[5]
            classifier = row[6].lower()
            agent_and_part = f"{produced_by} ({part_produced})"

            #create a new dictionary for the object with the specified id
            # if it's not in the master dictionary already
            if obj_id not in obj_dict:
                obj_dict[obj_id] = {
                    "id" : obj_id,
                    "label" : label,
                    "produced_by" : [agent_and_part],
                    "date" : date,
                    "department": [department],
                    "classifier": [classifier] 
                }
            else:
                #check whether each attributes is in
                # the object's dictionary already, if not add it in
                if agent_and_part not in obj_dict[obj_id]['produced_by']:
                    obj_dict[obj_id]['produced_by'].append(agent_and_part)
                if department not in obj_dict[obj_id]['department']:
                    obj_dict[obj_id]['department'].append(department)
                if classifier not in obj_dict[obj_id]['classifier']:
                    obj_dict[obj_id]['classifier'].append(classifier)

        return obj_dict

class LuxDetailsQuery(Query):
    """"Class to represent querying the database. 
    Stores the database file for opening connection to later on. 
    Stores the columns for the output table.
    """

    def __init__(self, db_file):
        self._db_file = db_file
        self._columns_produced_by = ["Part", "Name", "Nationalities", "Timespan"]
        self._columns_information = ["Type", "Content"]
        self._format_str_produced=["w", "w", "p", "w"]
        self._format_str_information=["w","w"]

    def search(self, id):
        with connect(self._db_file, isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                # objects.label, productions.part, agents.name, nationalities.descriptor,
                # agents.begin_date, agents.end_date, classifiers.name
                smt_str = "SELECT DISTINCT objects.label, productions.part, agents.name,"
                smt_str += " nationalities.descriptor, agents.begin_date,"
                smt_str += " agents.end_date, classifiers.name,"
                smt_str += " \"references\".type, \"references\".content, agents.id"
                # joining objects and agents using productions
                smt_str += " FROM objects INNER JOIN productions ON productions.obj_id = objects.id"
                smt_str += " INNER JOIN agents on productions.agt_id = agents.id"
                # joining nationalities using agents_nationalities
                smt_str += " INNER JOIN agents_nationalities"
                smt_str += " ON agents_nationalities.agt_id = agents.id"
                smt_str += " INNER JOIN nationalities ON"
                smt_str += " nationalities.id = agents_nationalities.nat_id"
                # joining references
                smt_str += " INNER JOIN \"references\" ON \"references\".obj_id = objects.id"
                # joining classifiers using objects_classifiers
                smt_str += " INNER JOIN objects_classifiers ON"
                smt_str += " objects_classifiers.obj_id = objects.id"
                smt_str += " INNER JOIN classifiers ON classifiers.id = objects_classifiers.cls_id"
                smt_str += f" WHERE objects.id = ?"
                smt_params = [id]

                # execute the statement and fetch the results
                cursor.execute(smt_str, smt_params)
                data = cursor.fetchall()
                if not data:
                    raise NoSearchResultsError
        # data formatting
        agent_dict, obj_dict = self.clean_data(data)
        agent_rows_list = self.format_data(agent_dict)

        return [self._columns_produced_by, self._columns_information,
                self._format_str_information, self._format_str_produced, agent_rows_list, obj_dict]

    def format_data(self, obj_dict):
        """Transform each object's dictionary into a list to fit the Table class requirements.

        Args:
            obj_dict (dict): dictionary of all the objects

        Returns:
            rows_list (list): a list with each object as a list which is a "row" in the Table
        """

        rows_list = []

        #loop through each obj in dictionary and convert the obj's dictionary to a list
        for key in obj_dict:

            #no more than 1000 objects in output
            if len(rows_list) == 1000:
                break

            #join appropriate strings together
            obj_dict[key]["nationality"] = "|".join(obj_dict[key]["nationality"])
            rows_list.append(list(obj_dict[key].values()))

        return rows_list

    def clean_data(self, data):
        """Creates dictionaries for the object queried and the agents associated with that object 
        with their relevant information 
        (label, part_produced, produced_by, nationality, begin_date, end_date,
        classifier, ref_type, ref_content, agent_id).
        Stores them in master dictionaries (obj_dict, agent_dict). agent_dict has agent's id as key. 

        Args:
            data (list): data returned from cursor.fetchall()

        Returns:
            agent_dict (dict):
                key: agent's id
                value: dictionary with all information relevant to the agent
            obj_dict (dict): 
                value: dictionary with all information relevant to the obhect
        """

        #master dictionary
        agent_dict = {}
        obj_dict = {}

        #loop through each row in the data, get the relevant data,
        # and store them in the dictionary for the relevant object
        for row in data:
            label = row[0]
            part_produced = row[1]
            produced_by = row[2]
            nationality = row[3]
            begin_date = row[4]
            end_date = row[5]
            classifier = row[6]
            ref_type = row[7]
            ref_content = row[8]
            agent_id = row[9]

            timespan = self.parse_date(begin_date, end_date)

            # create dictionary for object if not already done
            if not obj_dict:
                obj_dict =  {
                    "label" : label,
                    "classifier" : [classifier],
                    "ref_type": [ref_type],
                    "ref_content": [ref_content]
                }
            # if dictionary has already been created, then we append classifiers
            else:
                if classifier not in obj_dict["classifier"]:
                    obj_dict['classifier'].append(classifier)
                if ref_type not in obj_dict['ref_type']:
                    obj_dict['ref_type'].append(ref_type)
                if ref_content not in obj_dict['ref_content']:
                    obj_dict['ref_content'].append(ref_content)

            # if agent has not been stored in agent_dict yet
            if agent_id not in agent_dict:
                agent_dict[agent_id] = {
                    "part": part_produced,
                    "name": produced_by,
                    "nationality": [nationality],
                    "timespan": timespan
                }
            # if agent has information stored in dictionary, then we append nationality
            else:
                if nationality not in agent_dict[agent_id]['nationality']:
                    agent_dict[agent_id]['nationality'].append(nationality)

        return agent_dict, obj_dict

    def parse_date(self, begin_date, end_date):
        """Given a begin_date (str) and end_date (str)
        formats the timespan needed for table in the form of {begin_year}-{end_year}.
        """

        if not begin_date and not end_date:
            return ""

        begin_year = ""
        end_year = ""

        if begin_date:
            begin_date_dt = datetime.strptime(begin_date, '%Y-%m-%d')
            begin_year = begin_date_dt.year

        if end_date:
            end_date_dt = datetime.strptime(begin_date, '%Y-%m-%d')
            end_year = end_date_dt.year

        return f"{begin_year}-{end_year}"
