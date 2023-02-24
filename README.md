# CPSC 419 PSET 1 PARTNER GROUP 9

Group members: Sophia Kang (yk575), Phuc Duong (phd24)

## Contributions
Sophia Kang contribution:
- initial query & backbone structure for LuxQuery class
- writing query for LuxDetailsQuery class
- error handling with try except clauses in lux.py, luxdetails.py
- writing LuxDetailsCLI output function
- writing docstrings for classes and functions
- pylint on query.py, lux.py, luxdetails.py
- testing on lux.py, luxdetails.py & error handling
- readme documentation

Phuc Duong contribution:
- Common Table Expression query (used in LuxQuery class)
- implementing argparse module in LuxCLI and LuxDetailsCLI
- writing LuxCLI output function
- reading & implementing Table documentation
- parsing and cleaning data for query.py
- modularizing the code
- pylint on query.py, lux.py, luxdetails.py & error handling
- testing on lux.py, luxdetails.py

## Description of outside help
ULA office hours

## Description of sources of information that you used while doing the assignment, not direct help from people
None

## Indication of how much time you spent doing the assignment, rounded to the nearest hour
17 hours

## Assessment of the assignment
- Did it help you to learn? / What did it help you to learn?
It helped us write SQL queries - we both wrote Common Table Expression (CTE) for the first time. We also learned the difference between LEFT OUTER JOIN and INNER JOIN.

- Do you have any suggestions for improvement? Etc.
An example on how to use the Table function or example outputs in the spec would be helpful.

## Any information to graders
For query.py, we have a pylint error that says too many local variables, but we only exceeded the limit by 1 or 3 and have tried to eliminate local variables without making the code unreadable. There is an error with the number of arguments from LuxDetailsQuery, because we inherit from the Query class, but we think this is negligible for the most part. We have no errors for lux.py and luxdetails.py.