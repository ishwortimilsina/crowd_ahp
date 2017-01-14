import sqlite3
import numpy as np

# Finding all the Alternatives for a goal
def getAllAlternatives(goal):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	c.execute('SELECT alternative_id FROM {tn} WHERE goal_id={goal}'.\
					format(tn='alternatives', goal=goal))
	allAlternatives = []
	for row in c.fetchall():
		allAlternatives.append(row[0])

	conn.close()

	return allAlternatives


# Finding all the Alternatives comparisons for a goal
def getAllAlternativesComparisons(goal, criteria):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()


	query = 'SELECT alternative_1_id, Alternative_2_id, value, criteria_id FROM {tn} WHERE goal_id={goal} and criteria_id={criteria}'.\
        format(tn='alternatives_comparisons', goal=goal, criteria=criteria)

	allAlternativesComparisons = []

	c.execute(query)
	result = c.fetchall()

	if (result):
		for row in result:
			temp = []
			temp.append(row[0])
			temp.append(row[1])
			temp.append(row[2])
			temp.append(row[3])
			allAlternativesComparisons.append(temp)
	else:
		return "Record not found"
	
	myDict = {}
	for row in allAlternativesComparisons:
		temp = []
		if (str(row[0])+'_'+str(row[1]) not in myDict):
			for col in allAlternativesComparisons:
				if row[0] == col[0] and row[1] == col[1]:
					temp.append(col[2])

			myDict[str(row[0])+'_'+str(row[1])] = temp

	conn.close()
	
	return myDict
	