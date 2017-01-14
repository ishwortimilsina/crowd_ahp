import sqlite3
import numpy as np

# Finding all the criteria for a goal
def getAllCriteria(goal):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	query = 'SELECT criteria_id FROM {tn} WHERE goal_id={goal}'.\
					format(tn='criteria', goal=goal)
	c.execute(query)
	
	allCriteria = []
	for row in c.fetchall():
		allCriteria.append(row[0])

	conn.close()

	return allCriteria


# Finding all the criteria comparisons for a goal
def getAllCriteriaComparisons(goal):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()


	query = 'SELECT criteria_1_id, criteria_2_id, value FROM {tn} WHERE goal_id={goal}'.\
        format(tn='criteria_comparisons', goal=goal)

	allCriteriaComparisons = []
	c.execute(query)
	result = c.fetchall()
	if (result):
		for row in result:
			temp = []
			temp.append(row[0])
			temp.append(row[1])
			temp.append(row[2])
			allCriteriaComparisons.append(temp)
	else:
		return "Record not found"

	myDict = {}
	for row in allCriteriaComparisons:
		temp = []
		if (str(row[0])+'_'+str(row[1]) not in myDict):
			for col in allCriteriaComparisons:
				if row[0] == col[0] and row[1] == col[1]:
					temp.append(col[2])

			myDict[str(row[0])+'_'+str(row[1])] = temp

	conn.close()

	return myDict
	