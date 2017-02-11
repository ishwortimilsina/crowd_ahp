import sqlite3
import numpy as np
from scipy import stats

# Finding all the Alternatives comparisons for a goal
def getNextAlternativesComparisons(sizeMatrix, goal, criteria, alternative_1, alternative_2, numOfRecords):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()


	query = 'SELECT value FROM {tn} WHERE goal_id={goal} and criteria_id={criteria} and alternative_1_id={alternative_1_id} and alternative_2_id={alternative_2_id} ORDER BY ROWID LIMIT {numOfRecords}'.\
        format(tn='alternatives_comparisons', goal=goal, criteria=criteria, alternative_1_id=alternative_1, alternative_2_id=alternative_2, numOfRecords=numOfRecords)
	
	allAlternativesComparisons = []

	c.execute(query)
	result = c.fetchall()

	if (result):
		for row in result:
			allAlternativesComparisons.append(row[0])
	else:
		return "Record not found"
	

	conn.close()

	mean, sigma = np.mean(allAlternativesComparisons), stats.sem(allAlternativesComparisons)
	
	conf_int = stats.t.interval(0.95, len(allAlternativesComparisons)-1, loc=mean, scale=sigma)
	print "Confidence Interval ---> " + str(conf_int)

	return (mean, conf_int)