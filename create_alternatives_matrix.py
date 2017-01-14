import sqlite3
import numpy as np
import alternatives_collection as coll

def createMatrix(size, comparisons):
	arr = np.zeros((size,size))
	for i in range(0,size):
		for j in range (0, size):
			if i==j:
				arr[i][j] = 1
			else:
				for key, value in comparisons.items():
					splitKey= key.split('_')
					if int(splitKey[0])-1 == i and int(splitKey[1])-1==j:
						arr[i][j] = float(value)
						arr[j][i] = 1/float(value)

	return arr

# This finds a representative value out of a given array
def getRepresentation(arr):
	total = 0
	for value in arr:
		total += value

	return total/len(arr)


# This function return a new dictionary with representative value for each key
def getAllRepresentativeAlternativesComparisons(allAlternativesComparisons):
	newDict = {}
	for key, value in allAlternativesComparisons.items():
		newDict[key] = getRepresentation(value)

	return newDict

########################################################################################
######################################   MAIN   ########################################
########################################################################################

def getAlternativesCriteriaMatrix(goal, criteria):
	allAlternatives = coll.getAllAlternatives(goal)

	allAlternativesComparisons = coll.getAllAlternativesComparisons(goal, criteria)

	allRepresentativeAlternativesComparisons = getAllRepresentativeAlternativesComparisons(allAlternativesComparisons)
	
	return createMatrix(len(allAlternatives), allRepresentativeAlternativesComparisons)