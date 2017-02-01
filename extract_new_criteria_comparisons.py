import sqlite3
import numpy as np

# Finding all the Criteira comparisons for a goal
def getNextCriteriaComparisons(sizeMatrix, goal, criteria_1, criteria_2, numOfRecords):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()


	query = 'SELECT value FROM {tn} WHERE goal_id={goal} and criteria_1_id={criteria_1_id} and criteria_2_id={criteria_2_id} ORDER BY ROWID LIMIT {numOfRecords}'.\
        format(tn='criteria_comparisons', goal=goal, criteria_1_id=criteria_1, criteria_2_id=criteria_2, numOfRecords=numOfRecords)
	
	c.execute(query)
	result = c.fetchall()

	allCriteriaComparisons = []
	if (result):
		for row in result:
			allCriteriaComparisons.append(row[0])
	else:
		return "Record not found"
	
	conn.close()
	
	return np.average(allCriteriaComparisons)