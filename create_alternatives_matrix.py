import math
import numpy as np
import alternatives_collection as coll
import map_to_scale as mts
from scipy import stats

def createMatrix(size, comparisons):
	np.set_printoptions(suppress=True)
	arr = np.zeros((size,size))
	for i in range(0,size):
		for j in range (0, size):
			if i==j:
				arr[i][j] = 1
			else:
				for key, value in comparisons.items():
					splitKey= key.split('_')
					if int(splitKey[0])-1 == i and int(splitKey[1])-1==j:
						# While returning the value, we return the mean that is scaled to range 1/9 to 9
						arr[i][j] = float(mts.mappingToRequiredScale(value[0]))
						arr[j][i] = 1/arr[i][j]

	return arr

# This finds a representative value out of a given array
def getRepresentation(arr):
	count = 1
	temp = []
	z = 1.96 # for confidence level of 95%
	moe = 0.75
	p = 0.5
	q = 1-0.5
	pq = p * q

	n = pq * z * z / (moe * moe)
	n = math.ceil(n)
	# sigma = np.std(arr)	
	# x = z * sigma/0.75
	# n = math.ceil(x*x)
	print n
	for value in arr:
		temp.append(value)
		if count > 1:
			mean, sigma = np.mean(temp), np.std(temp)
			conf_int = stats.t.interval(0.70, len(temp)-1, loc=mean, scale=sigma)
			print "New Value -------------> " + str(value)
			print "Mean ------------------> " + str(mean)
			print "Confidence Interval ---> " + str(conf_int)
			print "Number of tuples ------> " + str(count)
			print "______________________________________________________________________________________"
			# if (np.abs(mean - conf_int[0]) <= 0.8) and count >= 5:
			# 	break
		if count == n:
			break

		if count < 100:
			count += 1
	
	return round(np.mean(temp), 4), np.around(conf_int, decimals=4), count


# This function return a new dictionary with representative value for each key
def getAllRepresentativeAlternativesComparisons(allAlternativesComparisons):
	newDict = {}
	for key, value in allAlternativesComparisons.items():
		print key
		newDict[key] = getRepresentation(value)
		print "______________________________________________________________________________________"
		print "For this particular cell, "+key+" this is the final tally"
		print "Mean ------------------> " + str(newDict[key][0])
		print "Confidence Interval ---> " + str(newDict[key][1])
		print "Number of tuples ------> " + str(newDict[key][2])
		print "______________________________________________________________________________________"
		print "______________________________________________________________________________________"

	return newDict

########################################################################################
######################################   MAIN   ########################################
########################################################################################

def getAlternativesCriteriaMatrix(goal, criteria):
	allAlternatives = coll.getAllAlternatives(goal)

	allAlternativesComparisons = coll.getAllAlternativesComparisons(goal, criteria)

	allRepresentativeAlternativesComparisons = getAllRepresentativeAlternativesComparisons(allAlternativesComparisons)

	return createMatrix(len(allAlternatives), allRepresentativeAlternativesComparisons), allRepresentativeAlternativesComparisons