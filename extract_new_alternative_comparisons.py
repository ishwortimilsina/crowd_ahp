import sqlite3
import numpy as np
from scipy import stats
import map_to_scale as mts

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
	
	conf_int = stats.t.interval(0.90, len(allAlternativesComparisons)-1, loc=mean, scale=sigma)

	#print "The newest element ---> " + str(allAlternativesComparisons[-1])
	#print "Comparison Mean ---> " + str(mean)

	# meanWithoutLastOneElement = np.mean(allAlternativesComparisons[:-1])
	# meanWithoutLastTwoElement = np.mean(allAlternativesComparisons[:-2])
	# meanWithoutLastThreeElement = np.mean(allAlternativesComparisons[:-3])

	# print "Comparison Mean without last element " + str(meanWithoutLastOneElement)
	# print "Comparison Mean without last two element " + str(meanWithoutLastTwoElement)
	# print "Comparison Mean without last three element " + str(meanWithoutLastThreeElement)

	loopBreaker = False
	# if (meanWithoutLastTwoElement == meanWithoutLastTwoElement and meanWithoutLastThreeElement == meanWithoutLastThreeElement): # to check for Nan
	# 	if np.abs(mean - meanWithoutLastOneElement) <= 0.01 and np.abs(meanWithoutLastOneElement - meanWithoutLastTwoElement) <= 0.01 and np.abs(meanWithoutLastTwoElement - meanWithoutLastThreeElement) <= 0.01 :
	#if (mean - conf_int[0]) / mean <= 0.05:
	if (mean - conf_int[0] <= 0.2):
		loopBreaker = True

	#print "Confidence Interval ---> " + str(conf_int)

	# While returning the value, we return the mean that is scaled to range 1/9 to 9
	scaledMean = mts.mappingToRequiredScale(mean)
	#print "Scaled Mean ---> " + str(scaledMean)

	return (scaledMean, conf_int, loopBreaker)