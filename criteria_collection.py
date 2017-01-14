import sqlite3
import numpy as np

# Finding all the criteria for a goal
def getAllCriteria(goal):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	c.execute('SELECT cr.criteria_id FROM {tn1} g, {tn2} cr WHERE g.ROWID=cr.goal_id and g.goal="{goal}"'.\
					format(tn1='goals', tn2='criteria', goal=goal))
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


	query = 'SELECT cr.criteria_1_id, cr.criteria_2_id, cr.value FROM {tn1} g, {tn2} cr WHERE g.ROWID=cr.goal_id and g.goal="{goal}"'.\
        format(tn1='goals', tn2='criteria_comparisons', goal=goal)

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
	