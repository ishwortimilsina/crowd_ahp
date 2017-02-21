import sqlite3
import numpy as np
from scipy import stats
import map_to_scale as mts

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

	mean, sigma = np.mean(allCriteriaComparisons), np.std(allCriteriaComparisons)

	conf_int = stats.t.interval(0.90, len(allCriteriaComparisons)-1, loc=mean, scale=sigma)
	
	#print "The newest element ---> " + str(allCriteriaComparisons[-1])	
	#print "Comparison Mean ---> " + str(mean)

	# meanWithoutLastOneElement = np.mean(allCriteriaComparisons[:-1])
	# meanWithoutLastTwoElement = np.mean(allCriteriaComparisons[:-2])
	# meanWithoutLastThreeElement = np.mean(allCriteriaComparisons[:-3])

	# print "Comparison Mean without last element " + str(meanWithoutLastOneElement)
	# print "Comparison Mean without last two element " + str(meanWithoutLastTwoElement)
	# print "Comparison Mean without last three element " + str(meanWithoutLastThreeElement)

	loopBreaker = False
	# if (meanWithoutLastTwoElement == meanWithoutLastTwoElement and meanWithoutLastThreeElement == meanWithoutLastThreeElement): # to check for Nan
	# 	if np.abs(mean - meanWithoutLastOneElement) <= 0.03 and np.abs(meanWithoutLastOneElement - meanWithoutLastTwoElement) <= 0.03 and np.abs(meanWithoutLastTwoElement - meanWithoutLastThreeElement) <= 0.03 :
	if (mean - conf_int[0] <= 0.2):	
		loopBreaker = True

	#print "Confidence Interval ---> " + str(conf_int)

	# While returning the value, we return the mean that is scaled to range 1/9 to 9
	scaledMean = mts.mappingToRequiredScale(mean)
	#print "Scaled Mean ---> " + str(scaledMean)

	return (scaledMean, conf_int, loopBreaker)