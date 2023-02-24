query_lux = "(WITH classifier AS (
    SELECT objects.id, classifiers.name AS cls_name
    FROM objects
    LEFT OUTER JOIN objects_classifiers ON objects_classifiers.obj_id = objects.id
    LEFT OUTER JOIN classifiers ON classifiers.id = objects_classifiers.cls_id
    ORDER BY LOWER(classifiers.name)
),
agent as (
        SELECT objects.id, agents.name as agt_name, productions.part as prod_part
        FROM objects
        LEFT OUTER JOIN productions ON productions.obj_id = objects.id
        LEFT OUTER JOIN agents ON productions.agt_id = agents.id
    ),
department as (
        SELECT objects.id, departments.name as dep_name
        FROM objects
        LEFT OUTER JOIN objects_departments ON objects_departments.obj_id = objects.id
        LEFT OUTER JOIN departments ON departments.id = objects_departments.dep_id
)

SELECT objects.id, objects.label, GROUP_CONCAT(distinct agent.agt_name || ' (' || agent.prod_part || ')'), 
objects.date,  department.dep_name,  GROUP_CONCAT(classifier.cls_name, "|")
FROM objects
LEFT OUTER JOIN classifier ON classifier.id = objects.id
LEFT OUTER JOIN agent ON agent.id = objects.id
LEFT OUTER JOIN department ON department.id = objects.id
GROUP BY objects.id, objects.label
ORDER BY objects.label; )""


