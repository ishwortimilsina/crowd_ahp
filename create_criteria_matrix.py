import sqlite3
import numpy as np
import criteria_collection as coll
import operator
import map_to_scale as mts

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
						arr[i][j] = float(mts.mappingToRequiredScale(value))
						arr[j][i] = 1/arr[i][j]

	return arr

# This finds a representative value out of a given array
def getRepresentation(arr):
	total = 0
	count = 0
	for value in arr:
		if count == 1:
			break
		total += value
		count += 1
	
	return total/count


# This function return a new dictionary with representative value for each key
def getAllRepresentativeCriteriaComparisons(allCriteriaComparisons):
	newDict = {}

	for key, value in allCriteriaComparisons.items():
		newDict[key] = getRepresentation(value)

	return newDict

########################################################################################
######################################   MAIN   ########################################
########################################################################################

def getCriteriaMatrix(goal):
	allCriteria = coll.getAllCriteria(goal)

	allCriteriaComparisons = coll.getAllCriteriaComparisons(goal)

	allRepresentativeCriteriaComparisons = getAllRepresentativeCriteriaComparisons(allCriteriaComparisons)
	
	return createMatrix(len(allCriteria), allRepresentativeCriteriaComparisons)